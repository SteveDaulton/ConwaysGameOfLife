"""Tests for __main__.py."""
from unittest.mock import patch, DEFAULT
from contextlib import ExitStack

import pytest

from game_of_life.__main__ import main
from game_of_life.custom_types import Defaults, Size
from game_of_life.gol import get_all_presets


@pytest.fixture(name="mock_patches")
def mock_setup():
    """Mock functions and DEFAULTS accessed by main()."""
    defaults = Defaults(universe_size=Size(0, 0), preset=0, refresh_rate=0.5)
    with ExitStack() as stack:
        mock_user_defaults = stack.enter_context(
            patch('game_of_life.__main__.DEFAULTS', new=defaults))
        mock_curses_wrapper = stack.enter_context(
            patch('curses.wrapper'))
        mock_menus = stack.enter_context(patch.multiple(
            'game_of_life.__main__',
            preset_menu=DEFAULT,
            refresh_rate_menu=DEFAULT))
        yield (mock_user_defaults, mock_menus, mock_curses_wrapper)


def test_main_defaults(mock_patches) -> None:
    """Test __main__ attribute default values."""
    # Unpack the mocks from the fixture
    defaults, _, _ = mock_patches

    assert isinstance(defaults.refresh_rate, float)
    assert isinstance(defaults.preset, int)
    assert defaults.refresh_rate >= 0

    # Check that default refresh rate is not stupidly slow.
    assert defaults.refresh_rate < 10.0

    all_presets = get_all_presets()
    assert isinstance(all_presets, tuple)
    # Check that preset ID matches index number.
    valid_ids = [preset.idx for index, preset in enumerate(all_presets)
        if index == preset.idx]
    assert len(valid_ids) == len(all_presets)
    # Check that default preset is a unique match for a valid preset id.
    assert defaults.preset in valid_ids


def test_main_with_no_args(mock_patches, monkeypatch) -> None:
    """Test __main__.main() without arguments.

    __main__ calls 'curses.wrapper' with partial formed from menu options.
    """

    # Unpack the mocks from the fixture.
    _, menu_mocks, mock_curses_wrapper = mock_patches
    preset_menu_mock = menu_mocks['preset_menu']
    refresh_rate_menu_mock = menu_mocks['refresh_rate_menu']

    # patch command-line attributes with no additional options.
    monkeypatch.setattr('sys.argv', ['__main__.py'])

    # Assign return values to the mock menus
    user_preset = 4
    user_refresh_rate = 0.5
    preset_menu_mock.return_value = user_preset
    refresh_rate_menu_mock.return_value = user_refresh_rate

    main()

    # Assert that the mocked menu functions were called once.
    preset_menu_mock.assert_called_once()
    refresh_rate_menu_mock.assert_called_once()

    # Get the arguments passed to the mock_curses_wrapper function call.
    actual_args = mock_curses_wrapper.call_args.args

    # Assert that mock_curses_wrapper was called with the expected args.
    mock_curses_wrapper.assert_called_once_with(actual_args[0])

    # We can't directly compare the partial, so compare the
    # arguments: actual arguments with the expected arguments.
    expected_preset = user_preset
    expected_refresh_rate = user_refresh_rate
    assert actual_args[0].keywords['choice'] == expected_preset
    assert actual_args[0].keywords['refresh_rate'] == expected_refresh_rate


def test_main_with_args(mock_patches, monkeypatch) -> None:
    """Test __main__.main() with command-line arguments.

    __main__ calls 'curses.wrapper' with partial formed from
    command-line options.
    """

    # Unpack the mocks from the fixture
    _, menu_mocks, mock_curses_wrapper = mock_patches
    preset_menu_mock = menu_mocks['preset_menu']
    refresh_rate_menu_mock = menu_mocks['refresh_rate_menu']

    # Assign return values to the mock command line
    user_preset = 4
    user_refresh_rate = 0.5
    # patch command-line attributes with options.
    monkeypatch.setattr('sys.argv', ['__main__.py',
                                     f'-p {user_preset}', f'-r {user_refresh_rate}'])

    main()

    # Assert that the mocked menu functions were not called.
    preset_menu_mock.assert_not_called()
    refresh_rate_menu_mock.assert_not_called()

    # Get the arguments passed to the mock_curses_wrapper function call.
    actual_args = mock_curses_wrapper.call_args.args

    # Assert that mock_curses_wrapper was called with the expected args.
    mock_curses_wrapper.assert_called_once_with(actual_args[0])

    # We can't directly compare the partial, so compare the
    # arguments: actual arguments with the expected arguments.
    expected_preset = user_preset
    expected_refresh_rate = user_refresh_rate
    assert actual_args[0].keywords['choice'] == expected_preset
    assert actual_args[0].keywords['refresh_rate'] == expected_refresh_rate
