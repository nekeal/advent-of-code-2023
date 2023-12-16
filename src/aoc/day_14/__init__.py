import functools
from collections import defaultdict
from pprint import pprint

from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    def part_1(self):
        simple_matrix = tuple(tuple(line) for line in self.get_input_lines(part=1))
        new_matrix = self.tilt2(simple_matrix)
        return self.score(new_matrix)

    def part_2(self):
        simple_matrix = tuple(tuple(line) for line in self.get_input_lines(part=2))
        pprint(simple_matrix)
        for _ in range(int(1e9 / 1e4)):
            simple_matrix = self.ten_thousand_cycles(simple_matrix)
        return self.score(simple_matrix)

    @functools.lru_cache(maxsize=None)  # noqa: B019
    def ten_thousand_cycles(self, matrix: tuple[tuple[str]]):
        for _ in range(10000):
            matrix = self.cycle(matrix)
        return matrix

    @functools.lru_cache(maxsize=None)  # noqa: B019
    def cycle(self, matrix: tuple[tuple[str]]):
        for _ in range(4):
            matrix = self.single_round(matrix)
        return matrix

    @functools.lru_cache(maxsize=None)  # noqa: B019
    def single_round(self, matrix: tuple[tuple[str]]):
        return self.rotate_90(self.tilt2(matrix))

    @functools.lru_cache(maxsize=None)  # noqa: B019
    def tilt2(self, matrix: tuple[tuple[str, ...], ...]):
        matrix_c = list(matrix)
        positions_per_row: dict[int, list[int]] = defaultdict(list)
        for c in range(len(matrix_c[0])):
            last_available_position = 0
            for r in range(len(matrix_c)):
                match matrix_c[r][c]:
                    case "O":
                        positions_per_row[last_available_position].append(c)
                        matrix_c[r] = tuple(
                            matrix_c[r][:c] + (".",) + matrix_c[r][c + 1 :]
                        )
                        matrix_c[last_available_position] = (
                            matrix_c[last_available_position][:c]
                            + ("O",)
                            + matrix_c[last_available_position][c + 1 :]
                        )
                        last_available_position += 1
                    case "#":
                        last_available_position = r + 1
                    case ".":
                        pass
        return tuple(matrix_c)

    @staticmethod
    @functools.lru_cache(maxsize=None)  # noqa: B019
    def rotate_90(matrix: tuple[tuple[str, ...], ...]) -> tuple[tuple[str, ...], ...]:
        return tuple(zip(*matrix[::-1]))

    @staticmethod
    def score(matrix: tuple[tuple[str, ...], ...]):
        return sum(
            len(matrix) - r
            for r in range(len(matrix))
            for c in range(len(matrix[0]))
            if matrix[r][c] == "O"
        )


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
