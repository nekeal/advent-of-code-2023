import operator
from functools import reduce
from typing import Generator

from aoc.base import BaseChallenge
from aoc.data_structures import Matrix


class MirrorMatrix(Matrix):
    def find_mirrors(self, smudges: int) -> Generator[int, None, None]:
        for c in range(self.width - 1):
            badness = 0
            for dc in range(min(c + 1, self.width - c - 1)):
                for r in range(self.height):
                    badness += self.matrix[r][c - dc] != self.matrix[r][c + dc + 1]
            if badness == smudges:
                yield c + 1
        for r in range(self.height - 1):
            badness = 0
            for dr in range(min(r + 1, self.height - r - 1)):
                for c in range(self.width):
                    badness += self.matrix[r - dr][c] != self.matrix[r + dr + 1][c]
            if badness == smudges:
                yield (r + 1) * 100


class Challenge(BaseChallenge):
    def part_1(self):
        return reduce(
            operator.add,
            (
                val
                for matrix in self.get_matrixes(part=1)
                for val in matrix.find_mirrors(smudges=0)
            ),
        )

    def part_2(self):
        return reduce(
            operator.add,
            (
                val
                for matrix in self.get_matrixes(part=2)
                for val in matrix.find_mirrors(smudges=1)
            ),
        )

    def get_matrixes(self, part) -> Generator[MirrorMatrix, None, None]:
        yield from (
            MirrorMatrix(matrix.splitlines())
            for matrix in "\n".join(self.get_input_lines(part=part)).split("\n\n")
        )


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
