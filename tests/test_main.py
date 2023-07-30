"""Tests for __main__.py."""
from unittest.mock import patch

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
    with patch('game_of_life.__main__.display_menu') as mock_display_menu, \
         patch('game_of_life.__main__.get_user_choice') as mock_get_user_choice, \
         patch('curses.wrapper') as mock_curses_wrapper, \
         patch('game_of_life.__main__.play') as mock_play:

        # Mock user choice of preset.
        mock_get_user_choice.return_value = 4

        # Set the return_value of mock_play to a partial object.
        # mock_play.return_value = partial(mock_play, choice='1', refresh_rate=0.5)

        main()

        print('\nArgs:', mock_curses_wrapper.call_args)
        print('\nArgs:', mock_curses_wrapper.call_args.args[0])
        print('Expect:', mock_play.return_value)

        # Assert that the mocked functions were called with the expected parameters.
        mock_display_menu.assert_called_once()
        mock_get_user_choice.assert_called_once()
        # mock_curses_wrapper.assert_called_once_with(
        #     mock_curses_wrapper.call_args[0][0])
        mock_curses_wrapper.assert_called_once()
