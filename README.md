# Conway's Game of Life

A Python implementation of Conway's Game of Life by Steve Daulton.

_Copyright Steve Daulton 2023._

## About

The Game of Life was devised by John Horton Conway as a simple
example of cellular automaton.

Progress of the "game" is determined by the initial state, with no further input.
The game then progresses based on a few simple rules.


### Rules:

The game takes place on a ("infinite") 2D grid of cells (the "board").
Each cell is either alive or dead.
Each cell interacts with its neighbouring cells to determine whether
the cell lives or dies on the next step:

- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by
reproduction.

These rules simplify to a single condition:

```
If cell has 3 neighbors, or cell is alive and has 2 neighbors:
    the cell lives
else:
    the cell dies
```

## Motivation

I wrote this little application primarily as an exercise / excuse to try out
Python's curses module. Treating this as a Python programming exercise, it is
my intention to follow [PEP-8](https://pep8.org/) closely, and include
docstrings, type hints and tests.

### Why (not) Curses?

Installing / importing a UI library seemed like overkill for such simple graphics
whereas curses is included in Python (on Linux). Curses is extremely lightweight, requiring
only a basic text terminal to run.

#### Would I choose to use curses again?

Curses is very old, and it shows. Where curses falls down is in areas that were
not relevant 30+ years ago, but that we take for granted in the 21st century.
Terminals in the 1990's had a fixed, physical size and resolution. Resizeable
and / or overlapping windows were not a thing, and colour, if supported at all,
was limited to maybe 8 colours.

Regular annoyances included:

- Coordinates are upsidedown and backwards (y, x) from top left to bottom right.
- Print outside of the window area => crash.
- Refresh a pad outside of the window area => crash.
- Resize the terminal while writing => crash.
- Debugging: Who needs debugging!

On the plus side, the entire app is only around 150 lines of code.

Would I choose to use curses again? No way :)


## Installation:

This application does not need to be installed. Just download the ZIP file, and
extract its contents somewhere convenient.

### Prerequisites

This app was developed using Python 3.11, though it will probably run with any
reasonably modern version of Python 3.

Python's curses module must be available. Note that The Windows version of Python
doesn’t include the curses module. A ported version called UniCurses is available .


### Running from the command line

1. Open a terminal window, either full screen, or at least 40 lines x 100 characters.
2. Navigate to the folder containing the `game_of_life` folder.
3. Launch the application with:

```
$ python3 -m game_of_life
```

4. When launched with no additional arguments you will see a menu showing the
available presets. Each preset represents a different initial configuration of
live cells.
5. Enter the number corresponding to the preset you want to use and press Enter. 
6. The game will start, and you will see the cells evolve from generation to
generation based on the rules of Conway's Game of Life. 
7. Press Ctrl + C to quit the game.


### Command line options

The application may be run without the menu by supplying command line arguments.

- -h, --help
    : Display application help.

- -p, --preset
    : Select preset initial state by number [default 4]

- -r --refresh-rate
    : Time per frame (seconds) [default 0.5]

#### Command line example:

To start the game with preset 2 and a refresh rate of 0.2, run the following
command:

```
$ python3 -m game_of_life -p 2 -r 0.2
```

## Acknowledgments

- The `Universe` class and the core game logic are inspired by the work of
John Conway.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE)
