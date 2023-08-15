"""The Game of Life.

Main entry point for running the Game of Life.
"""

import sys
import argparse
import curses
from functools import partial

from game_of_life.gol import play
from game_of_life.menu import display_menu, get_user_choice
from game_of_life.constants import DEFAULTS
from game_of_life.validate import valid_refresh_rate_string, valid_preset_id_string


def main() -> None:
    """Entry point to game_of_life.

    Notes
    -----
    Use `if __name__ == '__main__':`, even though __main__.py is a valid
    entry point without it, so that argparse code does not interfere with pytest.
    """
    if len(sys.argv) == 1:
        # No arguments were passed.
        display_menu()
        user_choice = get_user_choice()
        # TODO: Add menu for refresh rate.
        partial_main = partial(play, choice=user_choice,
                               refresh_rate=DEFAULTS.refresh_rate)
        curses.wrapper(partial_main)
    else:
        # Arguments were passed
        parser = argparse.ArgumentParser(
            description="Conway's Game of Life.",
            epilog="Ctrl + C to quit.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('-p', '--preset', type=valid_preset_id_string,
                            default=DEFAULTS.preset,
                            help='Select preset by number.')
        parser.add_argument('-r', '--refresh_rate',
                            type=valid_refresh_rate_string, default=DEFAULTS.refresh_rate,
                            help='Time per frame (seconds)')
        arguments = parser.parse_args()
        partial_main = partial(play, choice=arguments.preset,
                               refresh_rate=arguments.refresh_rate)
        curses.wrapper(partial_main)


if __name__ == '__main__':
    main()
