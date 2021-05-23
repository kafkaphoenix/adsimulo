"""Module related with all the planet generation stuff."""


class Planet():
    """A class to build a planet."""

    def __init__(self, height, width):
        """Initialize planet parameters.

        :param name: Planet's name
        :type name: str
        :param symbol: Planet's symbol
        :type symbol: str
        :param age: Planet's age
        :type age: int
        :param height: Planet's height
        :type height: int
        :param width: Planet's width
        :type width: int
        :param tgrid: Planet's topographic grid
        :type tgrid: list
        :param cgrid: Planet's civilisation grid
        :type cgrid: list
        """
        self._name = 'Terra'  # TODO random planet name generator
        self._symbol = '🜨'  # TODO random symbol generator
        self._age = 0
        self._height = height
        self._width = width
        self._tgrid = None
        self._cgrid = None

    def formation(self):
        """Planet formation.

        In the beginning Python created the heavens and the earth.
        Generate world structure, temperature map, elevation map and
        fill world with biomes.
        """

    @property
    def name(self):
        """Return planet's name."""
        return self._name

    @property
    def symbol(self):
        """Return planet's symbol."""
        return self._symbol

    @property
    def age(self):
        """Return planet's age."""
        return self._age
