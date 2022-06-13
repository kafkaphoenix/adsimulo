import numpy as np
import pyfastnoisesimd as fns

from adsimulo.config import Config


def simd_noise(
    frequency: float,
    noiseType: fns.NoiseType,
    octaves: int,
    lacunarity: float,
    gain: float,
    perturbType: fns.PerturbType,
    height: int,
    width: int,
) -> np.ndarray:
    shape = [height, width]
    n = fns.Noise(seed=Config.random_settings["SEED"], numWorkers=4)
    n.frequency = frequency
    n.noiseType = noiseType
    n.fractal.octaves = octaves
    n.fractal.lacunarity = lacunarity
    n.fractal.gain = gain
    n.perturb.perturbType = perturbType
    return n.genAsGrid(shape=shape)


def messy_noise(factor: list, noise: list):
    """Make something specially noisy."""
    return noise[0](factor) + 0.5 * noise[1](factor) + 0.25 * noise[2](factor)
