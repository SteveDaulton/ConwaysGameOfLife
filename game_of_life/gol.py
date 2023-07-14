"""The Game of Life.
"""

import curses
import argparse
from random import randint
from typing import (Generator,
                    NamedTuple,
                    Final)
from time import perf_counter


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


Matrix = list[list[str]]


def universe_init(choice: int | str = 4) -> set[Point]:
    """Return initial universe state.
    Examples from:
    https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    """
    presets = {
        'block': {Point(7, 7), Point(8, 7), Point(7, 8), Point(8, 8)},
        'beehive': {Point(6, 10), Point(6, 11), Point(7, 9),
                    Point(7, 12), Point(8, 10), Point(8, 11)},
        'beacon': {Point(2, 2), Point(2, 3), Point(3, 2), Point(3, 3),
                   Point(4, 4), Point(4, 5), Point(5, 4), Point(5, 5)},
        'glider': {Point(2, 3), Point(3, 4), Point(4, 2), Point(4, 3), Point(4, 4)},
        'R-pentomino': {Point(10, 51), Point(10, 52), Point(11, 50),
                        Point(11, 51), Point(12, 51)},
        'random': set(Point(randint(0, 98), randint(0, 98)) for _ in range(randint(10, 1000))),
    }

    if type(choice) is str:
        return presets[choice]
    if type(choice) is int:
        return presets[list(presets.keys())[choice]]
    return presets['R-pentomino']


def neighbours(point: Point) -> Generator[Point, None, None]:
    """Yields each coordinate around point."""
    y = point[0]
    x = point[1]
    yield Point(y - 1, x - 1)
    yield Point(y, x - 1)
    yield Point(y + 1, x - 1)
    yield Point(y - 1, x)
    yield Point(y + 1, x)
    yield Point(y - 1, x + 1)
    yield Point(y, x + 1)
    yield Point(y + 1, x + 1)


def main(stdscr: curses.window) -> None:
    """Play the Game of Life."""
    curses.curs_set(0)  # Turn off blinking cursor.
    stdscr.clear()
    universe: set[Point] = universe_init()
    universe_old: set[Point] = set()
    # Pad (y, x) must be big enough to hold content.
    pad_size: Size = Size(y=100, x=100)
    pad = curses.newpad(pad_size[0], pad_size[1])

    # Initialise timer.
    clock = perf_counter()
    # If refresh rate is too fast, then animation will not be smooth.
    refresh_rate: Final[float] = 0.2

    # stop if universe is dead.
    while universe != universe_old:

        # Clear old cells
        for y, x in universe_old:
            pad.addch(y, x, ' ')

        # Add content to pad in reverse colours
        for y, x in universe:
            pad.addch(y, x, ' ', curses.A_REVERSE)

        # Wait before updating.
        clock = throttle(clock, refresh_rate)
        refresh_pad(pad, pad_size)

        # Update to next generation.
        universe_old = universe
        universe = update(universe)


def throttle(prev: float, period: float) -> float:
    """Wait until 'period' seconds since 'prev' time."""
    if 0.0 < (perf_counter() - prev) < period:
        sleep_time = period - (perf_counter() - prev)
        curses.napms(int(sleep_time * 1000))
    return perf_counter()


def update(living: set[Point]) -> set[Point]:
    """Return a set of new cells that satisfy the rules to
    be alive, and are within the display range.
    """
    new_cells = set()
    # We only need to consider cells that are either alive
    # or neighbouring a live cell.
    cell_set = set(living)
    for cell in living:
        cell_set.update(neighbours(cell))
    # Return the next generation.
    for cell in cell_set:
        n_cells = neighbours(cell)
        live_count = sum(1 for neighbor in n_cells if neighbor in living)
        if live_count == 3 or (live_count == 2 and cell in living):
            if cell_in_range(cell):
                new_cells.add(cell)
    return new_cells


def cell_in_range(cell):
    return (99 >= cell[0] >= 0 and
            99 >= cell[1] >= 0 and
            sum(cell) < 198)


def refresh_pad(pad, size):
    """Do pad refresh.
    Refreshed part of pad must fit in visible window, so
    get size of terminal window immediately before refresh
    in case terminal has been resized.
    """
    y_max = min(curses.LINES - 1, size[0])  # pylint: disable=maybe-no-member
    x_max = min(curses.COLS - 1, size[1])  # pylint: disable=maybe-no-member
    pad.refresh(0, 0, 0, 0, y_max, x_max)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     description="Conway's Game of Life.",
    #     epilog="Ctrl + C to quit.")
    # parser.add_argument('-p', '--preset', choices=['0', 'rock', '1', 'paper', '2', 'scissors'])
    # args = parser.parse_args()
    curses.wrapper(main)
    # try:
    #     preset = int(args.preset)
    # except ValueError:
    #     preset = args.preset
    # print(type(preset))
    # print(preset)
