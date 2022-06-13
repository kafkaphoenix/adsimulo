from dataclasses import dataclass, field

from adsimulo.civ.contansts import CivActions
from adsimulo.civ.diplomacy import Diplomacy
from adsimulo.civ.utils import roll
from adsimulo.config import Config


@dataclass
class Profile:
    instability: float = -10
    power: float = 10
    basepower: float = 1
    tech_level: float = 0
    priorities: list = field(init=False)
    diplomacy: Diplomacy = field(init=False)

    def __post_init__(self):
        self.priorities = [item for priority in list(CivActions) for item in (priority,) * Config.rng.integers(1, 9)]
        self.power = roll("3d10")
        self.diplomacy = Diplomacy()
