from dataclasses import dataclass, field

from adsimulo.config import Config
from adsimulo.universe.constants import Stellar


@dataclass
class Star:
    name: str = "PA-99-N2"
    symbol: str = "☉"
    age: int = 0
    stellar: Stellar = field(init=False)

    def __post_init__(self):
        self.stellar = Config.rng.choice(list(Stellar))

    def __repr__(self) -> str:
        return f"{self.name} [{self.symbol}]: Age {self.age} - Stellar classification {self.stellar}\n"
