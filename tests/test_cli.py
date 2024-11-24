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


class TestRunningSolution:
    def test_run_for_a_specific_day_with_default_data(self, tmp_path: Path):
        result = runner.invoke(
            app,
            [
                "run",
                "0",
            ],
        )
        if result.exception:
            raise result.exception
        assert result.exit_code == 0, result.exc_info
        assert "Day 0 - Part 1: 1" in result.stdout
        assert "Day 0 - Part 2: 55" in result.stdout

    def test_run_for_a_specific_day_with_test_data(self, tmp_path: Path):
        result = runner.invoke(
            app,
            [
                "run",
                "0",
                "-t",
            ],
        )
        if result.exception:
            raise result.exception
        assert result.exit_code == 0, result.exc_info
        assert "00_test_input.txt" in result.stdout
        assert "Day 0 - Part 1: 1" in result.stdout
        assert "Day 0 - Part 2: 21" in result.stdout

    def test_run_for_a_specific_day_with_a_custom_file(self, tmp_path: Path):
        result = runner.invoke(
            app,
            [
                "run",
                "0",
                "-f",
                Path(__file__).parent / "data/custom_input.txt",
            ],
        )
        if result.exception:
            raise result.exception
        assert result.exit_code == 0, result.exc_info
        assert "Using data from custom_input.txt" in result.stdout
        assert "Day 0 - Part 1: 1" in result.stdout
        assert "Day 0 - Part 2: 33" in result.stdout
