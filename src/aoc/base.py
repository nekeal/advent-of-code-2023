import abc
import logging
from pathlib import Path
from typing import Any

import __main__

REPO_ROOT = Path(__file__).parent.parent.parent
logger = logging.getLogger(__name__)


class BaseChallenge(abc.ABC):
    """Base class for all challenges."""

    def __init__(self, use_test_data: bool = False, data_dir: Path | None = None):
        self._use_test_data = use_test_data
        self._input_lines: dict[int | None, list[str]] = {}
        self._data_dir = data_dir or REPO_ROOT.joinpath("data")

    @property
    def day(self) -> int:
        """Return the day of this challenge based on the module name."""
        if self.__module__ == "__main__":  # challenge is run directly
            return int(Path(__main__.__file__).parent.name.split("_")[1])
        return int(self.__module__.split(".")[-1].split("_")[1])

    def get_input_filename(self, part: int | None = None) -> str:
        """Return the input filename for this challenge."""
        base_filename = (
            f"{self.day:02}_test_input"
            if self._use_test_data
            else f"{self.day:02}_input"
        )
        default_filename = f"{base_filename}.txt"
        if part is not None:
            filename = f"{base_filename}_part_{part}.txt"
            if self._data_dir.joinpath(filename).exists():
                return filename
            else:
                logger.info(
                    "File %s does not exist. Using default instead %s",
                    filename,
                    default_filename,
                )
        return default_filename

    def get_input_file_path(self, filename: str) -> Path:
        """Return the input filename for this challenge."""
        return self._data_dir.joinpath(filename)

    def get_input_lines(self, part: int | None = None) -> list[str]:
        """Return the input lines for this challenge. Relative to this file"""
        filename = self.get_input_filename(part)
        print(f"Using data from {filename}")
        if not self._input_lines.get(part):
            self._input_lines[part] = (
                self.get_input_file_path(filename).read_text().splitlines()
            )
        return self._input_lines[part]

    def set_input_lines(self, lines: list[str], part: int | None = None):
        self._input_lines[part] = lines

    @abc.abstractmethod
    def part_1(self) -> Any:
        """Return the solution for part 1 of this challenge."""
        ...

    @abc.abstractmethod
    def part_2(self) -> Any:
        """Return the solution for part 2 of this challenge."""
        ...

    def solve(self) -> tuple[Any, Any]:
        """Return solutions for this challenge as a 2 element tuple."""
        return self.part_1(), self.part_2()

    def run(self):
        solution1 = self.part_1()
        print(f"Day {self.day} - Part 1: {solution1}")
        solution2 = self.part_2()
        print(f"Day {self.day} - Part 2: {solution2}\n")
        return solution1, solution2
