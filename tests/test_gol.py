"""Tests for gol.py."""

from unittest.mock import patch

import pytest


from game_of_life.gol import Universe, get_all_presets
from game_of_life.custom_types import Point, Preset, Size
from game_of_life.validate import (
    valid_refresh_rate_string,
    valid_preset_id_string,
    preset_id_range)
from game_of_life.constants import DEFAULTS


def test_singleton() -> None:
    """Test that Universe is singleton."""
    u1 = Universe()
    u2 = Universe()
    assert u1 is u2


@pytest.mark.parametrize('attribute, expected_type', [
    ('_initialized', bool),
    ('display_size', Size),
    ('_refresh_rate', float),
    ('live_cells', set)])
def test_universe_attribute_types(attribute, expected_type) -> None:
    """Test Universe attribute types."""
    universe = Universe()
    attr = getattr(universe, attribute)
    assert isinstance(attr, expected_type)


@pytest.mark.parametrize('attribute, expected_val', [
    ('_initialized', True),
    ('display_size', DEFAULTS.universe_size),
    ('_refresh_rate', DEFAULTS.refresh_rate),
    ('live_cells', set())
])
def test_universe_attribute_values(attribute, expected_val):
    """Test Universe attribute values."""
    universe = Universe()
    attr = getattr(universe, attribute)
    assert attr == expected_val


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


def test_init_cells():
    """Test init_cells."""
    universe = Universe()
    mock_presets = [Preset(0, 'first', {Point(0, 0), Point(1, 1)}),
                    Preset(1, 'second', {Point(0, 0)})]
    def mock_get_one_preset(choice):
        """Mock of get_one_preset"""
        return mock_presets[choice]

    with patch('game_of_life.gol.get_one_preset', side_effect=mock_get_one_preset):
        # Case 1: Valid choice.
        choice = 0
        universe.init_cells(choice=choice)
        assert universe.live_cells == mock_presets[choice].cells

        # Case 2: Another valid choice.
        choice = 1
        universe.init_cells(choice=choice)
        assert universe.live_cells == mock_presets[choice].cells
        previous_state = universe.live_cells

        # Invalid choices leave the Universe unchanged.

        # Case 3: Out of range choice
        choice = 20
        with pytest.raises(Exception):
            universe.init_cells(choice=choice)
        assert universe.live_cells == previous_state

        # Case 4: Invalid choice type.
        choice = 'not a number'
        with pytest.raises(Exception):
            universe.init_cells(choice=choice)
        assert universe.live_cells == previous_state

        # Case 5: Non-integer choice.
        choice = 1.5
        with pytest.raises(Exception):
            universe.init_cells(choice=choice)
        assert universe.live_cells == previous_state
