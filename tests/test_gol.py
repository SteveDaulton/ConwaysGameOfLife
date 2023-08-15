"""Tests for gol.py."""


import pytest

from game_of_life.gol import Universe, get_all_presets
from game_of_life.custom_types import Point, Preset
from game_of_life.validate import (
    valid_refresh_rate_string,
    valid_preset_id_string,
    preset_id_range)


def test_update() -> None:
    """Test game_of_life.gol.update()"""
    universe = Universe()  # Singleton instance.
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


def test_get_preset() -> None:
    """Test game_of_life.gol.get_preset()"""
    presets = get_all_presets()
    # Case 1: presets is a list
    assert isinstance(presets, list)
    # Case 2: Each preset is an instance of Preset named tuple.
    # Case 3: Preset indices are numbered 0 to n.
    for i, option in enumerate(presets):
        assert isinstance(option, Preset)
        assert i == option.idx


def test_valid_preset_id() -> None:
    """Test __main__.valid_preset."""
    valid_indices = range(preset_id_range())
    # Case 1: Valid presets.
    for idx in valid_indices:
        assert valid_preset_id_string(f'{idx}') == idx
    # Case 2: Invalid preset IDs below 0.
    with pytest.raises(ValueError) as exc_info:
        valid_preset_id_string("-1")
    assert "is not a valid preset ID" in str(exc_info.value)
    # Case 3: Invalid preset IDs above maximum index.
    with pytest.raises(ValueError) as exc_info:
        valid_preset_id_string(str(preset_id_range() + 1))
    assert "is not a valid preset ID" in str(exc_info.value)
    # Case 4: Non-integer input
    with pytest.raises(ValueError) as exc_info:
        valid_preset_id_string("not_an_integer")
    assert "not_an_integer" in str(exc_info.value)


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
        assert valid_refresh_rate_string(f'{float_val}') - float_val < delta
    # Case 2: Out of range values.
    with pytest.raises(ValueError) as exc_info:
        valid_refresh_rate_string(f'{fastest - 0.01}')
    assert 'Refresh rate must be between' in str(exc_info.value)
    with pytest.raises(ValueError) as exc_info:
        valid_refresh_rate_string(f'{slowest + 0.01}')
    assert 'Refresh rate must be between' in str(exc_info.value)
    # Case 3: Non-number input
    with pytest.raises(ValueError) as exc_info:
        valid_refresh_rate_string('not a number')
    assert 'not a number' in str(exc_info.value)
