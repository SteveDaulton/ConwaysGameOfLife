"""The Game of Life.

Main entry point for running the Game of Life.
"""

import sys
import argparse
import curses
from functools import partial
from game_of_life.gol import (
    play,
    display_menu,
    get_user_choice,
    get_preset)

DEFAULT_REFRESH_RATE = 0.5
DEFAULT_PRESET = 4


def valid_refresh_rate(value: str) -> float:
    """Validate refresh rate.

    Parameters
    ----------
    value : str
        The requested refresh rate / frame display duration in seconds.
        A string representation of a positive number between `fastest` and `slowest`

    Returns
    -------
    float
        The minimum length of time for an animation frame
        to display (seconds).

    Raises
    ------
    argparse.ArgumentTypeError
        If value is invalid or outside valid range.

    Notes
    -----
        Values greater than about 1 second are likely to be too slow for practical use.
    """
    fastest = 0.0  # The shortest frame duration. Effectively disables waiting.
    slowest = 10.0  # 10 seconds per frame!
    try:
        float_value = float(value)
        if not 0 <= float_value <= 10:
            raise argparse.ArgumentTypeError(
                f'Refresh rate must be between {fastest} and {slowest}.')
        return float_value
    except ValueError:
        # pylint: disable=W0707
        raise argparse.ArgumentTypeError(f'{value} is not a valid float.')


def valid_preset_id(value: str) -> int:
    """Validate preset ID.

    Parameters
    ----------
    value : str
        The requested preset ID number.

    Returns
    -------
    int
        The selected preset ID number.

    Raises
    ------
    argparse.ArgumentTypeError
        If value is not a valid Preset ID.
    """
    try:
        int_value = int(value)
        if int_value < 0 or int_value >= len(get_preset()):
            raise argparse.ArgumentTypeError(
                f'{value} is not a valid preset ID.'
                f'Select a preset from 0 to {len(get_preset())}')
        return int_value
    except ValueError:
        # pylint: disable=W0707
        raise argparse.ArgumentTypeError(
            f'{value} is not a valid integer.'
            f'Select a preset from 0 to {len(get_preset())}.')


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
        partial_main = partial(play, choice=user_choice,
                               refresh_rate=DEFAULT_REFRESH_RATE)
        curses.wrapper(partial_main)
    else:
        # Arguments were passed
        parser = argparse.ArgumentParser(
            description="Conway's Game of Life.",
            epilog="Ctrl + C to quit.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('-p', '--preset', type=valid_preset_id,
                            default=DEFAULT_PRESET,
                            help='Select preset by number.')
        parser.add_argument('-r', '--refresh_rate', type=valid_refresh_rate, default=0.5,
                            help='Time per frame (seconds)')
        arguments = parser.parse_args()
        partial_main = partial(play, choice=arguments.preset,
                               refresh_rate=arguments.refresh_rate)
        curses.wrapper(partial_main)


if __name__ == '__main__':
    main()
