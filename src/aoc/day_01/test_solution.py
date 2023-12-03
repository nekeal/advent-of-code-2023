from ..base_tests import BaseTestChallenge
from . import Challenge


class TestChallenge(BaseTestChallenge):
    challenge_class = Challenge
    expected_results_from_test_data = (142, 281)
    expected_results_from_real_data = (55017, 53539)
