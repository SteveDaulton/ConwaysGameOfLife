"""Menu system for  Game of Life."""

from game_of_life.gol import get_all_presets
from game_of_life.constants import REFRESH_RATE_RANGE, DEFAULTS


def preset_menu() -> int:
    """Print preset choices and prompt for selection.

    Returns
    -------
    int
        Selected preset ID.
    """
    all_settings = get_all_presets()
    for setting in all_settings:
        print(f'{setting.idx}. {setting.name}')
    print()
    return get_user_preset_choice()


def get_user_preset_choice() -> int:
    """Return user choice from preset menu."""
    valid_indices = {option.idx for option in get_all_presets()}
    while True:
        user_input: str = input(f'Select initial state (default {DEFAULTS.preset}): ')
        if user_input == "":
            return DEFAULTS.preset
        try:
            selected_index = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if selected_index in valid_indices:
            return selected_index
        print("Invalid choice. Please try again.")


def refresh_rate_menu() -> float:
    """Prompt for refresh rate input."""
    fastest, slowest = REFRESH_RATE_RANGE.values()
    print(f"""Set animation speed.
Enter a target value for the length of time, in seconds, that each
animation will be displayed. The game will wait between frames if the
next frame is ready before the specified time.

Valid values are in the range:
{fastest} : As fast as possible.
{slowest} : Each frame displayed for {slowest} seconds.
    """)
    return get_user_refresh_rate()


def get_user_refresh_rate() -> float:
    """Return user choice from refresh-rate menu."""
    fastest, slowest = REFRESH_RATE_RANGE.values()
    while True:
        user_input: str = input("Time per frame (default 0.5 seconds): ")
        if user_input == "":
            return DEFAULTS.refresh_rate
        try:
            refresh_rate = float(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if fastest <= refresh_rate <= slowest:
            return refresh_rate
        print("Out of range. Please try again.")
