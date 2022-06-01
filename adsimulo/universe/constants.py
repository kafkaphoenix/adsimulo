from enum import Enum


class Biomes(str, Enum):
    BEACH = "b"
    DESERT = "d"
    FOREST = "f"
    GRASSLAND = "g"
    JUNGLE = "j"
    MOUNTAIN = "m"
    OCEAN = "~"
    SNOW = "s"
    TUNDRA = "t"


biome_colors = {
    Biomes.BEACH: "yellow",
    Biomes.DESERT: "yellow",
    Biomes.FOREST: "green",
    Biomes.GRASSLAND: "green",
    Biomes.JUNGLE: "cyan",
    Biomes.MOUNTAIN: "magenta",
    Biomes.OCEAN: "blue",
    Biomes.SNOW: "white",
    Biomes.TUNDRA: "white",
}

SEA_LEVEL = 0.001

DISASTERS = [
    "landslide",
    "earthquake",
    "sinkhole",
    "volcanic eruption",
    "flood",
    "tsunami",
    "tropical cyclone",
    "blizzard",
    "hailstorm",
    "ice storm",
    "cold wave",
    "heat wave",
    "drought",
    "thunderstorm",
    "tornado",
    "wildfire",
    "impact event",
]
