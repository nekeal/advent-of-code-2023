import abc
from pathlib import Path
from typing import Any

import __main__
import pytest

REPO_ROOT = Path(__file__).parent.parent.parent


class BaseChallenge(abc.ABC):
    """Base class for all challenges."""

    def __init__(self, use_test_data: bool = False, data_dir: Path | None = None):
        self._use_test_data = use_test_data
        self._input_lines: list[str] | None = None
        self._data_dir = data_dir or REPO_ROOT.joinpath("data")

    @property
    def day(self) -> int:
        """Return the day of this challenge based on the module name."""
        if self.__module__ == "__main__":  # challenge is run directly
            return int(Path(__main__.__file__).parent.name.split("_")[1])
        return int(self.__module__.split(".")[-1].split("_")[1])

    @property
    def input_filename(self) -> str:
        """Return the input filename for this challenge."""
        return (
            f"{self.day:02}_input.txt"
            if not self._use_test_data
            else f"{self.day:02}_test_input.txt"
        )

    @property
    def input_file_path(self) -> Path:
        """Return the input filename for this challenge."""
        return self._data_dir.joinpath(self.input_filename)

    def input_lines(self) -> list[str]:
        """Return the input lines for this challenge. Relative to this file"""
        if not self._input_lines:
            self._input_lines = self.input_file_path.read_text().splitlines()
        return self._input_lines

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
        solution1, solution2 = self.solve()
        print(f"Using data from {self.input_filename}")
        print(f"Day {self.day} - Part 1: {self.part_1()}")
        print(f"Day {self.day} - Part 2: {self.part_2()}\n")
        return solution1, solution2


class NotSet:
    """A class to represent a value that is not set."""


class BaseTestChallenge:
    challenge_class: type[BaseChallenge]
    expected_results_from_test_data: tuple[Any, Any] = (NotSet, NotSet)
    expected_results_from_real_data: tuple[Any, Any] = (NotSet, NotSet)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "challenge_class"):
            raise ValueError(
                f"You must define a challenge_class attribute on class {cls.__name__}."
            )
        if (
            not isinstance(cls.expected_results_from_test_data, tuple)
            or len(cls.expected_results_from_test_data) != 2
        ):
            raise ValueError(
                "expected_results_from_test_data must be a tuple of 2 elements."
            )

        if (
            not isinstance(cls.expected_results_from_real_data, tuple)
            or len(cls.expected_results_from_real_data) != 2
        ):
            raise ValueError(
                "expected_results_from_real_data must be a tuple of 2 elements."
            )

    def test_on_sample_data_part_1(self):
        if (expected_result := self.expected_results_from_test_data[0]) == NotSet:
            pytest.skip("No expected result for part one of test data set.")
        assert self.challenge_class(use_test_data=True).part_1() == expected_result

    def test_on_sample_data_part_2(self):
        if (expected_result := self.expected_results_from_test_data[1]) == NotSet:
            pytest.skip("No expected results for part two of test data set.")
        assert self.challenge_class(use_test_data=True).part_2() == expected_result

    def test_on_real_data_part_1(self):
        if (expected_result := self.expected_results_from_real_data[0]) == NotSet:
            pytest.skip("No expected result for part one of real data set.")
        assert self.challenge_class().part_1() == expected_result

    def test_on_real_data_part_2(self):
        if (expected_result := self.expected_results_from_real_data[1]) == NotSet:
            pytest.skip("No expected results for part two of real data set.")
        assert self.challenge_class().part_2() == expected_result
