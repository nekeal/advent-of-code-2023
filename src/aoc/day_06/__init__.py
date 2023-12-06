import math
from functools import reduce
from operator import mul
from typing import Generator

from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    def part_1(self):
        times, distances = self.get_parsed_input(self.get_input_lines(part=1))
        winning_possibilities = []
        for time, distance in zip(times, distances):
            winning_numbers = list(self.get_winning_numbers(time, distance))
            winning_possibilities.append(len(list(winning_numbers)))
        return reduce(mul, winning_possibilities)

    def part_2(self):
        times, distances = self.get_parsed_input(self.get_input_lines(part=2))
        time = int("".join(map(str, times)))
        distance = int("".join(map(str, distances)))
        winning_possibilities = []
        winning_numbers = self.get_range_of_winning_numbers(time, distance)
        print("Winning numbers:", winning_numbers)
        winning_possibilities.append(winning_numbers[1] - winning_numbers[0] + 1)
        return reduce(mul, winning_possibilities)

    def get_parsed_input(self, lines: list[str]) -> tuple[list[int], list[int]]:
        return self.get_numbers_from_string(lines[0]), self.get_numbers_from_string(
            lines[1]
        )

    @staticmethod
    def get_numbers_from_string(string: str):
        return list(map(int, string.split(":")[1].split()))

    def get_winning_numbers(
        self, time: int, distance: int
    ) -> Generator[int, None, None]:
        for t in range(1, time):
            if (time - t) * t > distance:
                yield t

    @staticmethod
    def get_range_of_winning_numbers(time: int, distance: int) -> tuple[int, int]:
        root1, root2 = sorted(
            [
                (time + math.sqrt(time**2 - 4 * distance)) / 2,
                (time - math.sqrt(time**2 - 4 * distance)) / 2,
            ]
        )
        if int(root1) == root1:
            root1 += 1
        if int(root2) == root2:
            root2 -= 1
        return math.ceil(root1), math.floor(root2)


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
