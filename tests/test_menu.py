"""Tests for menu.py"""

from unittest.mock import patch
import pytest

from game_of_life.custom_types import Preset
from game_of_life.menu import (preset_menu,
                               get_user_preset_choice,
                               refresh_rate_menu,
                               get_user_refresh_rate)
from game_of_life.custom_types import Defaults, Size


@pytest.mark.parametrize(
    "test_settings,expected_output", [
        # Empty list of Presets will print nothing.
        ([], ''),
        # List of one preset
        ([Preset(0, 'Preset name', set())], '0. Preset name'),
        # Multiple presets
        ([Preset(0, 'First', set()),
          Preset(1, 'Second', set()),
          Preset(2, 'Third', set())],
         '0. First\n1. Second\n2. Third')])
def test_preset_menu_with_fixture(capsys, test_settings, expected_output) -> None:
    """Test menu.preset_menu with  fixtures.

    This only tests the printed menu. The return value is ignored
    and will be tested separately.
    """
    with (patch('game_of_life.menu.get_all_presets') as mock_get_all_presets,
          patch('game_of_life.menu.get_user_preset_choice')):
        mock_get_all_presets.return_value = test_settings
        preset_menu()
        captured = capsys.readouterr()
        assert captured.err == ''
        assert captured.out.strip() == expected_output


def test_preset_menu_return() -> None:
    """Check return values from menu.preset_menu."""
    with (patch('game_of_life.menu.get_user_preset_choice') as mock_user_choice,
          patch('builtins.print')):  # No need to print.
        # Test values from 0 to an arbitrary number > number of presets.
        for val in range(100):
            mock_user_choice.return_value = val
            assert preset_menu() == mock_user_choice.return_value


def test_preset_menu_with_presets(capsys) -> None:
    """Test menu display with actual Presets.

    Expected output of each printed line in the form:
    integer dot space name_string.
    The final line(s) may be empty.

    Examples
    --------
        Printed line => '2. Beacon'

    Notes
    -----
    This only tests the printed menu. The return value is ignored
    """
    with patch('game_of_life.menu.get_user_preset_choice') as _:
        preset_menu()
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


def test_user_preset_choice(capsys) -> None:
    """Test menu.get_user_preset_choice.

    Notes
    -----
    get_user_preset_choice() returns the value input by user when the
    input is valid, or returns the default when input is an empty string.

    When user input is invalid, get_user_preset_choice() prompts for
    another input, and continues to do so until it receives a valid
    input.

    A valid input is an integer-string that matches a Preset ID.
    """
    mock_get_all_presets = [Preset(0, 'First', set()),
                            Preset(1, 'Second', set())]

    defaults = Defaults(universe_size=Size(0, 0), preset=0, refresh_rate=0.5)
    range_error = 'Invalid choice. Please try again.'
    type_error = 'Invalid input. Please enter a number.'
    no_error = ''

    test_cases = [  # ('input', 'error')
        ([''], [no_error], defaults.preset),  # Default.
        (['0'], [no_error], 0),  # Valid input.
        (['1'], [no_error], 1),  # Valid input.
        (['20', ''], [range_error], defaults.preset),  # Out of range.
        (['1.5', ''], [type_error], defaults.preset),  # Non-integer.
        (['not a number', ''], [type_error], defaults.preset),  # Non-numeric.
        (['w', '-6', '20', '1.5', '1'], [type_error, range_error], 1),  # Multiple errors.
    ]
    for inputs, errors, rtn in test_cases:
        with (patch('builtins.input', side_effect=inputs),
              patch('game_of_life.menu.get_all_presets', return_value=mock_get_all_presets),
              patch('game_of_life.menu.DEFAULTS', new=defaults)):
            val = get_user_preset_choice()
            captured = capsys.readouterr()
            if len(errors) == 1:  # A single error
                assert errors[0] == captured.out.strip()
            else:
                for err in errors:
                    assert err in captured.out
            assert val == rtn


def test_refresh_rate_menu() -> None:
    """Test menu.refresh_rate_menu.

    This only tests that the supplied input is returned.
    """
    with (patch('game_of_life.menu.REFRESH_RATE_RANGE', new={'min': 0, 'max': 10}),
          patch('game_of_life.menu.get_user_refresh_rate') as mock_user_refresh_rate):
        mock_user_refresh_rate.return_value = 1
        assert refresh_rate_menu() == mock_user_refresh_rate.return_value


def test_user_refresh_rate(capsys) -> None:
    """Test menu.get_user_refresh_rate.

    Notes
    -----
    get_user_refresh_rate() returns value input by user when input
    is valid.

    When user input is invalid, get_user_refresh_rate() prompts for
    another input, and continues to do so until it receives a valid
    input.

    A valid input is a float-string within REFRESH_RATE_RANGE.
    """
    refresh_rate_range = {'min': 0, 'max': 10}

    def side_effects():
        """User input values.

        Only the final value is valid.
        """
        input_vals = [
            refresh_rate_range['min'] - 1,
            refresh_rate_range['min'] - 1.1,
            refresh_rate_range['max'] + 1,
            refresh_rate_range['max'] + 1.1,
            'not a number',
            (refresh_rate_range['min'] + refresh_rate_range['max']) / 2.0
        ]
        for value in input_vals:
            yield str(value)

    with (patch('builtins.input', side_effect=side_effects()),
          patch('game_of_life.menu.REFRESH_RATE_RANGE', new=refresh_rate_range)):
        val = get_user_refresh_rate()
        # Invalid input should cause user prompts to be printed.
        captured = capsys.readouterr()
        assert captured.out
        assert val == (refresh_rate_range['min'] + refresh_rate_range['max']) / 2.0
