from dataclasses import dataclass, field

from adsimulo.config import Config
from adsimulo.eva import Eva


@dataclass
class GameMaster:
    deployed_evas: list[Eva] = field(default_factory=list)

    def start(self):
        """Create a simulation universe and deploy Evas.

        Select one galaxy and assign one Eva to each nebula suitable for
        a planetary system. Then Eva start the planetary system formation
        collapsing a nebula.
        """
        debug = Config.debug_settings["DEBUG"]
        lore = Config.debug_settings["LORE"]
        if not debug and lore:
            Eva.lore()
        deployed = 0
        while deployed < Config.game_settings["TOTAL_EVAS"]:
            eva = Eva()
            mission_status_ok = eva.deploy()
            if mission_status_ok:
                deployed += 1
            else:
                print("Discarding galaxy. Trying new one...")
            self.deployed_evas.append(eva)
        if debug:
            eva.stats()
        input("Simulation ready to start. Press any key to continue...")
        eva.loop()
        if debug:
            eva.stats()
