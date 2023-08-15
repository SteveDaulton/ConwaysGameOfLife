"""Presets for initial state.

Examples from:
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
"""
from random import randint
from typing import Final

from game_of_life.custom_types import Preset, Point, Defaults, Size

PRESETS: Final[list[Preset]] = [
    Preset(0, 'Block', {Point(7, 7), Point(8, 7), Point(7, 8), Point(8, 8)}),
    Preset(1, 'Beehive', {Point(6, 10), Point(6, 11), Point(7, 9),
                          Point(7, 12), Point(8, 10), Point(8, 11)}),
    Preset(2, 'Beacon', {Point(2, 2), Point(2, 3), Point(3, 2), Point(3, 3),
                         Point(4, 4), Point(4, 5), Point(5, 4), Point(5, 5)}),
    Preset(3, 'Glider', {Point(2, 3), Point(3, 4), Point(4, 2), Point(4, 3), Point(4, 4)}),
    Preset(4, 'R-pentomino', {Point(10, 51), Point(10, 52), Point(11, 50),
                              Point(11, 51), Point(12, 51)}),
    Preset(5, 'Pulsar', {Point(1, 5), Point(1, 11),
                         Point(2, 5), Point(2, 11),
                         Point(3, 5), Point(3, 6), Point(3, 10), Point(3, 11),
                         Point(5, 1), Point(5, 2), Point(5, 3), Point(5, 6), Point(5, 7),
                         Point(5, 9), Point(5, 10), Point(5, 13), Point(5, 14), Point(5, 15),
                         Point(6, 3), Point(6, 5), Point(6, 7),
                         Point(6, 9), Point(6, 11), Point(6, 13),
                         Point(7, 5), Point(7, 6), Point(7, 10), Point(7, 11),
                         Point(9, 5), Point(9, 6), Point(9, 10), Point(9, 11),
                         Point(10, 3), Point(10, 5), Point(10, 7),
                         Point(10, 9), Point(10, 11), Point(10, 13),
                         Point(11, 1), Point(11, 2), Point(11, 3), Point(11, 6), Point(11, 7),
                         Point(11, 9), Point(11, 10), Point(11, 13), Point(11, 14), Point(11, 15),
                         Point(13, 5), Point(13, 6), Point(13, 10), Point(13, 11),
                         Point(14, 5), Point(14, 11),
                         Point(15, 5), Point(15, 11)}),
    Preset(6, 'Penadecathlon', {Point(4, 5),
                                Point(5, 4), Point(5, 6),
                                Point(6, 3), Point(6, 7),
                                Point(7, 3), Point(7, 7),
                                Point(8, 3), Point(8, 7),
                                Point(9, 3), Point(9, 7),
                                Point(10, 3), Point(10, 7),
                                Point(11, 3), Point(11, 7),
                                Point(12, 4), Point(12, 6),
                                Point(13, 5)})
]


def random_preset(random_id, pad_size):
    """Generate a random preset.

    Random preset 'may' include bottom right corner cell, which
    is invalid, but will be caught by validation when Universe
    is initialised.
    """
    max_x, max_y = pad_size
    max_x -= 1
    max_y -= 1
    rand_preset = Preset(random_id, 'Random',
                         set(Point(randint(0, max_x), randint(0, max_y))
                             for _ in range(randint(4, max_x * max_y))))
    return rand_preset


DEFAULTS: Final[Defaults] = Defaults(universe_size=Size(y=40, x=80),
                                     preset=4,
                                     refresh_rate=0.5)

# Time per frame greater than about 1 second are likely to be too slow for practical use.
# Zero frame duration effectively disables waiting.
# 10 seconds per frame is generous.
REFRESH_RATE_RANGE: Final[dict] = {'min': 0, 'max': 10}
