from aoc.base_tests import BaseTestChallenge

from . import Challenge


class TestChallenge(BaseTestChallenge):
    challenge_class = Challenge
    expected_results_from_test_data = (6, 6)
    expected_results_from_real_data = (17263, 14631604759649)
