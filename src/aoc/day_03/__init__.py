import string
from collections import defaultdict
from operator import mul
from pprint import pprint

from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    @staticmethod
    def iter_neighbors(matrix: list[str], x: int, y: int):
        """
        Iter over neighbors of a cell considering the matrix borders
        :param matrix:
        :param x:
        :param y:
        :return:
        """
        for i in range(max(0, x - 1), min(len(matrix), x + 2)):
            for j in range(max(0, y - 1), min(len(matrix[i]), y + 2)):
                if i == x and j == y:
                    continue
                yield i, j, matrix[i][j]

    def check_if_symbol_is_neighbor(self, matrix: list[str], x: int, y: int):
        for i, j, _ in self.iter_neighbors(matrix, x, y):
            if matrix[i][j] not in [".", *string.digits]:
                return True
        return False

    def part_2(self):
        tmp_number: str = ""
        matrix = self.get_input_lines(part=1)
        stars_neighbours = defaultdict(list)
        current_stars: set[tuple[int, int]] = set()
        total_sum = 0
        for line_number, line in enumerate(matrix):
            for character_number, character in enumerate(line):
                match character:
                    case number if number.isdigit():
                        tmp_number += number
                        for x, y, _ in filter(
                            lambda cell: cell[2] == "*",
                            self.iter_neighbors(matrix, line_number, character_number),
                        ):
                            current_stars.add((x, y))
                    case _:
                        if current_stars:
                            for star in current_stars:
                                stars_neighbours[star].append(int(tmp_number))
                            current_stars.clear()
                        tmp_number = ""
        pprint(stars_neighbours)
        for _, neighbours in stars_neighbours.items():
            if len(neighbours) == 2:
                total_sum += mul(*neighbours)
        return total_sum

    def part_1(self):
        tmp_number: str = ""
        neighbour_to_symbol = False
        matrix = self.get_input_lines(part=1)
        to_sum = []

        for line_number, line in enumerate(matrix):
            for character_number, character in enumerate(line):
                match character:
                    case number if number.isdigit():
                        tmp_number += number
                        neighbour_to_symbol = (
                            neighbour_to_symbol
                            or self.check_if_symbol_is_neighbor(
                                matrix, line_number, character_number
                            )
                        )
                    case _:
                        if neighbour_to_symbol:
                            to_sum.append(int(tmp_number))
                        neighbour_to_symbol = False
                        tmp_number = ""
        return sum(to_sum)


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
