import sys

from adsimulo import __version__
from adsimulo.config import Config
from adsimulo.scripts.constants import GameModes
from adsimulo.scripts.utils import DefaultArgumentParser, game_mode
from adsimulo.settings import MENU_LOGO


def main():
    parser = DefaultArgumentParser()
    args = parser.parse_args()

    print(f"{MENU_LOGO}\n")
    print(f"Ad Simulo {__version__} by kafkaphoenix\n\n")

    mode = game_mode()
    if mode == GameModes.EXIT:
        sys.exit(0)
    Config.set(mode=mode, debug=args.debug, seed=args.seed, stop=args.year, noise=args.noise)
    Config.init_log()

    from adsimulo.game_master import GameMaster

    gm = GameMaster()
    gm.start()
