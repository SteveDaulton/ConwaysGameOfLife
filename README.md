Conway's Game of Life
=====================

A Python implementation of Conway's Game of Life.

The Game of Life was devised by John Horton Conway as a simple
example of cellular automaton.

Progress of the "game" is determined by the initial state, with no further input.
The game then progresses based on a few simple rules.


Rules:
======

The game takes place on a ("infinite") 2D grid of cells (the "board").
Each cell is either alive or dead.
Each cell interacts with its neighbouring cells to determine whether
the cell lives or dies on the next step:

- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

These rules simplify to a single condition:

If cell has 3 neighbors, or cell is alive and has 2 neighbors:
    the cell lives
else:
    the cell dies
