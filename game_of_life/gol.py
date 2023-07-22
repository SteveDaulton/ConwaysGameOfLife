"""The Game of Life.
"""

import curses
from typing import Generator
from time import perf_counter
from random import randint

from game_of_life.presets import PRESETS
from game_of_life.custom_types import (
    Point,
    Size,
    Preset)


def display_menu():
    """Print preset choices."""
    for setting in get_preset():
        print(f'{setting.idx}. {setting.name}')
    print()


def get_preset(choice: int = -1) -> Preset | list[Preset]:
    """Return preset dictionary or specified preset when valid choice passed."""
    max_x, max_y = GameOfLifeUI.display_pad_size()
    max_x -= 1
    max_y -= 1
    presets = PRESETS
    # Random preset 'may' include bottom right corner cell, which
    # is invalid, but will be caught by validation when Universe
    # is initialised.
    random_id = presets[-1][0] + 1
    random_preset = Preset(random_id, 'Random',
                           set(Point(randint(0, max_x), randint(0, max_y))
                               for _ in range(randint(1, max_x * max_y))))
    presets.append(random_preset)
    if choice >= 0:
        return presets[choice]
    return presets


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


class GameOfLifeUI:
    """Render GOL to terminal."""
    _pad_size: Size = Size(y=40, x=100)

    def __init__(self, refresh_rate) -> None:
        height, width = GameOfLifeUI._pad_size
        self.pad = curses.newpad(height, width)
        self.cell_char = ' '
        self.refresh_rate = refresh_rate
        self.clock = perf_counter()

    @property
    def pad_size(self):
        """self.pad_size from class attribute."""
        return GameOfLifeUI._pad_size

    @classmethod
    def display_pad_size(cls) -> Size:
        """Return cls._pad_size.
        Public method to get class attribute.
        """
        return cls._pad_size

    def populate(self, live_cells: set[Point]) -> None:
        """Populate pad with live cells."""
        for y, x in live_cells:
            self.pad.addch(y, x, self.cell_char, curses.A_REVERSE)

    def refresh_pad(self):
        """Do pad refresh.
        Refreshed part of pad must fit in visible window, so
        get size of terminal window immediately before refresh
        in case terminal has been resized.
        """
        if 0.0 < (perf_counter() - self.clock) < self.refresh_rate:
            sleep_time = self.refresh_rate - (perf_counter() - self.clock)
            curses.napms(int(sleep_time * 1000))
        self.clock = perf_counter()

        if curses.is_term_resized(curses.LINES, curses.COLS):
            # If the terminal has been resized, recalculate y_max and x_max
            curses.resizeterm(curses.LINES, curses.COLS)
        y_max = min(curses.LINES - 1, self.pad_size.y)  # pylint: disable=maybe-no-member
        x_max = min(curses.COLS - 1, self.pad_size.x)  # pylint: disable=maybe-no-member
        self.pad.refresh(0, 0, 0, 0, y_max, x_max)

    def clear_cells(self, cells: set[Point]) -> None:
        """Clear the cells on the pad."""
        for y, x in cells:
            self.pad.addch(y, x, self.cell_char)


class Universe:
    """Singleton class for Universe."""
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, choice) -> None:
        if not Universe._initialized:
            # 'choice' should already be validated.
            assert isinstance((live_cells := get_preset(choice)), Preset),\
                f'Invalid preset id {choice}'
            # Cells must fit in pad, so validate before adding.
            self.display_size = GameOfLifeUI.display_pad_size()
            self.live_cells = set(cell for cell in live_cells.cells
                                  if cell_in_range(self.display_size, cell))
            Universe._initialized = True

    def update(self) -> set[Point]:
        """Return a set of new cells that satisfy the rules to
        be alive, and are within the display range.
        """
        new_cells = set()
        # We only need to consider cells that are either alive
        # or neighbouring a live cell.
        cell_set = set(self.live_cells)
        for cell in self.live_cells:
            cell_set.update(neighbours(cell))
        # Return the next generation.
        for cell in cell_set:
            n_cells = neighbours(cell)
            live_count = sum(1 for neighbor in n_cells if neighbor in self.live_cells)
            if live_count == 3 or (live_count == 2 and cell in self.live_cells):
                if cell_in_range(self.display_size, cell):
                    new_cells.add(cell)
        return new_cells


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


def cell_in_range(pad_size: Size, cell: Point) -> bool:
    """Return True if cell is within range of pad."""
    return (pad_size.y - 1 >= cell.y >= 0 and
            pad_size.x - 1 >= cell.x >= 0 and not
            (cell.y == pad_size.y - 1 and cell.x == pad_size.x - 1))


def main(stdscr: curses.window, choice: int,
         refresh_rate: float) -> None:
    """Play the Game of Life."""
    curses.curs_set(0)  # Turn off blinking cursor.
    stdscr.clear()

    ui = GameOfLifeUI(refresh_rate)
    universe = Universe(choice)
    universe_old: set[Point] = set()

    while True:
        # Clear old cells.
        ui.clear_cells(universe_old)
        # Add content to pad in reverse colours
        ui.populate(universe.live_cells)
        # Render to screen.
        ui.refresh_pad()
        # Update to next generation.
        universe_old = universe.live_cells
        universe.live_cells = universe.update()
