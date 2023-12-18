"""
This file unittests the main.py file
"""
from click.testing import CliRunner

from src import main


def test_entry_point_pass():
    """
    Should run and pass without errors
    """
    runner = CliRunner()
    result = runner.invoke(main.entry_point)

    assert result.exit_code == 0
