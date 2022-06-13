import logging
import os
from dataclasses import dataclass
from typing import ClassVar, Generator, Optional

import numpy as np

from adsimulo.scripts.constants import GameModes
from adsimulo.settings import DEBUG_SETTINGS, GAME_SETTINGS, RANDOM_SETTINGS


@dataclass
class Config:
    game_settings: ClassVar[dict[str]] = GAME_SETTINGS
    random_settings: ClassVar[dict[str]] = RANDOM_SETTINGS
    debug_settings: ClassVar[dict[str]] = DEBUG_SETTINGS
    rng: ClassVar[Generator] = np.random.default_rng(RANDOM_SETTINGS["SEED"])

    @classmethod
    def update_settings(
        cls,
        game_settings: dict[str],
        random_settings: dict[str],
        debug_settings: dict[str],
    ):
        cls.game_settings = game_settings
        cls.random_settings = random_settings
        cls.debug_settings = debug_settings
        cls.rng = np.random.default_rng(random_settings["SEED"])

    @classmethod
    def set(
        cls,
        mode: GameModes,
        debug: bool,
        seed: int,
        stop: int,
        noise: str,
    ):
        cls.game_settings["MODE"] = mode
        cls.game_settings["STOP"] = stop
        cls.debug_settings["DEBUG"] = debug
        cls.random_settings["SEED"] = seed
        cls.random_settings["NOISE"] = noise
        cls.rng = np.random.default_rng(seed)

    @classmethod
    def init_log(cls, path: Optional[str] = None):
        logging.basicConfig(
            filename=path or cls.debug_settings["FILENAME"],
            encoding="utf-8",
            filemode="w",
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s\n\t%(message)s",
            datefmt="%H:%M:%S",
            level=logging.DEBUG,
        )
        cls._clean_logs()

    @classmethod
    def _clean_logs(cls):
        if os.path.exists(cls.debug_settings["MAP_FILENAME"]):
            os.remove(cls.debug_settings["MAP_FILENAME"])
