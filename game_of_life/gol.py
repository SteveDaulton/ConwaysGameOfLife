"""The Game of Life."""

import curses
from typing import Generator, Type
from time import perf_counter

from game_of_life.custom_types import (
    Point,
    Size,
    Preset)
from game_of_life.constants import (
    PRESETS,
    random_preset,
    DEFAULTS)


class Universe:
    """Singleton class for Universe.

    The Game of Life occurs within the context of a single 'Universe'.
    This class manages persistent state of the Universe.
    """

    _instance = None
    _initialized = False

    def __new__(cls: Type['Universe'], *args, **kwargs) -> 'Universe':
        """Override the creation of new instances for the Singleton pattern.

        Enforces the Singleton pattern by allowing only one instance of the
        Universe class to exist at any time.

        Arguments
        ---------
            cls : Type['Universe']
                The class itself.

        Returns
        -------
        'Universe'
            The created instance or the existing instance if it already exists.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize an empty Universe."""
        if not Universe._initialized:
            self.display_size = DEFAULTS.universe_size
            self._refresh_rate = DEFAULTS.refresh_rate
            # Universe initialised without any cells.
            self.live_cells: set[Point] = set()
            Universe._initialized = True

    @property
    def refresh_rate(self):
        """refresh_rate getter."""
        return self._refresh_rate

    @refresh_rate.setter
    def refresh_rate(self, rate):
        """refresh_rate setter."""
        self._refresh_rate = rate

    def init_cells(self, choice: int = DEFAULTS.preset) -> None:
        """Initialise cell population.

        See Also
        --------
        get_one_preset : Retrieves a preset.

        """
        preset = get_one_preset(choice)
        self.live_cells = set(cell for cell in preset.cells)

    def update(self) -> set[Point]:
        """Update the Universe state according to the rules of Conway's Game of Life.

        Calculate and return the next generation of live cells based on the current
        state of the Universe and the rules of Conway's Game of Life.

        Returns
        -------
        set[Point]
            A set containing the new live cells that satisfy the rules and are
            within the display range.

        Notes
        -----
        The method considers the current live cells and their neighboring cells.
        It then calculates the number of live neighbors for each cell and applies
        the rules of the game to determine if the cell should be alive in the next
        generation.

        - If a cell has 3 live neighbors, it will be alive in the next generation,
          regardless of its current state.
        - If a cell has 2 live neighbors, and it is currently alive, it will continue
          to be alive in the next generation.

        The set containing the new live cells for the next generation is returned.
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
                new_cells.add(cell)
        return new_cells


class GameOfLifeUI:
    """Render GOL to terminal."""

    def __init__(self) -> None:
        """Initialize the GameOfLifeUI class.

        GameOfLifeUI handles graphic display of game.
        """
        self._universe = Universe()  # Singleton instance
        self._pad_size = self._universe.display_size
        height, width = self._pad_size
        self._pad: 'curses._CursesWindow' = curses.newpad(height, width)
        self._cell_char = ' '
        self._refresh_rate = self._universe.refresh_rate
        self._population: int = 0
        self._clock = perf_counter()

    @property
    def pad_size(self) -> Size:
        """Get the size of the Curses pad.

        Returns
        -------
        Size
            A namedtuple containing the height and width of the Curses pad.

        Note
        ----
            The size of the Curses pad is defined by the class attribute `_pad_size`, which
            represents the dimensions (height and width) of the pad. Allows access the
            pad size without directly accessing the protected class attribute.
        """
        return self._pad_size

    def populate(self, live_cells: set[Point]) -> None:
        """Populate the pad with live cells.

        Parameters
        ----------
        live_cells : set[Point]
            A set containing the coordinates of live cells.

        Raises
        ------
        'curses.error'
            If an error occurs while trying to add a live cell to the pad.
            Such errors are expected and must pass silently.

        """
        self._population = len(live_cells)
        for y, x in live_cells:
            # Adding characters outside the available window area raises a curses.error.
            try:
                self._pad.addch(y, x, self._cell_char, curses.A_REVERSE)
            except curses.error:
                pass

    def write_info(self) -> None:
        """Write info to top line of pad."""
        # Ensure that we have the current terminal size.
        curses.update_lines_cols()
        window_info: str = f' Height: {curses.LINES} Width: {curses.COLS} '
        window_info_pos = min(curses.COLS, self.pad_size.x) - len(window_info)
        # Clear top line
        self._pad.addstr(0, 0, self._cell_char * curses.COLS)
        # Add info to top line of pad.
        self._pad.addstr(0, 0, f'Population: {self._population} ', curses.A_REVERSE)
        self._pad.addstr(0, window_info_pos, window_info, curses.A_REVERSE)

    def refresh_pad(self) -> None:
        """Refresh the Curses pad.

        The pad is refreshed at a controlled rate based on the `refresh_rate` attribute.
        If the elapsed time since the last refresh is less than the `refresh_rate`,
        the method will wait to achieve the desired frame rate.
        The pad's refresh area is adjusted to fit the visible window.

        Notes
        -----
        - Sleep time is calculated to maintain the desired frame rate.
        - The pad's refresh area is limited to fit within the terminal window.
        """
        # Wait if less than refresh_rate (seconds) since previous refresh.
        if 0.0 < (perf_counter() - self._clock) < self._refresh_rate:
            sleep_time = self._refresh_rate - (perf_counter() - self._clock)
            curses.napms(int(sleep_time * 1000))
        self._clock = perf_counter()
        # Now refresh the area of the pad that will fit in terminal window.
        y_max = min(curses.LINES - 1, self.pad_size.y)
        x_max = min(curses.COLS - 1, self.pad_size.x)
        self._pad.refresh(0, 0, 0, 0, y_max, x_max)

    def clear_cells(self, cells: set[Point]) -> None:
        """Clear the cells on the pad."""
        for y, x in cells:
            try:
                self._pad.addch(y, x, self._cell_char)
            except curses.error:
                # addch to bottom right corner throws a curses error
                pass


def neighbours(point: Point) -> Generator[Point, None, None]:
    """Yield each coordinate around point.

    Each neighbouring cell is yielded in turn.

    Arguments
    ---------
    point : Point
        Coordinates (y, x) of the cell being evaluated.

    Yields
    ------
    Point
        The neighboring cell coordinates.
    """
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


def play(stdscr: curses.window, choice: int, refresh_rate: float) -> None:
    """Play the Game of Life."""
    curses.curs_set(0)  # Turn off blinking cursor.
    stdscr.clear()
    # Initialise Universe instance.
    universe = Universe()
    # Initialise starting  population.
    universe.init_cells(choice)
    universe.refresh_rate = refresh_rate
    # Initialise game interface.
    ui = GameOfLifeUI()
    universe_old: set[Point] = set()

    while True:
        # Clear old cells.
        ui.clear_cells(universe_old)
        # Add content to pad in reverse colours
        ui.populate(universe.live_cells)
        # (Optional) write info to top line.
        ui.write_info()
        # Render to screen.
        ui.refresh_pad()
        # Update to next generation.
        universe_old = universe.live_cells
        universe.live_cells = universe.update()


def get_all_presets() -> list[Preset]:
    """Return list of presets."""
    presets = PRESETS
    next_idx = presets[-1][0] + 1
    rand_preset = random_preset(next_idx, DEFAULTS.universe_size)
    presets.append(rand_preset)
    return presets


def get_one_preset(choice: int) -> Preset:
    """Return specified preset when valid choice passed.

    Raises
    ------
    IndexError
        When choice is not in presets.

    TypeError
        When choice is not an integer.
    """
    presets = get_all_presets()
    return presets[choice]
