from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import ClassVar, Optional

import numpy as np

from adsimulo.civ.contansts import CIV_EMBLEMS, CellState, CivActions
from adsimulo.civ.history import History
from adsimulo.civ.profile import Profile
from adsimulo.civ.utils import (
    append2d,
    contains2d,
    count_element2d,
    delete2d,
    draw_civ,
    empty2d,
    find_civ,
    menu,
    replace2d,
    roll,
)
from adsimulo.config import Config
from adsimulo.universe.constants import Biomes
from adsimulo.universe.planet import Planet
from adsimulo.universe.weather import Weather

logger = logging.getLogger(__name__)


@dataclass
class Civilisation:
    name: str
    emblem: str
    origin: np.ndarray
    home_planet: Planet
    age: int = 0
    cpu: bool = True
    dead: bool = False
    profile: Profile = field(init=False)
    history: History = field(init=False)
    home_biome: Planet = field(init=False)
    territory: np.ndarray = field(init=False)
    civ_slots: ClassVar[set[str]] = set(CIV_EMBLEMS)
    eva = None

    def __post_init__(self):
        self.home_biome = self.home_planet.terrain_grid[self.origin[0]][self.origin[1]]
        self.territory = np.array([self.origin])
        self.profile = Profile()
        self.history = History()

    def __repr__(self) -> str:
        msg = (
            f"{self.name} [{self.emblem}] governs over {len(self.territory)} territories with its homeland biome"
            f" {Biomes.biome(self.home_biome)} from planet {self.home_planet.name}\n"
        )
        return msg

    @classmethod
    def born(cls, lat: int, long: int, planet: Planet, cpu: bool = True, expand: bool = False) -> Civilisation:
        """There is no salvation for us but to adopt Civilisation and lift ourselves down to its level."""
        if len(cls.civ_slots) == 0:
            if Config.debug_settings["DEBUG"]:
                logger.debug("Depleted emblem slots\n")
            return

        if planet.civ_grid[lat][long] != CellState.UNOCCUPIED:
            # raise Exception(f"WAIT! This should not happen")
            return

        sprout_emblem = cls.civ_slots.pop()
        planet.civ_grid[lat][long] = sprout_emblem
        sprout = cls(
            name=f"{sprout_emblem}",
            emblem=sprout_emblem,
            origin=np.array([lat, long]),
            home_planet=planet,
            cpu=cpu,
        )
        if cpu:
            logger.info(f"A new civilisation {sprout.name} appeared at {[lat, long]}\n")
        else:
            logger.info(f"A new civilisation {sprout.name} appeared at {[lat, long]} controlled by the player\n")
        if expand:
            sprout._expand()
        cls.eva.compendium.civilisations[sprout.emblem] = sprout

        return sprout

    def actions(self):
        """Civilisation is made -- or destroyed -- by its articulate voices."""
        self.profile.basepower = len(self.territory)
        base_actions = np.ceil(self.profile.basepower / 10 + 1)
        max_actions = np.ceil(self.profile.basepower / 5 + 1)
        curr_actions = Config.rng.integers(base_actions, max_actions + 1)
        if not self.cpu:
            print(
                f"Son of {self.name} [{self.emblem}] which is your next move?\n"
                f"Power: {self.profile.power:.2f} (Grow or expand to increase your power)\n"
                f"Territory: {self.profile.basepower} (Expanding requires 10 power)\n"
                f"Tech level: {self.profile.tech_level:.2f} (Development requires 20 power)\n"
                f"Instability: {self.profile.instability:.2f} (Decreasing instability is free)"
            )

        for n in range(curr_actions):
            if empty2d(self.territory):
                return
            if not self.cpu:
                print(f"\nYOU HAVE {curr_actions-n} ACTIONS REMAINING\n")
                action = menu()
            else:
                action = Config.rng.choice(self.profile.priorities)
            self._solve_action(action)

    def _solve_action(self, action: CivActions):
        if action == CivActions.TERRITORIAL_EXPANSION:
            if self.profile.power > 10:
                self.profile.power -= 10
                self._expand()
        elif action == CivActions.TECH_DEVELOPMENT:
            if self.profile.power > 20:
                self.profile.power -= 20
                self.profile.tech_level += roll("1d10") / 10
        elif action == CivActions.POPULATION_GROWTH:
            self.profile.power += self.profile.power * (roll("1d4") / 10)
        elif action == CivActions.TERRITORIAL_STABILIZATION:
            self.profile.instability *= Config.rng.random()

    def cadastre(self):
        """Order a real state's metes-and-bounds cadastral map to be set up."""
        if empty2d(self.territory):
            self._dissolve()
            return

        self.age += 1
        self.profile.basepower = len(self.territory)  # For each unit of land you hold you gain extra power
        self.profile.power += (
            self.profile.basepower * (0.8 + (roll("6d10") - roll("6d10") / 100))
            + self.profile.basepower * self.profile.tech_level * 3
        )  # National fortune = Fortune (normal distribution) + tech
        self.profile.power = min(self.profile.power, 1000000)
        self.profile.instability += (
            Config.rng.integers(1, np.ceil(self.profile.basepower / 10) + 1 + 1) - roll("3d6") - roll("3d6")
        )
        if roll("2d100") < self.profile.instability:
            if roll("1d6") == 1:
                self._dissolve()
                return

            if roll("1d6") < 4:
                self._collapse()
            else:
                self._collapse(natural=True)

    def _expand(self):
        """We must annex those people. We can afflict them with our wise and beneficent government."""
        for _ in range(Config.rng.integers(2, 6)):
            attempt = Config.rng.choice(self.territory)
            rng_number = 1
            long = Config.rng.integers(
                np.clip(attempt[1] - rng_number, a_min=0, a_max=self.home_planet.width - 1),
                np.clip(attempt[1] + rng_number, a_min=0, a_max=self.home_planet.width - 1) + 1,
            )
            lat = Config.rng.integers(
                np.clip(attempt[0] - rng_number, a_min=0, a_max=self.home_planet.height - 1),
                np.clip(attempt[0] + rng_number, a_min=0, a_max=self.home_planet.height - 1) + 1,
            )
            attempt_coord = self.home_planet.terrain_grid[lat][long]
            can_expand, civ = self._check_coord(attempt_coord, lat, long)
            if can_expand:
                if civ:
                    civ.territory = delete2d(civ.territory, [[lat, long]])
                    civ.home_planet.civ_grid[lat][long] = CellState.UNOCCUPIED
                self.home_planet.civ_grid[lat][long] = self.emblem
                self.territory = append2d(self.territory, [[lat, long]])
                self.profile.basepower = len(self.territory)

    def _check_coord(self, attempt_coord: Biomes, lat: int, long: int) -> tuple[bool, Optional[Civilisation]]:
        civ = None
        is_not_water = attempt_coord != Biomes.OCEAN.value
        not_territory = not contains2d(self.territory, [lat, long])
        if is_not_water and not_territory:
            c = 10 + max(50, 5 * self.profile.tech_level)  # Base 10% success chance, max +50% from technology
            if attempt_coord == self.home_biome:
                # Bonus chance if attempting to expand into base biome
                c += 20
            if self.home_planet.civ_grid[lat][long] != CellState.UNOCCUPIED.value:
                # Spreading into occupied squares is harder
                emblem = self.home_planet.civ_grid[lat][long]
                civ = find_civ(type(self).eva, emblem)
                c -= 5 + civ.profile.tech_level
            c -= Biomes.expansion_cost(self.home_planet.terrain_grid[lat][long])

            if roll("1d100") < c:
                return True, civ
        return False, None

    def _dissolve(self):
        """Every civilisation carries the seeds of its own destruction."""
        self.dead = True
        # at this point we lose the reference to the civ, this is intentional unless in the future is needed
        # in that case we will use dead variable
        del type(self).eva.compendium.civilisations[self.emblem]
        if not empty2d(self.territory):
            assert count_element2d(self.home_planet.civ_grid, self.emblem) == len(self.territory)
            logger.info(
                f"{self.name} [{self.emblem}] which governs over {len(self.territory)} territories has dissolved due to"
                f" instability! It lasted {self.age} years and achieved a tech level of {self.profile.tech_level:.2f}\n"
            )
            draw_civ(planet=self.home_planet, emblem=self.emblem, name=self.name)
            self._rise_remnants()
        else:
            assert count_element2d(self.home_planet.civ_grid, self.emblem) == 0
            logger.info(
                f"{self.name} [{self.emblem}] has dissolved after losing all its territory! It lasted {self.age} years"
                f" and achieved a tech level of {self.profile.tech_level:.2f}\n"
            )
        # for now remnants can't take dissolved civilisation emblems as theirs to avoid confusion
        type(self).civ_slots.add(self.emblem)

    def _collapse(self, natural: bool = False):
        """Look on my works, ye Mighty, and despair!."""
        if natural:
            disaster = Weather.disaster()
            logger.info(f"{self.name} [{self.emblem}] suffers a {disaster}!\n")
        logger.info(f"{self.name} [{self.emblem}] with powerbase {self.profile.basepower} is collapsing!\n")

        self.profile.instability += roll(f"{np.ceil(self.profile.basepower/10)}d6")
        self.profile.power /= Config.rng.integers(2, 5)

        rebels = self._rise_rebels()
        # rebels should try to join forces to overthrow tyran or create a new kingdom
        if not natural and len(rebels) > 0:
            # Natural disasters do not create new states, rebels eventually will be pacified but territory is lost
            self._rise_warlords(rebels)
        if empty2d(self.territory):
            self._dissolve()
            return

    def _rise_rebels(self) -> np.ndarray:
        n = Config.rng.integers(np.floor((len(self.territory)) / 1.5), len(self.territory))
        rebels = Config.rng.choice(self.territory, min(len(self.territory), n), replace=False)
        replace2d(self.home_planet, rebels, CellState.UNOCCUPIED)
        for rebel in rebels:
            logger.info(f"Rebels from {self.name} [{self.emblem}] have appeared at [{rebel[0]}, {rebel[1]}]!\n")
            self.territory = delete2d(self.territory, rebel)
        return rebels

    def _rise_warlords(self, rebels: np.ndarray) -> list[Optional[Civilisation]]:
        n = Config.rng.integers(1, np.ceil(self.profile.basepower / 10) + 1 + 1)
        warlords = Config.rng.choice(rebels, min(len(rebels), n), replace=False)
        new_civs = []
        for warlord in warlords:
            logger.info(
                f"Rebels from {self.name} [{self.emblem}] at [{warlord[0]}, {warlord[1]}] have chosen a warlord!\n"
            )
            new_civ = type(self).born(lat=warlord[0], long=warlord[1], planet=self.home_planet, expand=True)
            if new_civ:
                new_civs.append(new_civ)
            else:
                logger.info("They failed misserably...\n")
        return new_civs

    def _rise_remnants(self):
        n = Config.rng.integers(1, np.ceil(self.profile.basepower / 10) + 1 + 1)
        remnants = Config.rng.choice(self.territory, min(len(self.territory), n), replace=False)
        replace2d(self.home_planet, self.territory, CellState.UNOCCUPIED)
        self.territory = np.array([])
        new_civs = []
        for remnant in remnants:
            logger.info(f"Remnants from {self.name} [{self.emblem}] have appeared at [{remnant[0]}, {remnant[1]}]!\n")
            new_civ = type(self).born(lat=remnant[0], long=remnant[1], planet=self.home_planet, expand=True)
            if new_civ:
                new_civs.append(new_civ)
            else:
                logger.info("They could not survive...\n")
        return new_civs

    @classmethod
    def ncivs(cls) -> int:
        return len(CIV_EMBLEMS) - len(cls.civ_slots)

    @classmethod
    def stats(cls) -> str:
        logger.debug(f"{cls.ncivs()} civilisations(s)\n")
