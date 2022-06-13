import numpy as np

from adsimulo.civ.contansts import CellState
from adsimulo.civ.utils import append2d, contains2d, count_element2d, delete2d, empty2d, filter2d, replace2d
from adsimulo.universe.constants import Biomes


def test_replace2d(planet):
    lat = long = 0
    planet.civ_grid[lat][long] = "A"

    replace2d(planet, [[lat, long]], CellState.UNOCCUPIED)

    assert planet.civ_grid[lat][long] == CellState.UNOCCUPIED.value


def test_delete2d():
    array = np.array([[1, 2], [3, 2], [2, 2]])
    element = np.array([1, 2])
    expected = np.array([[3, 2], [2, 2]])

    result = delete2d(array=array, element=element)

    assert np.array_equal(result, expected)


def test_append2d_one():
    array = np.array([[1, 2], [3, 2], [2, 2]])
    new_array = np.array([[2, 4]])
    expected = np.array([[1, 2], [3, 2], [2, 2], [2, 4]])

    result = append2d(array=array, new_array=new_array)

    assert np.array_equal(result, expected)


def test_append2d_several():
    array = np.array([[1, 2], [3, 2], [2, 2]])
    new_array = np.array([[2, 4], [4, 2]])
    expected = np.array([[1, 2], [3, 2], [2, 2], [2, 4], [4, 2]])

    result = append2d(array=array, new_array=new_array)

    assert np.array_equal(result, expected)


def test_contains2d_element():
    array = np.array([[1, 2], [3, 2], [2, 2]])
    element = np.array([1, 2])

    result = contains2d(array=array, element=element)

    assert result


def test_not_contains2d_element():
    array = np.array([[1, 2], [3, 2], [2, 2]])
    element = np.array([2, 1])

    result = contains2d(array=array, element=element)

    assert not result


def test_count_element2d():
    array = np.array([[1, 3, 2], [2, 2, 4]])
    element = 2

    result = count_element2d(array=array, element=element)

    assert result == 3


def test_empty2d():
    array = np.array([[], []])
    array2 = np.array([[]])

    result = empty2d(array=array)
    result2 = empty2d(array=array2)

    assert result
    assert result2


def test_not_empty2d():
    array = np.array([[3]])
    array2 = np.array([[3], [4]])

    result = empty2d(array=array)
    result2 = empty2d(array=array2)

    assert not result
    assert not result2


def test_filter2d():
    array = np.array(
        [
            [Biomes.DESERT.value, Biomes.JUNGLE.value, Biomes.OCEAN.value],
            [Biomes.JUNGLE.value, Biomes.BEACH.value, Biomes.JUNGLE.value],
        ]
    )

    result = filter2d(array=array, element=Biomes.JUNGLE.value)

    assert result == [(0, 1), (1, 0), (1, 2)]
