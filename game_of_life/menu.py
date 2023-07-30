"""Menu system for  Game of Life."""

from game_of_life.gol import get_all_presets


def display_menu() -> None:
    """Print preset choices."""
    all_settings = get_all_presets()
    assert isinstance(all_settings, list)
    for setting in all_settings:
        print(f'{setting.idx}. {setting.name}')
    print()


def get_user_choice():
    """Return user choice from preset menu."""
    valid_indices = {option.idx for option in get_all_presets()}
    while True:
        try:
            selected_index = int(input("Select initial state: "))
            if selected_index in valid_indices:
                return selected_index
            print("Invalid choice. Please try again.")
        except IndexError:
            print("Invalid input. Please enter a number.")
