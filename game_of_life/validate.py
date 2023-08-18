"""Validators."""


from game_of_life.gol import get_all_presets
from game_of_life.constants import REFRESH_RATE_RANGE


def valid_refresh_rate_string(value: str) -> float:
    """Validate refresh rate string to a float.

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
    ValueError
        If value is invalid or outside valid range.

    Notes
    -----
    Used as a type validator for argparse. It converts the input string to
    a float, and is then validated using the 'valid_refresh_rate' function.
    If the 'value' string does not represent a number, argparse itself
    raises an ArgumentTypeError.
    """
    return valid_refresh_rate(float(value))


def valid_refresh_rate(value: float) -> float:
    """Validate and return a refresh rate value within a specified range.

    Parameters
    ----------
    value : float
        The requested refresh rate / frame display duration in seconds.
        A positive number between `fastest` and `slowest`

    Returns
    -------
    float
        The minimum length of time for an animation frame
        to display (seconds), if within the allowed range.

    Raises
    ------
    ValueError
        If value is outside valid range.

    Notes
    -----
    Validates whether the provided refresh rate value is within
    the range specified by constants.REFRESH_RATE_RANGE.
    """
    fastest = REFRESH_RATE_RANGE['min']
    slowest = REFRESH_RATE_RANGE['max']
    if not fastest <= value <= slowest:
        raise ValueError(
            f'Refresh rate must be between {fastest} and {slowest}.')
    return value


def valid_preset_id_string(value: str) -> int:
    """Validate preset ID string to an integer.

    Parameters
    ----------
    value : str
        The preset ID string to be validated.

    Returns
    -------
    int
        The valid preset ID as an integer.

    Raises
    ------
    ValueError
        If the converted preset ID is not within the valid range.

    Notes
    -----
    Used as a type validator for argparse. It converts the input string to
    an integer representing a preset ID, and is then validated using the
    'valid_preset_id' function.
    If the 'value' string does not represent an integer, argparse itself
    raises an ArgumentTypeError.
    """
    return valid_preset_id(int(value))


def valid_preset_id(value: int) -> int:
    """Validate and return a preset ID integer.

    Parameters
    ----------
    value : int
        The requested preset ID number.

    Returns
    -------
    int
        The selected preset ID number.

    Raises
    ------
    ValueError
        If value is not a valid Preset ID.
    """
    if value < 0 or value >= len(get_all_presets()):
        raise ValueError(
            f'{value} is not a valid preset ID.'
            f'Select a preset from 0 to {len(get_all_presets())}')
    return value
