import logging

from adsimulo import __version__
from adsimulo.config import MENU_LOGO
from adsimulo.game_master import GameMaster
from adsimulo.scripts.utils import DefaultArgumentParser, select_mode


def main():
    parser = DefaultArgumentParser()
    args = parser.parse_args()

    logging.basicConfig(
        filename="lore.log",
        encoding="utf-8",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )

    print(f"{MENU_LOGO}\n")
    print(f"Ad Simulo {__version__} by kafkaphoenix\n\n")
    mode = select_mode()

    gm = GameMaster(mode=mode, debug=args.debug, seed=args.seed, apocalypse=args.year)
    gm.start()
