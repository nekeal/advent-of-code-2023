from aoc.base_tests import BaseTestChallenge

from . import Challenge


class TestChallenge(BaseTestChallenge):
    challenge_class = Challenge
    expected_results_from_test_data = (2, 47)
    expected_results_from_real_data = (18098, 886858737029295)
