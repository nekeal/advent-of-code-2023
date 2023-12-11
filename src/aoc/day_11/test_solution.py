from aoc.base_tests import BaseTestChallenge

from . import Challenge


class TestChallenge(BaseTestChallenge):
    challenge_class = Challenge
    expected_results_from_test_data = (374, 82000210)
    expected_results_from_real_data = (9627977, 644248339497)
