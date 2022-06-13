from dataclasses import dataclass, field

from adsimulo.civ.utils import roll


@dataclass
class Diplomacy:
    profile: dict[str, int] = field(default_factory=dict)
    relationships: dict[str, list] = field(default_factory=dict)

    def __post_init__(self):
        self.profile = {
            "friendliness": roll("1d100"),
            "trustworthiness": roll("1d100"),
            "fearfulness": roll("1d100"),
            "reputation": 0,
        }

    def make_alliance():
        pass
