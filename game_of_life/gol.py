"""The Game of Life.
"""

import sys
import curses
import argparse
from random import randint
from typing import (Generator,
                    NamedTuple,
                    Final)
from functools import partial
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


class Preset(NamedTuple):
    """Preset initial state of universe."""
    idx: int
    name: str
    cells: set[Point]


def get_preset(choice: int = -1) -> Preset | list[Preset]:
    """Return preset dictionary or specified preset when valid choice passed.
    Examples from:
    https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    """
    presets = [
        Preset(0, 'block', {Point(7, 7), Point(8, 7), Point(7, 8), Point(8, 8)}),
        Preset(1, 'beehive', {Point(6, 10), Point(6, 11), Point(7, 9),
                              Point(7, 12), Point(8, 10), Point(8, 11)}),
        Preset(2, 'beacon', {Point(2, 2), Point(2, 3), Point(3, 2), Point(3, 3),
                             Point(4, 4), Point(4, 5), Point(5, 4), Point(5, 5)}),
        Preset(3, 'glider', {Point(2, 3), Point(3, 4), Point(4, 2), Point(4, 3), Point(4, 4)}),
        Preset(4, 'R-pentomino', {Point(10, 51), Point(10, 52), Point(11, 50),
                                  Point(11, 51), Point(12, 51)}),
        # TODO: Use Universe size rather than hard coded ranges for y and x.
        Preset(5, 'random', set(Point(randint(0, 38), randint(0, 98))
                                for _ in range(randint(10, 1000))))
    ]
    if choice >= 0:
        if choice < len(presets):
            return presets[choice]
        sys.exit('Invalid Preset ID.')
    return presets


def display_menu():
    """Print preset choices."""
    for setting in get_preset():
        print(f'{setting.idx}. {setting.name}')
    print()


def get_user_choice():
    """Return user choice from preset menu."""
    valid_indices = {option.idx for option in get_preset()}
    while True:
        try:
            choice = int(input("Select initial state: "))
            if choice in valid_indices:
                return choice
            print("Invalid choice. Please try again.")
        except IndexError:
            print("Invalid input. Please enter a number.")


def universe_init(choice: int) -> set[Point]:
    """Return initial universe state.
    Override this function for custom initial state.
    """
    # TODO: Make Universe a class to handle global properties
    # TODO: such as initial state, size of pad, colours, etc.
    # Keep MyPy happy.
    assert isinstance((live_cells := get_preset(choice)), Preset), f'Invalid preset id {choice}'
    return live_cells.cells


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


def cell_in_range(cell: Point) -> bool:
    """Return True if cell is within range of pad."""
    # TODO: Get pad size from Universe rather than duplicating setting.
    pad_size: Size = Size(y=40, x=100)
    return (pad_size.y - 1 >= cell.y >= 0 and
            pad_size.x - 1 >= cell.x >= 0 and not
            (cell.y == pad_size.y - 1 and cell.x == pad_size.x - 1))


def refresh_pad(pad, size):
    """Do pad refresh.
    Refreshed part of pad must fit in visible window, so
    get size of terminal window immediately before refresh
    in case terminal has been resized.
    """
    y_max = min(curses.LINES - 1, size[0])  # pylint: disable=maybe-no-member
    x_max = min(curses.COLS - 1, size[1])  # pylint: disable=maybe-no-member
    pad.refresh(0, 0, 0, 0, y_max, x_max)


def main(stdscr: curses.window, choice: int) -> None:
    """Play the Game of Life."""
    curses.curs_set(0)  # Turn off blinking cursor.
    stdscr.clear()
    universe: set[Point] = universe_init(choice)
    universe_old: set[Point] = set()
    # Pad (y, x) must be big enough to hold content.
    # TODO: This should be part of Universe settings.
    pad_size: Size = Size(y=40, x=100)
    pad = curses.newpad(pad_size[0], pad_size[1])

    # Initialise timer.
    clock = perf_counter()
    # If refresh rate is too fast, then animation will not be smooth.
    # TODO: This should be part of Universe settings.
    refresh_rate: Final[float] = 0.1

    while True:
        # Clear old cells.
        # This is a bit quicker than using pad.clear()
        for y, x in universe_old:
            pad.addch(y, x, ' ')

        # Add content to pad in reverse colours
        # TODO: Validate cells in Universe initial state.
        for y, x in universe:
            pad.addch(y, x, ' ', curses.A_REVERSE)

        # Wait before updating.
        clock = throttle(clock, refresh_rate)
        refresh_pad(pad, pad_size)

        # Update to next generation.
        universe_old = universe
        universe = update(universe)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # No arguments were passed
        display_menu()
        user_choice = get_user_choice()
        partial_main = partial(main, choice=user_choice)
        curses.wrapper(partial_main)
    else:
        # Arguments were passed
        parser = argparse.ArgumentParser(
            description="Conway's Game of Life.",
            epilog="Ctrl + C to quit.")
        parser.add_argument('-p', '--preset', type=int, help='Select preset by number.')
        args = parser.parse_args()
        try:
            preset = get_preset(args.preset)
        except IndexError:
            sys.exit(f'Invalid preset number. Select a preset from 0 to {len(get_preset())}')
        partial_main = partial(main, choice=args.preset)
        curses.wrapper(partial_main)
