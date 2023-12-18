from aoc.base_tests import BaseTestChallenge

from . import Challenge


class TestChallenge(BaseTestChallenge):
    challenge_class = Challenge
    expected_results_from_test_data = (62, 952408144115)
    expected_results_from_real_data = (36679, 88007104020978)
