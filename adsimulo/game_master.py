"""Main agent which controls Ad Simulo initialization and execution."""

from adsimulo.config import PLANETARY_SYSTEMS_SAMPLE
from adsimulo.eva import Eva


class GameMaster():
    """A class to rule them all."""

    def __init__(self, mode, debug, seed, year):
        """Initialize Enuma Elis (public name Eden) simulation project parameters.

        Initialize game parameters which the given arguments.

        :param mode: 0 cpu mode, 1 one player vs cpu mode
        :type mode: int
        :param debug: Print debug information
        :type debug: bool
        :param seed: Initialize the random number generator
        :type seed: int
        :param year: Year when the simulation will end
        :type year: int
        """
        self._mode = mode
        self._debug = debug
        self._seed = seed
        self._year = year

    def start(self):
        """Create a simulation universe and deploy Evas.

        Select one galaxy and assign one Eva to each nebula suitable for
        a planetary system. Then Eva start the planetary system formation
        collapsing a nebula.
        """
        Eva.big_bang()
        n = 0
        while n < PLANETARY_SYSTEMS_SAMPLE:
            eva = Eva(self._mode, self._debug, self._seed, self._year)
            mission_status = eva.deploy()
            if mission_status:
                n += 1
            else:
                print('Discarding planetary system. Trying new one...')
        input('Simulation ready to start. Press any key to continue...')
        eva.display()
        eva.hourglass()
