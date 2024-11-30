from typing import Any

import pytest

from aoc.base import BaseChallenge
from aoc.input_providers import SmartFileInputProvider


class Empty:
    """A class to represent a value that is not set."""


class BaseTestChallenge:
    challenge_class: type[BaseChallenge]
    expected_results_from_test_data: tuple[Any, Any] = (Empty, Empty)
    expected_results_from_real_data: tuple[Any, Any] = (Empty, Empty)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "challenge_class"):
            raise ValueError(
                f"You must define a challenge_class attribute on class {cls.__name__}."
            )
        if (
            not isinstance(cls.expected_results_from_test_data, tuple)
            or len(cls.expected_results_from_test_data) != 2
        ):
            raise ValueError(
                "expected_results_from_test_data must be a tuple of 2 elements."
            )

        if (
            not isinstance(cls.expected_results_from_real_data, tuple)
            or len(cls.expected_results_from_real_data) != 2
        ):
            raise ValueError(
                "expected_results_from_real_data must be a tuple of 2 elements."
            )

    def test_on_sample_data_part_1(self):
        if (expected_result := self.expected_results_from_test_data[0]) == Empty:
            pytest.skip("No expected result for part one of test data set.")

        challenge = self.challenge_class(
            SmartFileInputProvider(
                self.challenge_class.year, self.challenge_class.day, use_test_data=True
            )
        )
        assert challenge.part_1(challenge.get_input_lines(part=1)) == expected_result

    def test_on_sample_data_part_2(self):
        if (expected_result := self.expected_results_from_test_data[1]) == Empty:
            pytest.skip("No expected results for part two of test data set.")
        challenge = self.challenge_class(
            SmartFileInputProvider(
                self.challenge_class.year, self.challenge_class.day, use_test_data=True
            )
        )
        assert challenge.part_2(challenge.get_input_lines(part=2)) == expected_result

    def test_on_real_data_part_1(self):
        if (expected_result := self.expected_results_from_real_data[0]) == Empty:
            pytest.skip("No expected result for part one of real data set.")
        challenge = self.challenge_class(
            SmartFileInputProvider(self.challenge_class.year, self.challenge_class.day)
        )
        assert challenge.part_1(challenge.get_input_lines(part=1)) == expected_result

    def test_on_real_data_part_2(self):
        if (expected_result := self.expected_results_from_real_data[1]) == Empty:
            pytest.skip("No expected results for part two of real data set.")
        challenge = self.challenge_class(
            SmartFileInputProvider(self.challenge_class.year, self.challenge_class.day)
        )
        assert challenge.part_2(challenge.get_input_lines(part=2)) == expected_result
