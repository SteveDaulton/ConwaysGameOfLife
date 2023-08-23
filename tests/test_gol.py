"""Tests for gol.py."""

from unittest.mock import patch, Mock

import pytest

from game_of_life.gol import (Universe,
                              GameOfLifeUI,
                              get_all_presets,
                              get_one_preset)
from game_of_life.custom_types import Point, Preset, Size
from game_of_life.constants import DEFAULTS, PRESETS


# pylint: disable=W0212 [protected-access]


@pytest.fixture(name="universe_singleton")
def universe_fixture():
    """Fixture for Universe Singleton Testing.

        Sets up and provides an initialized Universe singleton instance for testing purposes.
        The fixture yields the singleton instance, and after the test completes, it resets
        the Universe singleton to its initial state.

        Yields
        ------
        Universe
            An initialized Universe singleton instance.
        """
    # Setup: Initialize the Universe singleton
    universe = Universe()
    yield universe
    # Teardown: Reset the Universe singleton to its initial state
    Universe._instance = None
    Universe._initialized = False


def test_update(universe_singleton) -> None:
    """Test game_of_life.gol.update()"""
    universe = universe_singleton  # Singleton instance.
    # Case 1: A single cell dies.
    universe.live_cells = {Point(10, 10)}
    assert len(universe.update()) == 0
    # Case 2: 3 adjacent cells in a line.
    universe.live_cells = {Point(10, 10), Point(10, 11), Point(10, 12)}
    expected = {Point(9, 11), Point(10, 11), Point(11, 11)}
    assert universe.update() == expected
    # Case 3: 3 cells in "L" shape.
    universe.live_cells = {Point(10, 10), Point(10, 11), Point(9, 10)}
    expected = {Point(9, 11), Point(10, 10), Point(10, 11), Point(9, 10)}
    assert universe.update() == expected
    # Case 4: Two cells above and one below.
    universe.live_cells = {Point(0, 0), Point(0, 1), Point(2, 0)}
    expected = {Point(1, 0), Point(1, 1)}
    assert universe.update() == expected


def test_get_preset() -> None:
    """Test game_of_life.gol.get_preset()"""
    presets = get_all_presets()
    # Case 1: presets is a tuple
    assert isinstance(presets, tuple)
    # Case 2: Each preset is an instance of Preset named tuple.
    # Case 3: Preset indices are numbered 0 to n.
    for i, option in enumerate(presets):
        assert isinstance(option, Preset)
        assert i == option.idx


# Universe Tests

def test_singleton(universe_singleton) -> None:
    """Test that Universe is singleton."""
    u1 = universe_singleton
    u2 = universe_singleton
    assert u1 is u2


@pytest.mark.parametrize('attribute, expected_type', [
    ('_initialized', bool),
    ('display_size', Size),
    ('_refresh_rate', float),
    ('live_cells', set)])
def test_universe_attribute_types(universe_singleton, attribute, expected_type) -> None:
    """Test Universe attribute types."""
    universe = universe_singleton
    attr = getattr(universe, attribute)
    assert isinstance(attr, expected_type)


@pytest.mark.parametrize('attribute, expected_val', [
    ('_initialized', True),
    ('display_size', DEFAULTS.universe_size),
    ('_refresh_rate', DEFAULTS.refresh_rate),
    ('live_cells', set()),
])
def test_universe_attribute_values(universe_singleton, attribute, expected_val):
    """Test Universe attribute values."""
    universe = universe_singleton
    attr = getattr(universe, attribute)
    assert attr == expected_val


def test_init_cells(universe_singleton):
    """Test Universe.init_cells."""
    universe = universe_singleton
    mock_presets = [Preset(0, 'first', {Point(0, 0), Point(1, 1)}),
                    Preset(1, 'second', {Point(0, 0)})]
    def mock_get_one_preset(choice):
        """Mock of get_one_preset"""
        return mock_presets[choice]

    with patch('game_of_life.gol.get_one_preset', side_effect=mock_get_one_preset):
        # Case 1: Valid choice.
        choice = 0
        universe.init_cells(choice=choice)
        assert universe.live_cells == mock_presets[choice].cells

        # Case 2: Another valid choice.
        choice = 1
        universe.init_cells(choice=choice)
        assert universe.live_cells == mock_presets[choice].cells
        previous_state = universe.live_cells

        # Invalid choices leave the Universe unchanged.

        # Case 3: Out of range choice
        choice = 20
        with pytest.raises(Exception):
            universe.init_cells(choice=choice)
        assert universe.live_cells == previous_state

        # Case 4: Invalid choice type.
        choice = 'not a number'
        with pytest.raises(Exception):
            universe.init_cells(choice=choice)
        assert universe.live_cells == previous_state

        # Case 5: Non-integer choice.
        choice = 1.5
        with pytest.raises(Exception):
            universe.init_cells(choice=choice)
        assert universe.live_cells == previous_state


def test_refresh_rate(universe_singleton) -> None:
    """Test Universe.refresh_rate."""
    default_rate = DEFAULTS.refresh_rate
    universe = universe_singleton
    # Case 1: Default value
    assert universe.refresh_rate == default_rate
    # Case 2: Set refresh rate.
    universe.refresh_rate = 1.0
    assert universe.refresh_rate == 1.0


# GameOfLifeUI Tests

@pytest.mark.parametrize('attribute, expected_type', [
    ('_universe', Universe),
    ('_pad_size', Size),
    ('_pad', None),  # Placeholder for _pad's expected type
    ('_cell_char', str),
    ('_refresh_rate', float),
    ('_population', int),
    ('_clock', float),
])
@patch('curses.newpad')  # Patch the curses.newpad function.
def test_gameoflifeui_attribute_types(mock_newpad, attribute, expected_type) -> None:
    """Test GameOfLifeUI attribute types."""
    mock_curses_window = Mock(name='curses._CursesWindow')
    mock_newpad.return_value = mock_curses_window
    gol = GameOfLifeUI()
    # Iterate through attributes and test types
    attr = getattr(gol, attribute)
    if attr == gol._pad:
        assert isinstance(gol._pad, type(mock_curses_window))
    else:
        assert isinstance(attr, expected_type)


@patch('curses.newpad')  # Patch the curses.newpad function
def test_gameoflifeui_init(mock_newpad, universe_singleton):
    """Test GameOfLifeUI attribute values."""
    mock_curses_window = Mock(name='curses._CursesWindow')
    mock_newpad.return_value = mock_curses_window
    universe = universe_singleton
    # Create the GameOfLifeUI instance
    golui = GameOfLifeUI()

    # Assertions for attribute initialization
    assert golui._universe is universe
    assert golui._pad_size == universe.display_size
    assert golui._pad is mock_curses_window
    assert golui._cell_char == ' '
    assert golui._refresh_rate == universe.refresh_rate
    assert golui._population == 0
    assert isinstance(golui._clock, float)


@pytest.fixture(name="mock_game_of_life_ui")
def mock_gol_ui():
    """Fixture to mock GameOfLifeUI class for testing."""
    class MockGameOfLifeUI(GameOfLifeUI):
        """Mock of GameOfLifeUI class."""
        # pylint: disable=super-init-not-called
        def __init__(self):
            # Do not call the parent class's __init__ method.
            # Initialize attributes needed for testing.
            self._pad_size = Size(y=50, x=100)  # Expected pad size

    with patch('game_of_life.gol.GameOfLifeUI', MockGameOfLifeUI):
        yield MockGameOfLifeUI()


def test_gameoflifeui_pad_size(mock_game_of_life_ui):
    """Test game_of_life.GameOfLifeUI.pad_size getter."""
    assert mock_game_of_life_ui.pad_size == Size(y=50, x=100)


@pytest.mark.timeout(0.5)  # Ensure we don't get stuck in loop.
def test_gol_get_one_preset() -> None:
    """Test gol.get_one_preset.

    Notes
    -----
    1. get_one_preset returns a valid Preset.
    2. Presets should have an idx attribute that matches its index.
    3. raises IndexError when preset request fails.
    4. Number of presets should length of PRESETS + 1 (the random preset)
    """
    # One `random` preset is added to the constant.PRESETS
    expected_number_of_presets = len(PRESETS) + 1

    index = 0
    preset_count = 0
    while True:
        try:
            preset = get_one_preset(index)
            # Case 1: preset is type Preset
            assert isinstance(preset, Preset)
            # Case 2: preset.idx == index
            assert preset.idx == index
            preset_count += 1
        except IndexError:  # Case 3: No more presets
            # Case 4: Expected number of presets.
            assert preset_count == expected_number_of_presets
            break  # Exit test.
        index += 1
