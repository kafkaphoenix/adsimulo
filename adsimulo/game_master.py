from dataclasses import dataclass

import numpy as np

from adsimulo.config import PLANETARY_SYSTEMS_SAMPLE
from adsimulo.eva import Eva


@dataclass
class GameMaster:
    mode: int
    debug: bool
    seed: int
    apocalypse: int

    def __post_init__(self):
        np.random.seed(self.seed)

    def start(self):
        """Create a simulation universe and deploy Evas.

        Select one galaxy and assign one Eva to each nebula suitable for
        a planetary system. Then Eva start the planetary system formation
        collapsing a nebula.
        """
        if not self.debug:
            Eva.lore()
        n = 0
        while n < PLANETARY_SYSTEMS_SAMPLE:
            eva = Eva(seed=self.seed)
            mission_status = eva.deploy()
            if mission_status:
                n += 1
            else:
                print("Discarding planetary system. Trying new one...")
        input("Simulation ready to start. Press any key to continue...")
        eva.loop(self.apocalypse)
