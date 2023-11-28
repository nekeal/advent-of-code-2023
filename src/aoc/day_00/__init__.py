from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    """Base class for all challenges."""

    def part_1(self) -> int | str:
        return int(all(self.input_lines()))

    def part_2(self) -> int | str:
        return sum(map(int, self.input_lines()))


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
