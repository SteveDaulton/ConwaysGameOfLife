"""Tests."""

import pytest
from game_of_life.gol import (Universe,
                              cell_in_range,
                              display_menu,
                              get_preset)
from game_of_life.custom_types import Point, Size,Preset


def test_point():
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


def test_size():
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


def test_update():
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


def test_cell_in_range():
    """Test game_of_life.gol.cell_in_range()"""
    assert cell_in_range(Size(100, 100), Point(99, 99)) is True
    assert cell_in_range(Size(100, 100), Point(0, 0)) is True
    assert cell_in_range(Size(100, 100), Point(-1, 0)) is False
    assert cell_in_range(Size(100, 100), Point(1, -1)) is False
    assert cell_in_range(Size(100, 100), Point(100, 0)) is False
    assert cell_in_range(Size(100, 100), Point(0, 100)) is False


def test_menu():
    """Test menu display."""
    display_menu()


def test_get_preset():
    """Test ame_of_life.gol.get_preset()"""
    presets = get_preset()
    # Case 1: presets is a list
    assert isinstance(presets, list)
    # Case 2: Each preset is an instance of Preset named tuple.
    # Case 3: Preset indices are numbered 0 to n.
    for i, option in enumerate(presets):
        assert isinstance(option, Preset)
        assert i == option.idx
