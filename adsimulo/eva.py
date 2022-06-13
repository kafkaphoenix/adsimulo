import logging
from dataclasses import dataclass
from time import sleep
from typing import Optional

from adsimulo.civ.civ import Civilisation
from adsimulo.civ.contansts import CellState
from adsimulo.civ.utils import filter2d, roll
from adsimulo.compendium import Compendium
from adsimulo.config import Config
from adsimulo.scripts.constants import GameModes
from adsimulo.universe.constants import Biomes
from adsimulo.universe.galaxy import Galaxy
from adsimulo.universe.planet import Planet
from adsimulo.universe.system import System

logger = logging.getLogger(__name__)


@dataclass
class Eva:
    compendium: Optional[Compendium] = None

    def __post_init__(self):
        if self.compendium is None:
            self.compendium = Compendium()

    @staticmethod
    def lore():
        print("Initializing universe...")
        sleep(0.3)
        print("Increasing simulation speed...")
        sleep(0.3)
        print("Superfast inflation...")
        sleep(0.3)
        print("Post inflation...")
        sleep(0.3)
        print("Cooling cosmos...")
        sleep(0.3)
        print("Atom era...")
        sleep(0.3)
        print("Entering into Galaxy era...")
        sleep(0.3)
        print("Fast-forwarding first galaxies and planetary systems...")
        sleep(0.3)
        print("First dying stars...")
        sleep(0.3)
        print("Slowing time...")
        sleep(0.3)
        print("Cooling proto-star...")
        sleep(0.3)
        print("Cooling proto-planets...")
        sleep(0.3)
        print("Analyzing planets' habitability...")
        sleep(0.3)

    def deploy(self) -> bool:
        self.compendium.galaxy = Galaxy()
        nsystems = Config.rng.integers(1, Config.game_settings["SYSTEM_SAMPLE"] + 1)
        for system in range(nsystems):
            system = System()
            habitable_planets = system.habitable_planets()
            if not habitable_planets:
                print("Failed to find habitable planets...Retrying with another system")
                sleep(0.3)
                continue
            self.compendium.galaxy.systems[system.name] = system
            Civilisation.eva = self
            for planet in habitable_planets:
                self._adam(settlers=Config.game_settings["SETTLERS"], planet=planet)
        return len(self.compendium.galaxy.systems) > 0

    def _adam(self, settlers: int, planet: Planet):
        unocuppied = filter2d(planet.civ_grid, CellState.UNOCCUPIED.value)
        attempts = Config.rng.choice(unocuppied, min(len(unocuppied), settlers), replace=False)
        for attempt in attempts:
            lat = attempt[0]
            long = attempt[1]
            biome_coord = planet.terrain_grid[lat][long]
            if biome_coord != Biomes.OCEAN.value:
                if Config.game_settings["MODE"] == GameModes.PLAYER_MODE:
                    new_civ = Civilisation.born(lat=lat, long=long, planet=planet, cpu=False)
                    if new_civ:
                        Config.game_settings["MODE"] = GameModes.CPU_MODE
                else:
                    Civilisation.born(lat=lat, long=long, planet=planet)

    def loop(self):
        year = 0
        while year < Config.game_settings["STOP"]:
            self.compendium.display()
            self._progress()
            self._populate()
            if not Config.debug_settings["FAST"]:
                sleep(0.1)
            year += 1

    def _progress(self):
        for _, civ in self.compendium.civilisations.copy().items():
            if not civ.dead:
                civ.actions()
                civ.cadastre()
            else:
                raise Exception(f"WAIT! You should be dead...{civ}")

    def _populate(self):
        for _, system in self.compendium.galaxy.systems.items():
            habitable_planets = system.habitable_planets()
            for planet in habitable_planets:
                if Config.rng.integers(1, 21) == 20:
                    self._adam(settlers=roll("1d6"), planet=planet)
                planet.age += 1
            system.age += 1
            self.compendium.galaxy.age += 1

    def stats(self):
        self.compendium.galaxy.stats()
        Civilisation.stats()
