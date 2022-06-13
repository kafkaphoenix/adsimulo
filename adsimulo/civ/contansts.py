from enum import Enum


class CellState(str, Enum):
    UNOCCUPIED = ""


class CivActions(str, Enum):
    TECH_DEVELOPMENT = "Develop"
    TERRITORIAL_EXPANSION = "Expand"
    POPULATION_GROWTH = "Growth"
    TERRITORIAL_STABILIZATION = "Stabilize"

    def __str__(self) -> str:
        return f"{self.value}"


CIV_EMBLEMS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[{]}\\|;:,<.>/?"

DICE_REGEX = r"(\d+(d|D)\d+)"
