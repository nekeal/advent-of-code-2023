from aoc.base_tests import BaseTestChallenge

from . import Challenge


class TestChallenge(BaseTestChallenge):
    challenge_class = Challenge
    expected_results_from_test_data = (8, 2286)
    expected_results_from_real_data = (2720, 71535)
