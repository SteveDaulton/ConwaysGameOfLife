"""Tests for __main__.py."""
from unittest.mock import patch
from functools import partial

from game_of_life.__main__ import main
from game_of_life.gol import get_all_presets
from game_of_life.constants import DEFAULTS


def test_defaults() -> None:
    """Test __main__.defaults."""
    assert isinstance(DEFAULTS.refresh_rate, float)
    assert isinstance(DEFAULTS.preset, int)
    assert DEFAULTS.refresh_rate >= 0

    # Check that default refresh rate is not stupidly slow.
    assert DEFAULTS.refresh_rate < 10.0
    # Check that default preset is a unique match for a valid preset id.
    all_presets = get_all_presets()
    assert isinstance(all_presets, list)
    valid_ids = [preset.idx for preset in all_presets]
    assert valid_ids.count(DEFAULTS.preset) == 1


def test_main(monkeypatch) -> None:
    """Test __main__.main.

    Notes
    -----
    When the app is run without arguments, the preset state is selected
    by the user from the menu
    """
    # Monkeypatch sys.argv to simulate no command-line arguments.
    monkeypatch.setattr('sys.argv', ['__main__.py'])

    # Mock the functions that main calls.
    with patch('game_of_life.__main__.preset_menu') as mock_preset_menu, \
         patch('game_of_life.__main__.refresh_rate_menu') as mock_refresh_rate_menu, \
         patch('curses.wrapper') as mock_curses_wrapper, \
         patch('game_of_life.__main__.play') as mock_play:

        # Mock user input.
        mock_preset_menu.return_value = 4
        mock_refresh_rate_menu.return_value = 0.5

        main()

        # Get the arguments passed to the mock_curses_wrapper function call.
        wrapper_args = mock_curses_wrapper.call_args.args[0]

        # Check function calls.

        # Assert that the mocked menu functions were called once.
        mock_preset_menu.assert_called_once()
        mock_refresh_rate_menu.assert_called_once()

        # Assert that mock_curses_wrapper was called with the expected args.
        mock_curses_wrapper.assert_called_once_with(wrapper_args)

        # Assert mock_curses_wrapper was called with correct keyword arguments.
        assert (mock_curses_wrapper.call_args.args[0].keywords['choice'] ==
                mock_preset_menu.return_value)
        assert (mock_curses_wrapper.call_args.args[0].keywords['refresh_rate'] ==
                mock_refresh_rate_menu.return_value)

        # Set the return_value of mock_play to a partial object.
        expected_partial = partial(mock_play, choice=mock_preset_menu.return_value,
                                   refresh_rate=mock_refresh_rate_menu.return_value)

        # Assert that mock_curses_wrapper is called with expected partial.
        assert isinstance(wrapper_args, partial)
        assert wrapper_args.func == expected_partial.func
        assert wrapper_args.keywords == expected_partial.keywords
