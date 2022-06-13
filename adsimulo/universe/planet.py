from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pyfastnoisesimd as fns
from perlin_noise import PerlinNoise

from adsimulo.civ.contansts import CellState
from adsimulo.config import Config
from adsimulo.universe.constants import SEA_LEVEL, Biomes
from adsimulo.universe.utils import messy_noise, simd_noise
from adsimulo.universe.weather import Weather


@dataclass
class Planet:
    name: str = "PA-99-N2 b"
    symbol: str = "🜨"
    age: int = 0
    height: int = Config.game_settings["PLANET_HEIGHT"]
    width: int = Config.game_settings["PLANET_WIDTH"]
    terrain_grid: np.ndarray = field(init=False)
    civ_grid: np.ndarray = field(init=False)
    continentalness_index: np.ndarray = field(init=False)
    erosion_index: np.ndarray = field(init=False)
    peaks_valleys_index: np.ndarray = field(init=False)
    temperature_index: np.ndarray = field(init=False)
    humidity_index: np.ndarray = field(init=False)
    habitable: bool = False
    weather: Optional[Weather] = None

    def __post_init__(self):
        noise = Config.random_settings["NOISE"]
        if noise == "simd":
            self._simd_noise_indexes()
        elif noise == "perlin":
            self._perlin_noise_indexes()
        if self.weather is None:
            self.weather = Weather()
        self.terrain_grid = np.full(shape=[self.height, self.width], fill_value=Biomes.OCEAN.value, dtype=str)
        self.civ_grid = np.full(shape=[self.height, self.width], fill_value=CellState.UNOCCUPIED.value, dtype=str)
        self._biomes()
        self.habitable = self._habitability()

    def __repr__(self) -> str:
        return f"{self.name} [{self.symbol}]: Age {self.age}\n"

    def _simd_noise_indexes(self):
        self.continentalness_index = simd_noise(
            frequency=0.02,
            noiseType=fns.NoiseType.Perlin,
            octaves=4,
            lacunarity=5,
            gain=0.45,
            perturbType=fns.PerturbType.GradientFractal_Normalise,
            height=self.height,
            width=self.width,
        )
        self.erosion_index = simd_noise(
            frequency=0.02,
            noiseType=fns.NoiseType.Perlin,
            octaves=4,
            lacunarity=2.1,
            gain=0.45,
            perturbType=fns.PerturbType.Gradient,
            height=self.height,
            width=self.width,
        )
        peaks_valleys_index = simd_noise(
            frequency=0.06,
            noiseType=fns.NoiseType.Perlin,
            octaves=4,
            lacunarity=2.1,
            gain=0.45,
            perturbType=fns.PerturbType.NoPerturb,
            height=self.height,
            width=self.width,
        )
        peaks_valleys_index2 = simd_noise(
            frequency=0.07,
            noiseType=fns.NoiseType.Perlin,
            octaves=4,
            lacunarity=2.1,
            gain=0.45,
            perturbType=fns.PerturbType.GradientFractal_Normalise,
            height=self.height,
            width=self.width,
        )
        peaks_valleys_index3 = simd_noise(
            frequency=0.15,
            noiseType=fns.NoiseType.Perlin,
            octaves=10,
            lacunarity=2.1,
            gain=0.45,
            perturbType=fns.PerturbType.Gradient_Normalise,
            height=self.height,
            width=self.width,
        )
        self.peaks_valleys_index = peaks_valleys_index * 0.8 + peaks_valleys_index2 * 0.2 + peaks_valleys_index3 * 0.2
        temperature_index = simd_noise(
            frequency=0.02,
            noiseType=fns.NoiseType.Perlin,
            octaves=8,
            lacunarity=2.1,
            gain=0.45,
            perturbType=fns.PerturbType.NoPerturb,
            height=self.height,
            width=self.width,
        )
        temperature_index2 = simd_noise(
            frequency=0.02,
            noiseType=fns.NoiseType.Perlin,
            octaves=4,
            lacunarity=2.1,
            gain=0.45,
            perturbType=fns.PerturbType.NoPerturb,
            height=self.height,
            width=self.width,
        )
        self.temperature_index = temperature_index * 0.9 + temperature_index2 * 0.2
        self.humidity_index = simd_noise(
            frequency=0.5,
            noiseType=fns.NoiseType.PerlinFractal,
            octaves=4,
            lacunarity=2.1,
            gain=0.45,
            perturbType=fns.PerturbType.NoPerturb,
            height=self.height,
            width=self.width,
        )

    def _perlin_noise_indexes(self):
        self.continentalness_index = simd_noise(
            frequency=0.02,
            noiseType=fns.NoiseType.Perlin,
            octaves=4,
            lacunarity=5,
            gain=0.45,
            perturbType=fns.PerturbType.GradientFractal_Normalise,
            height=self.height,
            width=self.width,
        )
        self.erosion_index = None
        enoise = [
            PerlinNoise(octaves=4, seed=Config.rng.integers(1, 10000).item()),
            PerlinNoise(octaves=10, seed=Config.rng.integers(1, 10000).item()),
            PerlinNoise(octaves=20, seed=Config.rng.integers(1, 10000).item()),
        ]
        self.peaks_valleys_index = np.array(
            [
                [messy_noise([i / self.width, j / self.height], enoise) for i in range(self.width)]
                for j in range(self.height)
            ]
        )
        tnoise = [
            PerlinNoise(octaves=2, seed=Config.rng.integers(1, 10000).item()),
            PerlinNoise(octaves=4, seed=Config.rng.integers(1, 10000).item()),
            PerlinNoise(octaves=88, seed=Config.rng.integers(1, 10000).item()),
        ]
        self.temperature_index = np.array(
            [
                [messy_noise([i / self.width, j / self.height], tnoise) + 0.1 for i in range(self.width)]
                for j in range(self.height)
            ]
        )
        self.humidity_index = None

    def _biomes(self):
        for lat, long in np.ndindex(self.continentalness_index.shape):
            local_t = self.temperature_index[lat][long]
            local_e = self.peaks_valleys_index[lat][long]
            if local_e >= SEA_LEVEL and local_e < 0.100:  # next to oceans are beaches
                self.terrain_grid[lat][long] = Biomes.BEACH.value
            elif local_e > 0.4:  # if too tall, mountain by default
                self.terrain_grid[lat][long] = Biomes.MOUNTAIN.value
            elif local_e > SEA_LEVEL:  # if in a temperate region, determine biome based on climate
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

    def _habitability(self):
        return not np.all(self.terrain_grid == Biomes.OCEAN.value)
