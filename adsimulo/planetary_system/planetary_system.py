"""Module related with all the planetary system generation stuff."""

from random import randint

from adsimulo.config import HEIGHT, WIDTH
from adsimulo.planetary_system.planet import Planet
from adsimulo.planetary_system.star import Star


class PlanetarySystem():
    """A class to build a planetary system."""

    def __init__(self):
        """Initialize planetary system parameters.

        :param name: planetary system's name
        :type name: str
        :param star: planetary system's star
        :type star: Star
        :param planets: planetary system's planets
        :type planets: dict
        """
        self._name = 'Planetary system-1'  # TODO random planetary system name generator
        self._star = None
        self._planets = {}

    def formation(self):
        """Born a star and start planets' formation."""
        star = Star()
        star.formation()
        self._star = star
        nplanets = randint(1, 1)
        for _ in range(nplanets):
            planet = Planet(height=HEIGHT, width=WIDTH)
            planet.formation()
            self._planets[planet.name] = planet

    @property
    def name(self):
        """Return planetary system name."""
        return self._name
