import argparse

from adsimulo.scripts.constants import GameModes
from adsimulo.settings import DEBUG_SETTINGS, GAME_SETTINGS, RANDOM_SETTINGS


class DefaultArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument(
            "-d",
            "--debug",
            help="Enable debug mode",
            action="store_true",
            default=DEBUG_SETTINGS["DEBUG"],
        )
        self.add_argument(
            "-s",
            "--seed",
            help="Set seed to initialize the random number generator",
            type=int,
            default=RANDOM_SETTINGS["SEED"],
        )
        self.add_argument(
            "-y",
            "--year",
            help="Year when the simulation will stop",
            type=int,
            default=GAME_SETTINGS["STOP"],
        )
        self.add_argument(
            "-n",
            "--noise",
            help="Set noise",
            type=str,
            default=RANDOM_SETTINGS["NOISE"],
        )


def game_mode() -> GameModes:
    mode = None
    print("Welcome! Please select a game mode:\n")
    while mode is None:
        print(f"{GameModes.mode(GameModes.CPU_MODE)}. {GameModes.CPU_MODE}\n")
        print(f"{GameModes.mode(GameModes.PLAYER_MODE)}. {GameModes.PLAYER_MODE}\n")
        print(f"{GameModes.mode(GameModes.EXIT)}. {GameModes.EXIT}\n")
        command = input()
        match command.split():
            case ["0"] | ["cpu"] | ["c"]:
                mode = GameModes.CPU_MODE
            case ["1"] | ["player"] | ["p"]:
                mode = GameModes.PLAYER_MODE
            case ["2"] | ["exit"] | ["e"]:
                mode = GameModes.EXIT
            case _:
                print("Wrong mode, please try again\n")
    return mode
