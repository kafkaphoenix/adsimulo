import numpy as np

from adsimulo.universe.constants import Biomes


def test_instance(planet, weather):
    assert planet.weather is weather


def test_habitability_ok(planet):
    planet.terrain_grid = np.full(shape=[planet.height, planet.width], fill_value=Biomes.OCEAN.value, dtype=str)

    assert planet._habitability() is False
