from game_of_life.gol import *
from unittest.mock import patch
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
    assert len(update({Point(10, 10)})) == 0
    univ = {Point(10, 10), Point(10, 11), Point(10, 12)}
    expected = {Point(9, 11), Point(10, 11), Point(11, 11)}
    assert update(univ) == expected
    univ = {Point(10, 10), Point(10, 11), Point(9, 10)}
    expected = {Point(9, 11), Point(10, 10), Point(10, 11), Point(9, 10)}
    assert update(univ) == expected
    univ = {Point(0, 0), Point(0, 1), Point(2, 0)}
    expected = {Point(1, 0), Point(1, 1)}
    assert update(univ) == expected


def test_cell_in_range():
    assert cell_in_range((99, 99)) is False
    assert cell_in_range((0, 0)) is True
    assert cell_in_range((-1, 0)) is False
    assert cell_in_range((1, -1)) is False
    assert cell_in_range((98, 99)) is True
    assert cell_in_range((99, 98)) is True
    assert cell_in_range((100, 0)) is False
    assert cell_in_range((0, 100)) is False


def test_throttle():
    """Test throttle()
    Note: curses.napms does not perform correctly with
    tests, so mock napms to test that it receives the
     correct arguments."""
    with patch("curses.napms") as mock_napms:
        # Case 1: No waiting needed
        start = perf_counter()
        end = throttle(start, 0.0)
        elapsed = end - start
        assert 0.0 <= abs(elapsed) < 0.001
        mock_napms.assert_not_called()

        # Case 2: waiting period already exceeded
        start = perf_counter() + 0.6
        delay = 0.5
        end = throttle(start, delay)
        assert abs(throttle(start, delay) - perf_counter()) < 0.001
        elapsed = end - start
        assert elapsed < 0.0
        mock_napms.assert_not_called()

        # Case 3: Short wait needed
        start = perf_counter()
        delay = 0.2
        end = throttle(start, delay)
        elapsed = end - start
        sleep_duration = (delay - elapsed)
        assert abs(sleep_duration - delay) > 0.0
        mock_napms.assert_called_with(int(sleep_duration * 1000))

        # Case 4: Long wait needed
        start = perf_counter()
        delay = 2.0
        end = throttle(start, delay)
        elapsed = end - start
        sleep_duration = (delay - elapsed)
        assert abs (sleep_duration - delay) < 0.002
        mock_napms.assert_called_with(int(sleep_duration * 1000))
