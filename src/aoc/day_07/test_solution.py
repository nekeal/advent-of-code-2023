import pytest

from aoc.base_tests import BaseTestChallenge

from . import Challenge, cards_to_values


class TestChallenge(BaseTestChallenge):
    challenge_class = Challenge
    expected_results_from_test_data = (6440, 5905)
    expected_results_from_real_data = (252052080, 252898370)

    @pytest.mark.parametrize(
        "hand,expected_result",
        (
            ("AAAAA", (7, (14, 14, 14, 14, 14))),
            ("AA8AA", (6, (14, 14, 8, 14, 14))),
            ("23332", (5, (2, 3, 3, 3, 2))),
            ("TTT98", (4, (10, 10, 10, 9, 8))),
            ("23432", (3, (2, 3, 4, 3, 2))),
            ("A23A4", (2, (14, 2, 3, 14, 4))),
            ("23456", (1, (2, 3, 4, 5, 6))),
        ),
    )
    def test_calculate_hand_value(self, hand, expected_result):
        assert (
            self.challenge_class.calculate_hand_value(
                (hand, 0), cards_to_values=cards_to_values
            )
            == expected_result
        ), hand

    @pytest.mark.parametrize(
        "hand, expected_result",
        (
            ("AAAAA", 7),
            ("AA8AA", 6),
            ("23332", 5),
            ("TTT98", 4),
            ("23432", 3),
            ("A23A4", 2),
            ("23456", 1),
            # single joker
            ("AKQTJ", 2),
            ("AAKTJ", 4),
            ("AAKKJ", 5),
            ("AAAKJ", 6),
            ("AAAAJ", 7),
            ("654JJ", 4),
            ("227JJ", 6),
            ("222JJ", 7),
            ("23JJJ", 6),
            ("22JJJ", 7),
            ("2JJJJ", 7),
            ("JJJJJ", 7),
        ),
    )
    def test_calculate_hand_value_with_jokers(self, hand, expected_result):
        assert (
            self.challenge_class().calculate_hand_value_with_jokers(
                (hand, 0), cards_to_values=cards_to_values
            )[0]
            == expected_result
        ), hand
