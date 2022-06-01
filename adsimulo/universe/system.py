from dataclasses import dataclass, field
from typing import Dict

import numpy as np

from adsimulo.config import HEIGHT, WIDTH
from adsimulo.universe.planet import Planet
from adsimulo.universe.star import Star


@dataclass
class System:
    seed: int
    name: str = "Planetary system-1"
    star: Star = Star()
    planets: Dict[str, Planet] = field(default_factory=dict)

    def __post_init__(self):
        nplanets = np.random.randint(1, 2)
        for _ in range(nplanets):
            planet = Planet(height=HEIGHT, width=WIDTH, seed=self.seed)
            self.planets[planet.name] = planet
