from pathlib import Path
from unittest import mock

import pytest
from aoc.main import app
from aocd.models import Puzzle
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(autouse=True)
def m_aocd_puzzle(monkeypatch):
    m_puzzle = mock.Mock(spec=Puzzle)
    m_puzzle.input_data = "1"
    m_puzzle.examples = [mock.Mock(input_data="2")]
    monkeypatch.setattr("aoc.main.get_puzzle_object", mock.Mock(return_value=m_puzzle))
    return m_puzzle


class TestSettingUpNewDay:
    def test_setting_up_new_day_creates_directories_in_configured_places(
        self, tmp_path: Path
    ):
        result = runner.invoke(
            app,
            [
                "new-day",
                "11",
                "--data-directory",
                str(tmp_path / "data"),
                "--directory",
                str(tmp_path / "src"),
            ],
        )
        if result.exception:
            raise result.exception
        assert result.exit_code == 0, result.exc_info

        assert (tmp_path / "data" / "11_input.txt").read_text() == "1"
        assert (tmp_path / "data" / "11_test_input.txt").read_text() == "2"
        assert (tmp_path / "src" / "day_11").exists()
