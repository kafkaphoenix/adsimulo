"""Agent which manages a planetary system."""

from time import sleep

from adsimulo.config import PIONERS
from adsimulo.planetary_system.planetary_system import PlanetarySystem
from adsimulo.utils import clear_shell


class Eva():
    """Simulation manager unit."""

    universe = {}

    def __init__(self, mode, debug, seed, year):
        """Initialize simulation project parameters for the planetary system.

        Initialize eva systems which the given arguments.

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
        self._system = None

    @staticmethod
    def big_bang():
        """Boom!."""
        print('Initializing universe...')
        sleep(0.3)
        print('Increasing simulation speed...')
        sleep(0.3)
        print('Superfast inflation...')
        sleep(0.3)
        print('Post inflation...')
        sleep(0.3)
        print('Cooling cosmos...')
        sleep(0.3)
        print('Atom era...')
        sleep(0.3)
        print('Entering into Galaxy era...')
        sleep(0.3)
        print('Fast-forwarding first galaxies and planetary systems...')
        sleep(0.3)
        print('First dying stars...')
        sleep(0.3)
        print('Slowing time...')

    def deploy(self):
        """Deploy Eva and start planetary system generation."""
        sleep(0.3)
        print('Cooling proto-star...')
        sleep(0.3)
        print('Cooling proto-planets...')
        self._planetary_system_formation()
        sleep(0.3)
        print("Analyzing planets' habitability...")
        sleep(0.3)
        habitable_planets = self._find_habitable_planets()
        if not habitable_planets:
            print('Failed to find habitable planets...')
            sleep(0.3)
            return False
        type(self).galaxy[self._system.name] = self._system
        for planet in habitable_planets:
            self._adam(PIONERS, planet)
        return True

    def _planetary_system_formation(self):
        """Create a planetary system with a star and planets."""
        system = PlanetarySystem()
        system.formation()
        self._system = system

    def _find_habitable_planets(self):
        """Return habitable planets."""
        return []

    def _adam(self, pioners, planet):
        """Early backers."""

    def _born_civ(self):
        """Born a new civilisation."""

    def display(self):
        """Draw planet map."""
        clear_shell()

    def hourglass(self):
        """Release the sands of time."""
