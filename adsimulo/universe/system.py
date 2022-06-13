from dataclasses import dataclass, field

from adsimulo.config import Config
from adsimulo.universe.planet import Planet
from adsimulo.universe.star import Star


@dataclass
class System:
    name: str = "PA-99-N2 System"
    age: int = 0
    stars: dict[str, Star] = field(default_factory=dict)
    planets: dict[str, Planet] = field(default_factory=dict)

    def __post_init__(self):
        nstars = Config.rng.integers(1, Config.game_settings["STAR_SAMPLE"] + 1)
        for _ in range(nstars):
            star = Star()
            self.stars[star.name] = star
        nplanets = Config.rng.integers(1, Config.game_settings["PLANET_SAMPLE"] + 1)
        for _ in range(nplanets):
            planet = Planet()
            self.planets[planet.name] = planet

    def __repr__(self) -> str:
        return (
            f"System {self.name}: Age"
            f" {self.age}\nStar(s):\n{list(self.stars.keys())}\nPlanet(s):\n{list(self.planets.keys())}\n"
        )

    def habitable_planets(self) -> list[Planet]:
        return [planet for planet in self.planets.values() if planet.habitable]
