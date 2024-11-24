import sys
from pathlib import Path

from aoc.base import BaseChallenge
from aoc.input_providers import SingleFileInputProvider, SmartFileInputProvider


class Challenge(BaseChallenge):
    """Base class for all challenges."""

    def part_1(self, input_lines: list[str]) -> int | str:
        return int(all(input_lines))

    def part_2(self, input_lines: list[str]) -> int | str:
        print(input_lines)
        return sum(map(int, input_lines))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_provider = SingleFileInputProvider(
            Challenge.day, input_path=Path(sys.argv[1])
        )
        Challenge(input_provider).run()
    else:
        Challenge(SmartFileInputProvider(Challenge.day, use_test_data=True)).run()
        Challenge(SmartFileInputProvider(Challenge.day)).run()
