import importlib
import shutil
from pathlib import Path
from typing import Optional

import pytest
import typer

app = typer.Typer(no_args_is_help=True)


def import_challenge_module(day: int):
    try:
        module = importlib.import_module(f"aoc.day_{day:02}")
    except ModuleNotFoundError as e:
        typer.echo(
            typer.style(
                f'You have not solved day {day} yet. Start it using "new-day" command',
                fg=typer.colors.RED,
            )
        )
        raise typer.Exit(1) from e
    return module


def run_challenge(day: int, test_data: bool):
    module = import_challenge_module(day)
    if test_data:
        module.Challenge(use_test_data=True).run()
    module.Challenge(use_test_data=False).run()


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
    day: Optional[int] = typer.Argument(None, help="Day of the challenge to verify."),
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
        pytest_args.append(module.__file__)
    print(pytest_args)
    pytest.main(pytest_args)


@app.command()
def new_day(
    day: int = typer.Argument(help="Day for which to create a directory."),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force creation of directory even if it already exists.",
    ),
):
    """Create a directory for a new day challenge."""
    if day < 1 or day > 25:
        typer.echo(typer.style("Day must be between 1 and 25.", fg=typer.colors.RED))
        raise typer.Exit(1)
    destination = Path(f"src/aoc/day_{day:02}")
    if destination.exists() and not force:
        typer.echo(
            typer.style(
                f"Day {day} already exists. Add -f flag if you want to ovewrite",
                fg=typer.colors.RED,
            )
        )
        raise typer.Exit(1)
    shutil.copytree(
        "templates/day_template", f"src/aoc/day_{day:02}", dirs_exist_ok=force
    )
    typer.echo(
        typer.style(f"Created solution directory for day {day}.", fg=typer.colors.GREEN)
    )
    if (real_input_data := Path(f"data/{day:02}_input.txt")).exists():
        typer.echo(
            typer.style(
                f"Input data already exists for day {day}.", fg=typer.colors.YELLOW
            )
        )
    else:
        real_input_data.touch()
        typer.echo(
            typer.style(f"Created input data for day {day}.", fg=typer.colors.GREEN)
        )
    real_input_data.touch()
    if (test_input_data := Path(f"data/{day:02}_test_input.txt")).exists():
        typer.echo(
            typer.style(
                f"Test input data already exists for day {day}.", fg=typer.colors.YELLOW
            )
        )
    else:
        test_input_data.touch()
        typer.echo(
            typer.style(
                f"Created test input data for day {day}.", fg=typer.colors.GREEN
            )
        )


if __name__ == "__main__":
    app()
