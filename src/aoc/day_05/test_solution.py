import pytest

from aoc.base_tests import BaseTestChallenge

from . import Challenge, Range


class TestChallenge(BaseTestChallenge):
    challenge_class = Challenge
    expected_results_from_test_data = (35, 46)
    expected_results_from_real_data = (600279879, 20191102)

    @pytest.mark.parametrize(
        ("range1", "range2", "expected"),
        (
            (Range(0, 1), Range(2, 3), False),
            (Range(0, 1), Range(1, 2), True),
            (Range(0, 2), Range(1, 2), True),
            (Range(0, 2), Range(1, 1), True),
            (Range(0, 2), Range(3, 4), False),
        ),
    )
    def test_range_overlaps(self, range1, range2, expected):
        assert range1.overlaps(range2) == expected

    @pytest.mark.parametrize(
        ("range1", "range2", "expected"),
        (
            (Range(0, 3), Range(2, 3), [Range(0, 1)]),
            (Range(0, 3), Range(2, 3), [Range(0, 1)]),
            (Range(0, 3), Range(2, 4), [Range(0, 1)]),
            (Range(0, 3), Range(1, 2), [Range(0, 0), Range(3, 3)]),
            (Range(0, 4), Range(2, 2), [Range(0, 1), Range(3, 4)]),
        ),
    )
    def test_range_split(self, range1, range2, expected):
        assert range1.diff(range2) == expected
