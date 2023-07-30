"""Tests for custom_types module"""


import pytest

from game_of_life.custom_types import Point, Size


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
