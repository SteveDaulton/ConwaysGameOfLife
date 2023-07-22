"""The Game of Life.

Main entry point.
"""

import sys
import argparse
from functools import partial
from game_of_life.gol import (
    main,
    display_menu,
    get_user_choice,
    get_preset,
    curses)


if len(sys.argv) == 1:
    # No arguments were passed.
    display_menu()
    user_choice = get_user_choice()
    partial_main = partial(main, choice=user_choice,
                           refresh_rate=0.5)
    curses.wrapper(partial_main)
else:
    # Arguments were passed
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life.",
        epilog="Ctrl + C to quit.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--preset', type=int, default=4,
                        help='Select preset by number.')
    parser.add_argument('-r', '--refresh_rate', type=float, default=0.5,
                        help='Time per frame (seconds)')
    arguments = parser.parse_args()
    try:
        preset = get_preset(arguments.preset)
    except IndexError:
        parser.print_help()
        sys.exit(('\nError.\n'
                  f'"{arguments.preset}" is out of range.\n'
                  f'Select a preset from 0 to {len(get_preset())}'))
    partial_main = partial(main, choice=arguments.preset,
                           refresh_rate=arguments.refresh_rate)
    curses.wrapper(partial_main)
