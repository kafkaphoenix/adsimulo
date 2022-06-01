import os

from termcolor import colored

from adsimulo.civ.contansts import CellState
from adsimulo.universe.constants import biome_colors
from adsimulo.universe.system import System


def clamp(val, nmin=0, nmax=1):
    return max(nmin, min(val, nmax))


def clear_shell():
    from platform import system

    os_system = system()
    if os_system == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def display(system: System):
    clear_shell()
    for _, planet in system.planets.items():
        print(f"Year {planet.age}")
        for lat in range(planet.height):
            for long in range(planet.width):
                biome = planet.terrain_grid[lat][long]
                civ = planet.civ_grid[lat][long]
                if civ != CellState.UNOCCUPIED.value:
                    print(colored(civ, "red"), end="")
                else:
                    print(colored(biome, biome_colors[biome]), end="")
            print("")
