from dataclasses import dataclass, field
from time import sleep
from typing import Dict, Optional

from adsimulo.config import PIONERS
from adsimulo.universe.planet import Planet
from adsimulo.universe.system import System
from adsimulo.utils import display


@dataclass
class Eva:
    seed: int
    galaxy: Optional[Dict[str, System]] = field(default_factory=dict)

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
        system = System(seed=self.seed)
        habitable_planets = self._is_habitable(system)
        if not habitable_planets:
            print("Failed to find habitable planets...Retrying with another system")
            sleep(0.3)
            return False
        self.galaxy[system.name] = system
        for _, planet in habitable_planets.items():
            self._adam(PIONERS, planet)
        return True

    def _is_habitable(self, system: System):
        return system.planets

    def _adam(self, pioners: int, planet: Planet):
        pass

    def _born_civ(self):
        pass

    def _display(self):
        for _, system in self.galaxy.items():
            display(system)

    def loop(self, apocalypse: int):
        year = 0
        while year < apocalypse:
            for _, system in self.galaxy.items():
                display(system)
            year += 1
