import logging
from dataclasses import dataclass, field

from adsimulo.civ.civ import Civilisation
from adsimulo.config import Config
from adsimulo.universe.galaxy import Galaxy
from adsimulo.utils import clear_shell, draw_map

logger = logging.getLogger(__name__)


@dataclass
class Compendium:
    galaxy: Galaxy = None
    civilisations: dict[str, Civilisation] = field(default_factory=dict)

    def display(self):
        clear_shell()
        if Config.debug_settings["DEBUG"]:
            print(f"{self.galaxy}")
        for _, system in self.galaxy.systems.items():
            if Config.debug_settings["DEBUG"]:
                print(f"{system}")
            for _, planet in system.planets.items():
                print(f"{planet}")
                if Config.debug_settings["DEBUG"]:
                    logger.debug("\n\t".join(str(p) for p in list(self.civilisations.values())))
                draw_map(planet)
