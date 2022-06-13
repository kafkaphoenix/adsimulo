import pytest

from adsimulo.civ.civ import Civilisation
from adsimulo.compendium import Compendium
from adsimulo.eva import Eva
from adsimulo.universe.planet import Planet
from adsimulo.universe.star import Star
from adsimulo.universe.system import System
from adsimulo.universe.weather import Weather


@pytest.fixture(scope="function")
def star():
    instance = Star()

    return instance


@pytest.fixture(scope="function")
def weather():
    instance = Weather()

    return instance


@pytest.fixture(scope="function")
def planet(weather):
    instance = Planet(weather=weather)

    return instance


@pytest.fixture(scope="function")
def system(star, planet):
    instance = System(stars={f"{star.name}": star}, planets={f"{planet.name}": planet})

    return instance


@pytest.fixture(scope="function")
def civilisation(planet):
    Civilisation.eva = Eva()
    instance = Civilisation.born(lat=0, long=0, planet=planet)

    yield instance

    Civilisation.civ_slots.add(instance.emblem)


@pytest.fixture(scope="function")
def compendium(system, civilisation):
    instance = Compendium(galaxy={f"{system.name}": system}, civilisations={f"{civilisation.name}": civilisation})

    yield instance


@pytest.fixture(scope="function")
def eva(compendium):
    instance = Eva(compendium=compendium)

    return instance
