from collections import defaultdict
from pprint import pprint

from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    @staticmethod
    def parse_line(line: str) -> tuple[list[int], list[int]]:
        numbers_str = line.split(":")[1]
        winning_numbers_str, got_numbers_str = numbers_str.split("|")

        return list(map(int, winning_numbers_str.split())), list(
            map(int, got_numbers_str.split())
        )

    @staticmethod
    def get_score(winning_numbers: list[int], got_numbers: list[int]) -> int:
        return len(set(winning_numbers) & set(got_numbers))

    def part_1(self):
        total_sum = 0
        for line in self.get_input_lines(part=1):
            parsed_line = self.parse_line(line)
            if score := self.get_score(parsed_line[0], parsed_line[1]):
                total_sum += 2 ** (score - 1)
        return total_sum

    def part_2(self):
        number_of_cards: dict[int, int] = defaultdict(lambda: 1)
        for i, line in enumerate(self.get_input_lines(part=2)):
            number_of_cards.setdefault(i, 1)
            parsed_line = self.parse_line(line)
            score = self.get_score(parsed_line[0], parsed_line[1])
            for j in range(i + 1, i + 1 + score):
                number_of_cards[j] += number_of_cards[i]
        return sum(number_of_cards.values())


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
