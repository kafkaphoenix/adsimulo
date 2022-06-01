import argparse

from adsimulo.config import DEBUG, GAME_MODES, SEED, YEAR


class DefaultArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument(
            "-d",
            "--debug",
            help="Enable debug mode",
            action="store_true",
            default=DEBUG,
        )
        self.add_argument(
            "-s",
            "--seed",
            help="Set seed to initialize the random number generator",
            type=int,
            default=SEED,
        )
        self.add_argument(
            "-y",
            "--year",
            help="Year when the simulation will stop",
            type=int,
            default=YEAR,
        )


def select_mode() -> int:
    print("Welcome! Please select a game mode:\n")
    print(f"0. {GAME_MODES[0]}\n")
    print(f"1. {GAME_MODES[1]}\n")
    mode = input()
    mode = int(mode) if mode else -1
    while mode != 0 and mode != 1:
        print("Wrong input. Please select a game mode:\n")
        print(f"0. {GAME_MODES[0]}\n")
        print(f"1. {GAME_MODES[1]}\n")
        mode = int(input())

    return mode
