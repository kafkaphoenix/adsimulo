import os

from termcolor import colored

from adsimulo.civ.contansts import CellState
from adsimulo.universe.constants import Biomes
from adsimulo.universe.planet import Planet


def clear_shell():
    from platform import system

    os_system = system()
    if os_system == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def draw_map(planet: Planet):
    for lat in range(planet.height):
        for long in range(planet.width):
            biome = planet.terrain_grid[lat][long]
            civ = planet.civ_grid[lat][long]
            if civ != CellState.UNOCCUPIED.value:
                print(colored(civ, "red"), end="")
            else:
                print(colored(biome, Biomes.biome_color(biome)), end="")
        print("")
