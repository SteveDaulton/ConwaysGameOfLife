from game_of_life.gol import *
import pytest


def test_point():
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
    universe = Universe(0)
    universe.live_cells = {Point(10, 10)}
    assert len(universe.update()) == 0
    universe.live_cells = {Point(10, 10), Point(10, 11), Point(10, 12)}
    expected = {Point(9, 11), Point(10, 11), Point(11, 11)}
    assert universe.update() == expected
    universe.live_cells = {Point(10, 10), Point(10, 11), Point(9, 10)}
    expected = {Point(9, 11), Point(10, 10), Point(10, 11), Point(9, 10)}
    assert universe.update() == expected
    universe.live_cells = {Point(0, 0), Point(0, 1), Point(2, 0)}
    expected = {Point(1, 0), Point(1, 1)}
    assert universe.update() == expected


def test_cell_in_range():
    assert cell_in_range(Size(100, 100), Point(99, 99)) is False
    assert cell_in_range(Size(100, 100), Point(0, 0)) is True
    assert cell_in_range(Size(100, 100), Point(-1, 0)) is False
    assert cell_in_range(Size(100, 100), Point(1, -1)) is False
    assert cell_in_range(Size(100, 100), Point(98, 99)) is True
    assert cell_in_range(Size(100, 100), Point(99, 98)) is True
    assert cell_in_range(Size(100, 100), Point(100, 0)) is False
    assert cell_in_range(Size(100, 100), Point(0, 100)) is False


def test_menu():
    display_menu()


def test_get_preset():
    presets = get_preset()
    # Check that presets is a list
    assert isinstance(presets, list)
    # Each preset is an instance of Preset named tuple, and
    # Preset indicies are numbered 0 to n.
    for i, option in enumerate(presets):
        assert isinstance(option, Preset)
        assert i == option.idx
