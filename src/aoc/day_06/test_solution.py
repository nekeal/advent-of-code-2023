from aoc.base_tests import BaseTestChallenge, Empty

from . import Challenge


class TestChallenge(BaseTestChallenge):
    challenge_class = Challenge
    expected_results_from_test_data = (288, Empty)
    expected_results_from_real_data = (Empty, Empty)
