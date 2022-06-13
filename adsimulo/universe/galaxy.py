import logging
from dataclasses import dataclass, field
from functools import reduce

from adsimulo.config import Config
from adsimulo.universe.system import System

logger = logging.getLogger(__name__)


@dataclass
class Galaxy:
    name: str = "Andromeda"
    age: int = 0
    systems: dict[str, System] = field(default_factory=dict)

    def __post_init__(self):
        nsystems = Config.rng.integers(1, Config.game_settings["SYSTEM_SAMPLE"] + 1)
        for _ in range(nsystems):
            system = System()
            self.systems[system.name] = system

    def __repr__(self) -> str:
        return f"Galaxy {self.name}: Age {self.age}\nSystem(s):\n{list(self.systems.keys())}\n"

    def stats(self) -> str:
        nsystems = len(self.systems)
        nstars = reduce(sum, [len(system.stars) for system in self.systems.values()])
        nplanets = reduce(sum, [len(system.planets) for system in self.systems.values()])
        logger.debug(f"Galaxy {self.name}: {nsystems} system(s), {nstars} star(s), {nplanets} planet(s)\n")
