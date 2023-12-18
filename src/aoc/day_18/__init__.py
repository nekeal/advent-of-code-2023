import itertools
from functools import wraps
from typing import Iterable, TypeVar

from aoc.base import BaseChallenge

vec_map_str = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1),
}

vec_map_int = {
    0: (1, 0),
    1: (0, 1),
    2: (-1, 0),
    3: (0, -1),
}
T = TypeVar("T")


class Challenge(BaseChallenge):
    @staticmethod
    def get_vertices(
        instructions: Iterable[tuple[T, int]],
        vec_map: dict[T, tuple[int, int]],
    ):
        x, y = 0, 0
        for direction, length in instructions:
            x += vec_map[direction][0] * length
            y += vec_map[direction][1] * length
            yield x, y

    def part_1(self):
        vertices = self.get_vertices(
            (
                (line.split()[0], int(line.split()[1]))
                for line in self.get_input_lines(part=1)
            ),
            vec_map_str,
        )
        return self.calc_inners(vertices)

    def part_2(self):
        vertices = self.get_vertices(
            (
                self.parse_hex(line.split()[2].strip("()"))
                for line in self.get_input_lines(part=2)
            ),
            vec_map_int,
        )
        return self.calc_inners(vertices)

    @staticmethod
    def calc_inners(vertices):
        area = 0
        boundary_count = 0
        for v1, v2 in itertools.pairwise(itertools.chain(((0, 0),), vertices)):
            area += (v1[0] * v2[1] - v2[0] * v1[1]) / 2
            boundary_count += abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])
        return int(area + boundary_count / 2 + 1)  # pick's theorem

    @staticmethod
    def parse_hex(hex_str: str) -> tuple[int, int]:
        """
        :param hex_str: instruction in hex i.e #70c710
        :return: Tuple of (direction, length)
        """
        return int(hex_str[6:], 16), int(hex_str[1:6], 16)


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
