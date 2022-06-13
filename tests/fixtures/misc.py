import pytest

from tests.test_settings import DEBUG_SETTINGS, GAME_SETTINGS, RANDOM_SETTINGS


@pytest.fixture(scope="function", autouse=True)
def config():
    from adsimulo.config import Config

    Config.update_settings(GAME_SETTINGS, RANDOM_SETTINGS, DEBUG_SETTINGS)
    if Config.debug_settings["DEBUG"]:
        Config.init_log()
    return Config
