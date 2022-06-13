import re

import numpy as np
from termcolor import colored

from adsimulo.civ.contansts import DICE_REGEX, CellState, CivActions
from adsimulo.config import Config
from adsimulo.universe.constants import Biomes
from adsimulo.universe.planet import Planet


def find_civ(eva, emblem: str) -> bool:
    found = eva.compendium.civilisations.get(emblem, None)
    if not found:
        raise Exception(f"Civilisation {emblem} not found")

    return found


def roll(dice: str) -> int:
    result = 0
    throw = re.match(DICE_REGEX, dice)
    if throw:
        throw = throw.group(0).split("d")
        result = sum(Config.rng.integers(1, int(throw[1]) + 1) for _ in range(int(throw[0])))

    return result


def menu() -> CivActions:
    action = None
    print("What are you doing next?\n")
    while action is None:
        print("Available actions:\n")
        print([f"{str(action)[0].lower()} - {action}" for action in CivActions])
        command = input()
        match command.split():
            case ["d"] | [CivActions.TECH_DEVELOPMENT.value]:
                action = CivActions.TECH_DEVELOPMENT
            case ["e"] | [CivActions.TERRITORIAL_EXPANSION.value]:
                action = CivActions.TERRITORIAL_EXPANSION
            case ["g"] | [CivActions.POPULATION_GROWTH.value]:
                action = CivActions.POPULATION_GROWTH
            case ["s"] | [CivActions.TERRITORIAL_STABILIZATION.value]:
                action = CivActions.TERRITORIAL_STABILIZATION
            case _:
                print("Wrong action, please try again\n")

    return action


def delete2d(array: np.ndarray, element: np.ndarray) -> np.ndarray:
    return array[~np.equal(array, element).all(1)]


def append2d(array: np.ndarray, new_array: np.ndarray) -> np.ndarray:
    return np.append(array, new_array, axis=0)


def contains2d(array: np.ndarray, element: np.ndarray) -> bool:
    return np.any(np.equal(array, element).all(1))


def count_element2d(array: np.ndarray, element: int) -> int:
    return np.count_nonzero(array == element)


def empty2d(array: np.ndarray) -> bool:
    return not array.any()


def filter2d(array: np.ndarray, element: str) -> list[tuple[int, int]]:
    result = np.where(array == element)
    coords = list(zip(result[0], result[1]))
    return coords


def replace2d(planet: Planet, indexes: np.ndarray, new_element: CellState):
    for lat, long in indexes:
        planet.civ_grid[lat][long] = new_element.value


def draw_civ(planet: Planet, name: str, emblem: str):
    with open(Config.debug_settings["MAP_FILENAME"], "a") as f:
        print(colored(f"{name} [{emblem}] has dissolved! Age: {planet.age}", "red"), file=f, end="")
        print("", file=f)
        for lat in range(planet.height):
            for long in range(planet.width):
                biome = planet.terrain_grid[lat][long]
                civ = planet.civ_grid[lat][long]
                if civ != CellState.UNOCCUPIED.value and civ == emblem:
                    print(colored(civ, "red"), file=f, end="")
                else:
                    print(colored(biome, Biomes.biome_color(biome)), file=f, end="")
            print("", file=f)
