"""Tests for presets module.

Notes
-----
PRESET is type: Final[list[Preset]].
Each preset in PRESETS must:
- Be a valid Preset type.
- Have a unique idx, as a sequence of consecutive integers.
- Have a non-empty name (str).
- Have at least one cell.
"""

from game_of_life.constants import PRESETS
from game_of_life.custom_types import Preset, Point


def test_preset_type() -> None:
    """Test: RESETS is a list of valid Preset instances."""
    assert isinstance(PRESETS, list)
    for preset in PRESETS:
        assert isinstance(preset, Preset)


def test_preset_data() -> None:
    """Test: Each preset in PRESETS has valid data."""
    for val, preset in zip(range(len(PRESETS)), PRESETS):
        # preset.idx must increment sequentially.
        assert val == preset.idx
        # preset.name must be non-empty string.
        assert isinstance(preset.name, str) and bool(preset.name)
        # preset.cells must be a non-empty set of cells.
        assert isinstance(preset.cells, set) and bool(preset.cells)
        for cell in preset.cells:
            assert isinstance(cell, Point)
