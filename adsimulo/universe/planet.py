from dataclasses import dataclass, field

import numpy as np
import pyfastnoisesimd as fns

from adsimulo.civ.contansts import CellState
from adsimulo.universe.constants import SEA_LEVEL, Biomes


@dataclass
class Planet:
    seed: int
    name: str = "Terra"
    symbol: str = "🜨"
    age: int = 0
    height: int = 40
    width: int = 40
    terrain_grid: np.ndarray = field(init=False)
    civ_grid: np.ndarray = field(init=False)
    continentalness_index: np.ndarray = field(init=False)
    erosion_index: np.ndarray = field(init=False)
    peaks_valleys_index: np.ndarray = field(init=False)
    temperature_index: np.ndarray = field(init=False)
    humidity_index: np.ndarray = field(init=False)

    def __post_init__(self):
        self._noise_indexes()
        self.terrain_grid = np.full(
            shape=[self.height, self.width], fill_value=Biomes.OCEAN.value
        )
        self.civ_grid = np.full(
            shape=[self.height, self.width], fill_value=CellState.UNOCCUPIED.value
        )
        self._biomes()

    def _noise_indexes(self):
        self.continentalness_index = self._noise(
            frequency=0.02,
            noiseType=fns.NoiseType.Perlin,
            octaves=4,
            lacunarity=5,
            gain=0.45,
            perturbType=fns.PerturbType.GradientFractal_Normalise,
        )
        self.erosion_index = self._noise(
            frequency=0.02,
            noiseType=fns.NoiseType.Perlin,
            octaves=4,
            lacunarity=2.1,
            gain=0.45,
            perturbType=fns.PerturbType.Gradient,
        )
        self.peaks_valleys_index = self._noise(
            frequency=0.02,
            noiseType=fns.NoiseType.Perlin,
            octaves=4,
            lacunarity=2.1,
            gain=0.45,
            perturbType=fns.PerturbType.NoPerturb,
        )
        self.temperature_index = self._noise(
            frequency=0.02,
            noiseType=fns.NoiseType.Perlin,
            octaves=4,
            lacunarity=2.1,
            gain=0.45,
            perturbType=fns.PerturbType.NoPerturb,
        )
        self.humidity_index = self._noise(
            frequency=0.02,
            noiseType=fns.NoiseType.Perlin,
            octaves=4,
            lacunarity=2.1,
            gain=0.45,
            perturbType=fns.PerturbType.NoPerturb,
        )

    def _noise(
        self,
        frequency: float,
        noiseType: fns.NoiseType,
        octaves: int,
        lacunarity: float,
        gain: float,
        perturbType: fns.PerturbType,
    ) -> np.ndarray:
        shape = [self.height, self.width]
        n = fns.Noise(seed=self.seed, numWorkers=4)
        n.frequency = frequency
        n.noiseType = noiseType
        n.fractal.octaves = octaves
        n.fractal.lacunarity = lacunarity
        n.fractal.gain = gain
        n.perturb.perturbType = perturbType
        return n.genAsGrid(shape=shape)

    def _biomes(self):
        for lat, long in np.ndindex(self.continentalness_index.shape):
            local_t = self.temperature_index[lat][long]
            local_e = self.erosion_index[lat][long]
            if local_e >= SEA_LEVEL and local_e < 0.100:  # next to oceans are beaches
                self.terrain_grid[lat][long] = Biomes.BEACH.value
            elif local_e > 0.4:  # if too tall, mountain by default
                self.terrain_grid[lat][long] = Biomes.MOUNTAIN.value
            elif (
                local_e > SEA_LEVEL
            ):  # if in a temperate region, determine biome based on climate
                if local_t < -0.2:
                    self.terrain_grid[lat][long] = Biomes.SNOW.value
                elif local_t < 0:
                    self.terrain_grid[lat][long] = Biomes.TUNDRA.value
                elif local_t < 0.1:
                    self.terrain_grid[lat][long] = Biomes.GRASSLAND.value
                elif local_t < 0.2:
                    self.terrain_grid[lat][long] = Biomes.FOREST.value
                elif local_t < 0.3:
                    self.terrain_grid[lat][long] = Biomes.JUNGLE.value
                else:
                    self.terrain_grid[lat][long] = Biomes.DESERT.value
