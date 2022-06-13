from dataclasses import dataclass

from adsimulo.config import Config
from adsimulo.universe.constants import Disaster


@dataclass
class Weather:
    @staticmethod
    def disaster() -> str:
        return Config.rng.choice(list(Disaster))
