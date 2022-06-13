from unittest.mock import patch

import numpy as np

from adsimulo.civ.utils import append2d, count_element2d
from adsimulo.config import Config


def test_instance(civilisation, planet):
    assert civilisation.home_planet is planet


def test_rise_rebels_ok(civilisation):
    new_territory = np.array([[2, 3], [2, 4]])
    expanded_territory = append2d(array=civilisation.territory, new_array=new_territory)
    civilisation.territory = expanded_territory
    civilisation.home_planet.civ_grid[2][3] = civilisation.emblem
    civilisation.home_planet.civ_grid[2][4] = civilisation.emblem
    expected_rebels = new_territory
    expected_territory = np.array([[0, 0]])

    rebels = civilisation._rise_rebels()

    assert len(rebels) == 2
    assert np.array_equal(rebels, expected_rebels)
    assert np.array_equal(civilisation.territory, expected_territory)
    assert count_element2d(civilisation.home_planet.civ_grid, civilisation.emblem) == 1
    assert type(civilisation).ncivs() == 1


def test_rise_warlords_ok(planet, civilisation):
    new_territory = np.array([[2, 3], [2, 4]])
    expanded_territory = append2d(array=civilisation.territory, new_array=new_territory)
    civilisation.territory = expanded_territory
    civilisation.home_planet.civ_grid[2][3] = civilisation.emblem
    civilisation.home_planet.civ_grid[2][4] = civilisation.emblem
    expected_rebels = new_territory
    expected_territory = np.array([[0, 0]])
    rebels = civilisation._rise_rebels()

    with patch.object(Config, "rng") as mocked_rng:
        mocked_rng.integers.return_value = 2
        mocked_rng.choice.return_value = expected_rebels
        new_civs = civilisation._rise_warlords(rebels)

        assert len(new_civs) == 2
        assert np.array_equal(rebels, expected_rebels)
        assert np.array_equal(civilisation.territory, expected_territory)
        assert np.array_equal(new_civs[0].territory, np.array([[2, 3]]))
        assert np.array_equal(new_civs[1].territory, np.array([[2, 4], [2, 2]]))  # expanded
        assert civilisation.home_planet.civ_grid[0][0] == civilisation.emblem
        assert civilisation.home_planet.civ_grid[2][3] == new_civs[0].emblem
        assert civilisation.home_planet.civ_grid[2][4] == new_civs[1].emblem
        assert civilisation.home_planet.civ_grid[2][2] == new_civs[1].emblem
        assert new_civs[0].home_planet.civ_grid[0][0] == civilisation.emblem
        assert new_civs[0].home_planet.civ_grid[2][3] == new_civs[0].emblem
        assert new_civs[0].home_planet.civ_grid[2][4] == new_civs[1].emblem
        assert new_civs[0].home_planet.civ_grid[2][2] == new_civs[1].emblem
        assert new_civs[1].home_planet.civ_grid[0][0] == civilisation.emblem
        assert new_civs[1].home_planet.civ_grid[2][3] == new_civs[0].emblem
        assert new_civs[1].home_planet.civ_grid[2][4] == new_civs[1].emblem
        assert new_civs[1].home_planet.civ_grid[2][2] == new_civs[1].emblem
        assert planet.civ_grid[0][0] == civilisation.emblem
        assert planet.civ_grid[2][3] == new_civs[0].emblem
        assert planet.civ_grid[2][4] == new_civs[1].emblem
        assert planet.civ_grid[2][2] == new_civs[1].emblem
        assert count_element2d(planet.civ_grid, civilisation.emblem) == 1
        assert count_element2d(planet.civ_grid, new_civs[0].emblem) == 1
        assert count_element2d(planet.civ_grid, new_civs[1].emblem) == 2
        assert type(civilisation).ncivs() == 3
        for civ in new_civs:
            type(civ).civ_slots.add(civ.emblem)


def test_rise_remnants_ok(planet, civilisation):
    new_territory = np.array([[2, 3], [2, 4]])
    expanded_territory = append2d(array=civilisation.territory, new_array=new_territory)
    civilisation.territory = expanded_territory
    civilisation.home_planet.civ_grid[2][3] = civilisation.emblem
    civilisation.home_planet.civ_grid[2][4] = civilisation.emblem
    expected_remnants = expanded_territory

    with patch.object(Config, "rng") as mocked_rng:
        mocked_rng.integers.return_value = 2
        mocked_rng.choice.return_value = expected_remnants
        new_civs = civilisation._rise_remnants()

        assert len(new_civs) == 3
        assert np.array_equal(new_civs[0].territory, np.array([[0, 0]]))
        assert np.array_equal(new_civs[1].territory, np.array([[2, 3]]))
        assert np.array_equal(new_civs[2].territory, np.array([[2, 4], [2, 2]]))  # expanded
        assert planet.civ_grid[0][0] == new_civs[0].emblem
        assert planet.civ_grid[2][3] == new_civs[1].emblem
        assert planet.civ_grid[2][4] == new_civs[2].emblem
        assert count_element2d(planet.civ_grid, civilisation.emblem) == 0
        assert count_element2d(planet.civ_grid, new_civs[0].emblem) == 1
        assert count_element2d(planet.civ_grid, new_civs[1].emblem) == 1
        assert count_element2d(planet.civ_grid, new_civs[2].emblem) == 2
        assert type(civilisation).ncivs() == 4
        for civ in new_civs:
            type(civ).civ_slots.add(civ.emblem)
