import abc
import inspect
from pathlib import Path
from typing import Any, ClassVar

from typing_extensions import Protocol

from aoc.input_providers import InputProvider

REPO_ROOT = Path(__file__).parent.parent.parent


def get_day_from_module(module_name: str) -> int:
    """Return the day of this challenge based on the module name."""
    return int(module_name.split(".")[-1].split("_")[1])


class ChallengeProtocol(Protocol):
    def part_1(self, input_lines: list[str]) -> Any: ...

    def part_2(self, input_lines: list[str]) -> Any: ...


class BaseChallenge(ChallengeProtocol, abc.ABC):
    """Base class for all challenges."""

    year: ClassVar[int]
    day: ClassVar[int]

    def __init__(
        self,
        input_provider: InputProvider,
    ):
        self._input_provider = input_provider
        self._input_lines: dict[int | None, list[str]] = {}

    def __init_subclass__(cls, **kwargs):
        cls.year = cls._get_year()
        cls.day = cls._get_day()

    @classmethod
    def _get_day(cls) -> int:
        import __main__

        """Return the day of this challenge based on the module name."""
        if cls.__module__ == "__main__":  # challenge is run directly
            return int(Path(__main__.__file__).parent.name.split("_")[1])
        return get_day_from_module(cls.__module__)

    @classmethod
    def _get_year(cls) -> int:
        import __main__

        """Return the year of this challenge based on the module name."""
        if cls.__module__ == "__main__":  # challenge is run directly
            return int(Path(__main__.__file__).parent.parent.name)
        # when running pytest it doesn't see parent module name due to relative import
        path_to_class = Path(inspect.getfile(cls))
        return int(path_to_class.parent.parent.name)

    def get_input_lines(self, part: int | None = None) -> list[str]:
        """Return the input lines for this challenge. Relative to this file"""
        if not self._input_lines.get(part):
            self._input_lines[part] = (
                self._input_provider.provide_input(part).strip().split("\n")
            )
        return self._input_lines[part]

    def set_input_lines(self, lines: list[str], part: int | None = None):
        self._input_lines[part] = lines

    @abc.abstractmethod
    def part_1(self, input_lines: list[str]) -> Any:
        """Return the solution for part 1 of this challenge."""
        ...

    @abc.abstractmethod
    def part_2(self, input_lines: list[str]) -> Any:
        """Return the solution for part 2 of this challenge."""
        ...

    def solve(self) -> tuple[Any, Any]:
        """Return solutions for this challenge as a 2 element tuple."""
        return self.part_1(self.get_input_lines(part=1)), self.part_2(
            self.get_input_lines(part=2)
        )

    def run(self):
        solution1 = self.part_1(self.get_input_lines(part=1))
        print(f"Day {self.day} - Part 1: {solution1}")
        solution2 = self.part_2(self.get_input_lines(part=2))
        print(f"Day {self.day} - Part 2: {solution2}\n")
        return solution1, solution2
