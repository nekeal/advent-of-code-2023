import importlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal

import aocd
import pytest
import typer
from aocd import AocdError
from aocd.exceptions import PuzzleLockedError
from aocd.models import Puzzle
from mypy.nodes import TypeGuard

app = typer.Typer(no_args_is_help=True)


def get_current_aoc_year():
    """
    Returns the current year if the current month is December (and the new AOC started)
    or the previous year otherwise.
    """
    now = datetime.now()
    return now.year if now.month == 12 else now.year - 1


def echo(text, fg=typer.colors.GREEN):
    typer.echo(
        typer.style(
            text,
            fg=fg,
        )
    )


def import_challenge_module(day: int):
    module_name = f"aoc.day_{day:02}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        echo(
            f'Could not import "{e.name}"',
            fg=typer.colors.RED,
        )
        if e.name == module_name:
            echo(
                f"You have not solved day {day} yet. Start it using 'new-day' command",
                fg=typer.colors.RED,
            )
        else:
            raise e
        raise typer.Exit(1) from e
    return module


def run_challenge(day: int, test_data: bool):
    module = import_challenge_module(day)
    if test_data:
        module.Challenge(use_test_data=True).run()
    else:
        module.Challenge(use_test_data=False).run()


def get_puzzle_object(year: int, day: int) -> Puzzle | None:
    try:
        puzzle = Puzzle(year=year, day=day)
        return puzzle
    except AocdError:
        pass
    return None


def write_example_data(puzzle, test_input_data):
    try:
        test_input_data.write_text(puzzle.examples[0].input_data)
    except PuzzleLockedError:
        echo(
            "Failed writing test input data. Puzzle data is not available yet.",
            fg=typer.colors.YELLOW,
        )


def write_input_data(puzzle, real_input_data):
    try:
        real_input_data.write_text(puzzle.input_data)
    except PuzzleLockedError:
        echo(
            "Failed writing user input data. Puzzle data is not available yet.",
            fg=typer.colors.YELLOW,
        )


@app.command()
def run(
    day: int = typer.Argument(..., help="Day of the challenge to run."),
    test_data: bool = typer.Option(
        False, "--test-data", "-t", help="Run challenge also for test data."
    ),
):
    """Run the challenge."""
    run_challenge(day, test_data)


@app.command()
def verify(
    day: int | None = typer.Argument(None, help="Day of the challenge to verify."),
    part_one_only: bool = typer.Option(
        False, "--part-one", "-1", help="Verify only part one of the solution."
    ),
    part_two_only: bool = typer.Option(
        False, "--part-two", "-2", help="Verify only part two of the solution."
    ),
    sample_data_only: bool = typer.Option(
        False,
        "--test-data-only",
        "-t",
        help="Only run test on sample data. Usefull for debugging.",
    ),
):
    """Verify the challenge."""
    pytest_args = ["-W", "ignore:Module already imported"][:2]
    pytest_args = []
    if sample_data_only:
        pytest_args.extend(["-k", "sample_data"])
    if sum([part_one_only, part_two_only]) == 1:
        pytest_args.extend(["-k", "part_1" if part_one_only else "part_2"])
    if day is not None:
        module = import_challenge_module(day)
        if not module.__file__:
            typer.echo(
                typer.style(
                    "Impossible to run verification. "
                    "Probably you are in the interactive shell.",
                    fg=typer.colors.RED,
                )
            )
            raise typer.Exit(1)
        del locals()["module"]
        pytest_args.append(module.__path__[0])
        print(pytest_args)
    pytest.main(pytest_args)


def _check_type_of_part(part: str) -> TypeGuard[Literal["a", "b"]]:
    if part in ("a", "b"):
        return True
    return False


def _transform_part(part: str) -> str:
    if part in ("1", "2"):
        return chr(ord("a") + int(part) - 1)
    return part


def _full_validate(part: str) -> Literal["a", "b"]:
    part = _transform_part(part)
    if _check_type_of_part(part):
        return part

    typer.echo(
        typer.style(
            f"Invalid part {part}. Must be one of 1, 2, a, b.",
            fg=typer.colors.RED,
        )
    )
    raise typer.Exit(1)


@app.command()
def submit(
    day: int,
    year: int = typer.Option(
        get_current_aoc_year(),
        "--year",
        "-y",
        help="Year for which to submit the solution.",
    ),
    part: str = typer.Argument(
        help="Which part of the solution to submit. "
        "You can use numbers 1/2 or letters a/b."
    ),
):
    validated_part = _full_validate(part)
    module = import_challenge_module(day)
    if validated_part == "a":
        solution = module.Challenge(use_test_data=False).part_1()
    else:
        solution = module.Challenge(use_test_data=False).part_2()
    aocd.submit(solution, day=day, year=year, part=validated_part)


@app.command()
def new_day(
    day: Annotated[int, typer.Argument(help="Day for which to create a directory.")],
    year: Annotated[
        int,
        typer.Option(
            "-y",
            "--year",
            help="Year for which to get the puzzle data",
        ),
    ] = get_current_aoc_year(),
    directory: Annotated[
        Path,
        typer.Option(
            ...,
            "-d",
            "--directory",
            help="Path to a directory with challenges",
        ),
    ] = "src/aoc",
    data_directory: Annotated[
        Path,
        typer.Option(help="Path to a directory with data."),
    ] = "data",
    template_directory: Annotated[
        Path,
        typer.Option(
            "--template-directory",
            help="Path to a template directory for a single day challenge.",
        ),
    ] = Path(__file__).parent / "templates/day_template",
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Force creation of directory even if it already exists.",
        ),
    ] = False,
):
    """Create a directory for a new day challenge."""
    puzzle = get_puzzle_object(year, day)
    if day < 1 or day > 25:
        typer.echo(typer.style("Day must be between 1 and 25.", fg=typer.colors.RED))
        raise typer.Exit(1)
    destination = directory.joinpath(f"day_{day:02}")
    if destination.exists() and not force:
        typer.echo(
            typer.style(
                f"Day {day} already exists. Add -f flag if you want to overwrite",
                fg=typer.colors.RED,
            )
        )
        raise typer.Exit(1)
    shutil.copytree(template_directory, destination, dirs_exist_ok=force)
    typer.echo(
        typer.style(f"Created solution directory for day {day}.", fg=typer.colors.GREEN)
    )
    data_directory.mkdir(exist_ok=True)
    if (
        real_input_data := data_directory.joinpath(f"{day:02}_input.txt")
    ).exists() and real_input_data.stat().st_size:
        typer.echo(
            typer.style(
                f"Input data already exists for day {day}.", fg=typer.colors.YELLOW
            )
        )
    else:
        real_input_data.touch()
        if puzzle is not None:
            write_input_data(puzzle, real_input_data)
        typer.echo(
            typer.style(f"Created input data for day {day}.", fg=typer.colors.GREEN)
        )
    if (
        test_input_data := data_directory.joinpath(Path(f"{day:02}_test_input.txt"))
    ).exists() and test_input_data.stat().st_size:
        typer.echo(
            typer.style(
                f"Test input data already exists for day {day}.", fg=typer.colors.YELLOW
            )
        )
    else:
        test_input_data.touch()
        if puzzle is not None and puzzle.examples:
            write_example_data(puzzle, test_input_data)
        typer.echo(
            typer.style(
                f"Created test input data for day {day}.", fg=typer.colors.GREEN
            )
        )


if __name__ == "__main__":
    app()
