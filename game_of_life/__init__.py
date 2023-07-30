"""game_of_life.

This package provides a graphical / text based implementation of Conway's Game of Life,
a cellular automaton model devised by John Horton Conway in 1970.
The game simulates the evolution of a grid of cells, based on simple set of rules.

Game of Life runs in a terminal window and uses curses for rendering the game
visuals. It allows users to visualize the game's evolution from a selection of
initial configurations.

Usage
-----
Game of Life may be launched from a terminal window with:

    `python3 -m game_of_life`

Running without additional arguments opens a menu in the terminal, allowing a
preset initial configuration to be selected.

Alternatively, configuration options may be enabled from command-line switches.
To view available command-line options, enter:

    `python3 -m game_of_life --help`

Dependencies
------------
The only dependencies are:
- Python 3
    The game was developed using Python 3.11, but any recent version should work.
- curses: Used to create the graphical interface and visualization.
    On Linux, this is usually included with Python.
    The Windows version of Python does not include the curses module, but a ported
    version called UniCurses is available, which may be installed separately.

Package Structure
-----------------
The package is organized as follows:

- `__init__.py`: This file marks the package as a Python package and provides a
  brief overview of the package's functionality.
- `__main__.py`: Entry point for the module.
- `constants.py`: Provides the presets and default values.
- `custom_types.py`: Type definitions for type hints.
- `gol.py`: The main program, including the curses rendering class.
- `menu.py`: The start menu.
- `validate.py`: Validation functions.

Implementation Details
----------------------
- The text-based interface utilizes curses to create a terminal-based GUI for the game.
- The `Universe` class in `gol.py` manages the game's state and its evolution, following
  the rules of Conway's Game of Life.
- Rendering to the terminal is handled by the `GameOfLifeUI` class, also in`gol.py`.
- The `menu.py` module displays a start menu allowing users to customize the initial
  state of the grid and set the frame rate for the simulation.
- The game evolution is visualized with a customizable frame rate to control the
  speed of the simulation.

For detailed documentation, refer to the documentation in the /docs/ directory.

License
-------
Distributed under the MIT License. Please see the LICENSE
file for more information.

For bug reports or contributions, please use 'Issues' or 'Pull Requests' at:
https://github.com/SteveDaulton/ConwaysGameOfLife

Enjoy exploring the fascinating world of Conway's Game of Life!
"""
