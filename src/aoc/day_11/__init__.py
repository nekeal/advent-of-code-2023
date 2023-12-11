from itertools import accumulate, combinations

from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    def part_1(self):
        input_lines = self.get_input_lines(part=1)
        total_sum = 0
        for pair in combinations(
            self.get_galaxies_coords(input_lines, expansion_multiplier=2), 2
        ):
            total_sum += abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
        return total_sum

    def part_2(self):
        input_lines = self.get_input_lines(part=1)
        total_sum = 0
        for pair in combinations(
            self.get_galaxies_coords(input_lines, expansion_multiplier=1000000), 2
        ):
            total_sum += abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
        return total_sum

    def get_galaxies_coords(
        self, input_lines, expansion_multiplier
    ) -> list[tuple[int, int]]:
        empty_columns = [
            expansion_multiplier - 1
            if all(row[column] == "." for row in input_lines)
            else 0
            for column in range(len(input_lines[0]))
        ]
        empty_rows = [
            expansion_multiplier - 1
            if all(char == "." for char in input_lines[row])
            else 0
            for row in range(len(input_lines))
        ]
        prefix_for_columns = list(accumulate(empty_columns))
        prefix_for_rows = list(accumulate(empty_rows))
        print("cols", empty_columns)
        print("rows", empty_rows)
        print("prefix cols", list(prefix_for_columns))
        print("prefix rows", list(prefix_for_rows))
        galaxies = []
        for y, line in enumerate(input_lines):
            for x, char in enumerate(line):
                if char == "#":
                    galaxies.append((x + prefix_for_columns[x], y + prefix_for_rows[y]))
        return galaxies


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
