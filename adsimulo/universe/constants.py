from __future__ import annotations

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

    def biome_color(biome: Biomes) -> str:
        match biome.split():
            case [Biomes.BEACH]:
                color = "yellow"
            case [Biomes.DESERT]:
                color = "yellow"
            case [Biomes.FOREST]:
                color = "green"
            case [Biomes.GRASSLAND]:
                color = "green"
            case [Biomes.JUNGLE]:
                color = "cyan"
            case [Biomes.MOUNTAIN]:
                color = "magenta"
            case [Biomes.OCEAN]:
                color = "blue"
            case [Biomes.SNOW]:
                color = "white"
            case [Biomes.TUNDRA]:
                color = "grey"
            case _:
                Exception("Wrong biome\n")

        return color

    def biome(biome: Biomes) -> str:
        match biome.split():
            case [Biomes.BEACH]:
                description = "beach"
            case [Biomes.DESERT]:
                description = "desert"
            case [Biomes.FOREST]:
                description = "forest"
            case [Biomes.GRASSLAND]:
                description = "grassland"
            case [Biomes.JUNGLE]:
                description = "jungle"
            case [Biomes.MOUNTAIN]:
                description = "mountain"
            case [Biomes.OCEAN]:
                description = "ocean"
            case [Biomes.SNOW]:
                description = "snow"
            case [Biomes.TUNDRA]:
                description = "tundra"
            case _:
                Exception("Wrong biome\n")

        return description

    def expansion_cost(biome: Biomes) -> str:
        match biome.split():
            case [Biomes.BEACH]:
                cost = 0
            case [Biomes.DESERT]:
                cost = 8
            case [Biomes.FOREST]:
                cost = -10
            case [Biomes.GRASSLAND]:
                cost = -20
            case [Biomes.JUNGLE]:
                cost = 12
            case [Biomes.MOUNTAIN]:
                cost = 20
            case [Biomes.OCEAN]:
                Exception("No boats\n")
            case [Biomes.SNOW]:
                cost = 14
            case [Biomes.TUNDRA]:
                cost = 10
            case _:
                Exception("Wrong biome\n")

        return cost


SEA_LEVEL = 0.001


class Disaster(str, Enum):
    LANDSLIDE = "landslide"
    EARTHQUAKE = "earthquake"
    SINKHOLE = "sinkhole"
    VOLCANIC_ERUPTION = "volcanic eruption"
    FLOOD = "flood"
    TSUNAMI = "tsunami"
    TROPICAL_CYCLONE = "tropical cyclone"
    BLIZZARD = "blizzard"
    HAILSTORM = "hailstorm"
    ICE_STORM = "ice storm"
    COLD_WAVE = "cold wave"
    HEAT_WAVE = "heat wave"
    DROUGHT = "drought"
    THUNDERSTORM = "thunderstorm"
    TORNADO = "tornado"
    WILDFIRE = "wildfire"
    IMPACT_EVENT = "impact event"

    def __str__(self) -> str:
        return f"{self.value}"


class Stellar(str, Enum):
    BLUE = "O"
    DEEP_BLUE_WHITE = "B"
    BLUE_WHITE = "A"
    WHITE = "F"
    YELLOWISH_WHITE = "G"
    PALE_YELLOW_ORANGE = "K"
    LIGHT_ORANGE_RED = "M"

    def __str__(self) -> str:
        return f"{self.value}"

    def temperature(stellar: Stellar) -> int:
        match stellar.split():
            case [Stellar.BLUE]:
                t = 30000
            case [Stellar.DEEP_BLUE_WHITE]:
                t = 20000
            case [Stellar.BLUE_WHITE]:
                t = 8500
            case [Stellar.WHITE]:
                t = 6500
            case [Stellar.YELLOWISH_WHITE]:
                t = 5500
            case [Stellar.PALE_YELLOW_ORANGE]:
                t = 4000
            case [Stellar.LIGHT_ORANGE_RED]:
                t = 2500
            case _:
                Exception("Wrong stellar\n")

        return t

    def mass(stellar: Stellar) -> float:
        match stellar.split():
            case [Stellar.BLUE]:
                m = 16
            case [Stellar.DEEP_BLUE_WHITE]:
                m = 9
            case [Stellar.BLUE_WHITE]:
                m = 1.4
            case [Stellar.WHITE]:
                m = 1.04
            case [Stellar.YELLOWISH_WHITE]:
                m = 0.8
            case [Stellar.PALE_YELLOW_ORANGE]:
                m = 0.45
            case [Stellar.LIGHT_ORANGE_RED]:
                m = 0.08
            case _:
                Exception("Wrong stellar\n")

        return m
