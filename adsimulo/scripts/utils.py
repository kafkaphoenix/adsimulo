"""Miscellaneous Scripts methods."""

import argparse

from adsimulo.config import GAME_MODES, SEED, YEAR


class DefaultArgumentParser(argparse.ArgumentParser):
    """Parse arguments from commands."""

    def __init__(self, *args, **kwargs):
        """Initialize arguments for each command."""
        super().__init__(*args, **kwargs)
        self.add_argument('--debug', help='Enable debug mode', action='store_true')
        self.add_argument('--seed', help='Set seed to initialize the random number generator', type=int, default=SEED)
        self.add_argument('--year', help='Year when the simulation will stop', type=int, default=YEAR)


def select_game_mode():
    """Print a game mode menu.

    Small menu which ask the game mode until it is valid.

    :return: the game mode selected.
    :rtype: int
    """
    print('Welcome! Please select a game mode:\n')
    print(f'0. {GAME_MODES[0]}\n')
    print(f'1. {GAME_MODES[1]}\n')
    mode = int(input())
    while(mode != 0 and mode != 1):
        print('Wrong input. Please select a game mode:\n')
        print(f'0. {GAME_MODES[0]}\n')
        print(f'1. {GAME_MODES[1]}\n')
        mode = int(input())

    return mode
