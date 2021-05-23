"""Module related with all the star generation stuff."""


class Star():
    """A class to build a star."""

    def __init__(self):
        """Initialize star parameters.

        :param name: star's name
        :type name: str
        :param symbol: star's symbol
        :type symbol: str
        :param age: star's age
        :type age: int
        """
        self._name = 'Aurora'  # TODO random star name generator
        self._symbol = '☉'  # TODO random symbol generator
        self._age = 0

    def formation(self):
        """Star formation."""

    @property
    def name(self):
        """Return star's name."""
        return self._name

    @property
    def symbol(self):
        """Return star's symbol."""
        return self._symbol

    @property
    def age(self):
        """Return star's age."""
        return self._age
