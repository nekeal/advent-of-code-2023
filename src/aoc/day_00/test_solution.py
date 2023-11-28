from ..base import BaseTestChallenge
from . import Challenge


class TestChallenge(BaseTestChallenge):
    challenge_class = Challenge
    expected_results_from_test_data = (1, 10)
    expected_results_from_real_data = (1, 55)
