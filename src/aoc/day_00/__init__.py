from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    """Base class for all challenges."""

    def part_1(self) -> int | str:
        return int(all(self.get_input_lines(part=1)))

    def part_2(self) -> int | str:
        return sum(map(int, self.get_input_lines(part=2)))


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
