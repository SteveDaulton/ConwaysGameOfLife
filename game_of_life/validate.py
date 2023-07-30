"""Validators."""
import argparse

from game_of_life.gol import get_all_presets


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
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f'{value} is not a valid float.') from exc


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
        if int_value < 0 or int_value >= len(get_all_presets()):
            raise argparse.ArgumentTypeError(
                f'{value} is not a valid preset ID.'
                f'Select a preset from 0 to {len(get_all_presets())}')
        return int_value
    except ValueError:
        # pylint: disable=W0707
        raise argparse.ArgumentTypeError(
            f'{value} is not a valid integer.'
            f'Select a preset from 0 to {len(get_all_presets())}.')
