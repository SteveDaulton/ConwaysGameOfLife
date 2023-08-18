"""Tests for validate.py."""

import pytest

from game_of_life.validate import (
    valid_refresh_rate_string)


def test_valid_refresh_rate() -> None:
    """Test __main__.valid_refresh_rate.

    Refresh rate is fastest when waiting before refresh is zero (disabled).
    `slowest` is fairly arbitrary, but should match __main__.valid_refresh_rate().
    """
    fastest = 0
    slowest = 10
    # Case 1: Valid values.
    delta = 1e-9
    for val in range(fastest, 10 * slowest):
        float_val = val / 10.0
        # Being cautious about float precision, though probably not necessary.
        assert valid_refresh_rate_string(f'{float_val}') - float_val < delta
    # Case 2: Out of range values.
    with pytest.raises(ValueError) as exc_info:
        valid_refresh_rate_string(f'{fastest - 0.01}')
    assert 'Refresh rate must be between' in str(exc_info.value)
    with pytest.raises(ValueError) as exc_info:
        valid_refresh_rate_string(f'{slowest + 0.01}')
    assert 'Refresh rate must be between' in str(exc_info.value)
    # Case 3: Non-number input
    with pytest.raises(ValueError) as exc_info:
        valid_refresh_rate_string('not a number')
    assert 'not a number' in str(exc_info.value)
