from collections import Counter
from functools import partial
from pprint import pprint
from typing import Generator

from aoc.base import BaseChallenge

cards_to_values: dict[str, int] = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


class Challenge(BaseChallenge):
    def part_1(self):
        input_lines = self.get_input_lines(part=1)
        parsed_input = list(self.get_parsed_input(input_lines))
        sorted_values = sorted(
            parsed_input,
            key=partial(self.calculate_hand_value, cards_to_values=cards_to_values),
        )
        total_sum = 0
        for rank, (_, bid) in enumerate(sorted_values, 1):
            total_sum += bid * rank

        return total_sum

    def part_2(self):
        input_lines = self.get_input_lines(part=2)
        parsed_input = list(self.get_parsed_input(input_lines))
        cards_to_values_with_joker = cards_to_values.copy()
        cards_to_values_with_joker["J"] = 1
        sorted_values = sorted(
            parsed_input,
            key=partial(
                self.calculate_hand_value_with_jokers,
                cards_to_values=cards_to_values_with_joker,
            ),
        )
        total_sum = 0
        for rank, (hand, bid) in enumerate(sorted_values, 1):
            print(hand, bid, rank)
            total_sum += bid * rank

        return total_sum

    @staticmethod
    def calculate_hand_value(
        hand_and_bid: tuple[str, int], cards_to_values: dict[str, int]
    ) -> tuple[int, tuple[int, ...]]:
        hand, bid = hand_and_bid
        hand_by_numbers = tuple(cards_to_values[card] for card in hand)
        counts = Counter(hand_by_numbers)
        counts_set = set(counts.values())

        if 5 in counts_set:  # five of a kind
            return 7, hand_by_numbers
        elif 4 in counts_set:  # four of a kind
            return 6, hand_by_numbers
        elif counts_set.issuperset({3, 2}):  # full house
            return 5, hand_by_numbers
        elif 3 in counts_set:  # three of a kind
            return 4, hand_by_numbers
        elif list(counts.values()).count(2) == 2:  # two pairs
            return 3, hand_by_numbers
        elif 2 in counts_set:  # one pair
            return 2, hand_by_numbers
        else:  # high card
            return 1, hand_by_numbers

    def calculate_hand_value_with_jokers(
        self, hand_and_bid: tuple[str, int], cards_to_values: dict[str, int]
    ) -> tuple[int, tuple[int, ...]]:
        hand, bid = hand_and_bid
        hand_by_numbers = tuple(cards_to_values[card] for card in hand)
        initial_value = self.calculate_hand_value(
            (hand.replace("J", ""), bid), cards_to_values=cards_to_values
        )
        if not (joker_count := hand.count("J")):
            return initial_value[0], hand_by_numbers
        elif joker_count == 1:
            return min(
                min(initial_value[0] + 2, 2 * initial_value[0]), 7
            ), hand_by_numbers
        elif joker_count == 2:
            if initial_value[0] == 2:
                return initial_value[0] + 4, hand_by_numbers
            else:
                return initial_value[0] + 3, hand_by_numbers
        elif joker_count == 3:
            return initial_value[0] + 5, hand_by_numbers
        elif joker_count in [4, 5]:
            return 7, hand_by_numbers
        else:
            raise ValueError(f"Invalid number of jokers: {joker_count}")

    @staticmethod
    def get_parsed_input(
        input_lines: list[str]
    ) -> Generator[tuple[str, int], None, None]:
        for line in input_lines:
            hand, bid = line.split()
            yield hand, int(bid)


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
