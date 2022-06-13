from __future__ import annotations

from enum import Enum


class GameModes(str, Enum):
    CPU_MODE = "CPU"
    PLAYER_MODE = "Player"
    EXIT = "Exit"

    def __str__(self) -> str:
        return f"{self.value}"

    def mode(game_mode: GameModes) -> int:
        match game_mode.split():
            case [GameModes.CPU_MODE]:
                mode = 0
            case [GameModes.PLAYER_MODE]:
                mode = 1
            case [GameModes.EXIT]:
                mode = 2
            case _:
                Exception("Wrong game mode\n")

        return mode
