"""Tests."""

import argparse
from unittest.mock import patch
from functools import partial

import pytest

from game_of_life.gol import (Universe,
                              display_menu,
                              get_preset)
from game_of_life.custom_types import (Point,
                                       Size,
                                       Preset)
from game_of_life.__main__ import (valid_preset_id,
                                   valid_refresh_rate,
                                   main)


def test_point() -> None:
    """Test game_of_life.custom_types.Point"""
    # Case 1: Initialization and attribute access
    p = Point(2, 3)
    assert p.y == 2
    assert p.x == 3
    # Case 2: Immutable properties
    with pytest.raises(AttributeError):
        p.y = 5  # Trying to modify 'y' should raise an AttributeError
    with pytest.raises(AttributeError):
        p.x = 7  # Trying to modify 'x' should raise an AttributeError
    # Case 3: Comparison and equality
    p1 = Point(2, 3)
    p2 = Point(2, 3)
    p3 = Point(4, 5)
    assert p1 == p2  # p1 and p2 should be equal
    assert p1 != p3  # p1 and p3 should not be equal


def test_size() -> None:
    """Test game_of_life.custom_types.Size"""
    # Case 1: Initialization and attribute access
    s = Size(2, 3)
    assert s.y == 2
    assert s.x == 3
    # Case 2: Immutable properties
    with pytest.raises(AttributeError):
        s.y = 5  # Trying to modify 'y' should raise an AttributeError
    with pytest.raises(AttributeError):
        s.x = 7  # Trying to modify 'x' should raise an AttributeError
    # Case 3: Comparison and equality
    s1 = Size(2, 3)
    s2 = Size(2, 3)
    s3 = Size(4, 5)
    assert s1 == s2  # p1 and p2 should be equal
    assert s1 != s3  # p1 and p3 should not be equal


def test_update() -> None:
    """Test game_of_life.gol.update()"""
    universe = Universe(0)
    # Case 1: A single cell dies.
    universe.live_cells = {Point(10, 10)}
    assert len(universe.update()) == 0
    # Case 2: 3 adjacent cells in a line.
    universe.live_cells = {Point(10, 10), Point(10, 11), Point(10, 12)}
    expected = {Point(9, 11), Point(10, 11), Point(11, 11)}
    assert universe.update() == expected
    # Case 3: 3 cells in "L" shape.
    universe.live_cells = {Point(10, 10), Point(10, 11), Point(9, 10)}
    expected = {Point(9, 11), Point(10, 10), Point(10, 11), Point(9, 10)}
    assert universe.update() == expected
    # Case 4: Two cells above and one below.
    universe.live_cells = {Point(0, 0), Point(0, 1), Point(2, 0)}
    expected = {Point(1, 0), Point(1, 1)}
    assert universe.update() == expected


def test_menu() -> None:
    """Test menu display."""
    display_menu()


def test_get_preset() -> None:
    """Test game_of_life.gol.get_preset()"""
    presets = get_preset()
    # Case 1: presets is a list
    assert isinstance(presets, list)
    # Case 2: Each preset is an instance of Preset named tuple.
    # Case 3: Preset indices are numbered 0 to n.
    for i, option in enumerate(presets):
        assert isinstance(option, Preset)
        assert i == option.idx


def test_valid_preset_id() -> None:
    """Test __main__.valid_preset."""
    valid_indices = range(len(get_preset()))
    # Case 1: Valid presets.
    for idx in valid_indices:
        assert valid_preset_id(f'{idx}') == idx
    # Case 2: Invalid preset IDs below 0.
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        valid_preset_id("-1")
    assert "is not a valid preset ID" in str(exc_info.value)
    # Case 3: Invalid preset IDs above maximum index.
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        valid_preset_id(str(len(get_preset()) + 1))
    assert "is not a valid preset ID" in str(exc_info.value)
    # Case 4: Non-integer input
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        valid_preset_id("not_an_integer")
    assert "is not a valid integer" in str(exc_info.value)


def test_valid_refresh_rate() -> None:
    """Test __main__.valid_refresh_rate.

    Refresh rate is fastest when waiting before refresh is zero (disabled).
    `slowest` is fairly arbitrary, but should match __main__.valid_refresh_rate().
    """
    fastest = 0
    slowest = 10
    # Case 1: Valid values.
    delta = 1e-9
    for val in range(fastest, 10 * slowest):
        float_val = val / 10.0
        # Being cautious about float precision, though probably not necessary.
        assert valid_refresh_rate(f'{float_val}') - float_val < delta
    # Case 2: Out of range values.
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        valid_refresh_rate(f'{fastest - 0.01}')
    assert 'Refresh rate must be between' in str(exc_info.value)
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        valid_refresh_rate(f'{slowest + 0.01}')
    assert 'Refresh rate must be between' in str(exc_info.value)
    # Case 3: Non-number input
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        valid_refresh_rate('not a number')
    assert 'is not a valid float.' in str(exc_info.value)


def test_main(monkeypatch):
    """Test __main__.main."""
    # Monkeypatch sys.argv to simulate no command-line arguments.
    monkeypatch.setattr('sys.argv', ['__main__.py'])

    # Mock the functions that main calls and the input() function.
    with patch('game_of_life.__main__.display_menu', return_value='1') as mock_display_menu, \
         patch('game_of_life.__main__.get_user_choice', return_value='1') as mock_get_user_choice, \
         patch('curses.wrapper') as mock_curses_wrapper, \
         patch('game_of_life.__main__.play') as mock_play:

        # Mock the gol.display_menu() function directly.
        mock_display_menu.return_value = None

        # Set the return_value of mock_play to a partial object.
        mock_play.return_value = partial(mock_play, choice='1', refresh_rate=0.5)

        main()
        # Assert that the mocked functions were called with the expected parameters.
        mock_display_menu.assert_called_once()
        mock_get_user_choice.assert_called_once_with()
        mock_curses_wrapper.assert_called_once_with(
            mock_curses_wrapper.call_args[0][0])
