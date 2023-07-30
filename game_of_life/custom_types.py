"""Type definitions for type hints."""

from typing import NamedTuple


class Point(NamedTuple):
    """Grid coordinates.

    ncurses' coordinates are ordered y: int, x: int.
    """

    y: int
    x: int


class Size(NamedTuple):
    """Grid size.

    ncurses' coordinates are ordered y: int, x: int.
    """

    y: int
    x: int


class Preset(NamedTuple):
    """Preset initial state of universe."""

    idx: int
    name: str
    cells: set[Point]


class Defaults(NamedTuple):
    """Default values for game_of_life.

    Provides immutable encapsulation of constants.
    """

    universe_size: Size
    preset: int
    refresh_rate: float
