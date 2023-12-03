from collections import defaultdict
from functools import reduce
from operator import mul

from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    def part_1(self):
        """
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
        :return:
        """
        limit = (12, 13, 14)
        result = 0
        for game_id, line in enumerate(self.get_input_lines(part=1), 1):
            parsed_game = self.parse_game(line)
            if all(
                round_result[color_id] <= limit[color_id]
                for round_result in parsed_game
                for color_id in range(3)
            ):
                result += game_id
        return result

    def part_2(self):
        result = 0

        for line in self.get_input_lines(part=2):
            parsed_game = self.parse_game(line)
            minimal_set = self.get_minimal_set(parsed_game)
            # multiply elements of minimal set
            result += reduce(mul, minimal_set, 1)
        return result

    def parse_game(self, line) -> list[tuple[int, ...]]:
        """
        sample line: "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
        :param line: game's line
        :return: parsed game as a list of tuples using match case
        """
        colors_line = line.split(":")[1].strip()
        rounds_colors_unparsed = colors_line.split(";")
        result: list[tuple[int, ...]] = []
        for round_colors_unparsed in rounds_colors_unparsed:
            round_colors = [str(x.strip()) for x in round_colors_unparsed.split(",")]
            result.append(self.parse_round(round_colors))
        return result

    def parse_round(self, round_colors: list[str]) -> tuple[int, ...]:
        """
        sample round_colors: "3 blue, 4 red"
        :param round_colors:
        :return: three elements tuple: (red, green, blue)
        """
        result = defaultdict(int)
        for number_and_color in round_colors:
            number, color = number_and_color.split(" ")
            result[color] = int(number)
        return tuple(result[color] for color in ("red", "green", "blue"))

    def parse_game_colors(self, game_colors):
        pass

    def get_minimal_set(self, parsed_game: list[tuple[int, ...]]) -> tuple[int, ...]:
        """
        Finds the minimal set of colors that can be used to play the game.
        :param parsed_game:
        :return:
        """
        maximums: dict[int, int] = defaultdict(int)
        for round_result in parsed_game:
            for color_id in range(3):
                maximums[color_id] = max(maximums[color_id], round_result[color_id])
        return tuple(maximums[color_id] for color_id in range(3))


if __name__ == "__main__":
    Challenge(use_test_data=True).run()
    Challenge().run()
