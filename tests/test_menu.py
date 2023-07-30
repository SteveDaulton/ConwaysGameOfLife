"""Tests for menu.py"""

from unittest.mock import patch

import pytest

from game_of_life.custom_types import Preset
from game_of_life.menu import display_menu


@pytest.mark.parametrize(
    "test_settings,expected_output",[
        # Empty list of Presets will print nothing.
        ([], ''),
        # List of one preset
        ([Preset(0, 'Preset name', set())], '0. Preset name'),
        # Multiple presets
        ([Preset(0, 'First', set()),
          Preset(1, 'Second', set()),
          Preset(2, 'Third', set())],
         '0. First\n1. Second\n2. Third')])
def test_display_menu_with_fixture(capsys, test_settings, expected_output) -> None:
    """Test menu.display_menu with  fixtures."""
    with patch('game_of_life.menu.get_all_presets') as mock_get_all_presets:
        mock_get_all_presets.return_value = test_settings
        display_menu()
        captured = capsys.readouterr()
        assert captured.err == ''
        assert captured.out.strip() == expected_output


def test_display_menu_with_presets(capsys) -> None:
    """Test menu display with actual Presets.

    Expected output of each printed line in the form:
    integer dot space name_string.
    The final line(s) may be empty.

    Examples
    --------
        Printed line => '2. Beacon'
    """
    display_menu()
    captured = capsys.readouterr()
    # Check 1: no error strings.
    assert captured.err == ''
    # Check 2: Correctly formatted strings
    assert captured.out != ''
    out = captured.out.strip()
    for line in out.split('\n'):
        # Line should have two parts: 'index. name'.
        # `name` may be any non-empty string
        try:
            idx_str, _ = line.split(' ', 1)
            assert idx_str[:-1].isnumeric()
            assert idx_str[-1] == '.'
        except ValueError as exc:
            raise AssertionError(f"Unexpected format in line: '{line}'") from exc
