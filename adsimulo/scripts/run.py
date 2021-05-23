"""Script to run Ad Simulo."""
from adsimulo.__version__ import __version__
from adsimulo.config import MENU_LOGO
from adsimulo.game_master import GameMaster
from adsimulo.scripts.utils import DefaultArgumentParser, select_game_mode


def main():
    """Start Ad Simulo."""
    parser = DefaultArgumentParser()
    args = parser.parse_args()

    print(f'{MENU_LOGO}\n')
    print(f'Ad Simulo {__version__} by kafkaphoenix\n\n')
    mode = select_game_mode()

    gm = GameMaster(mode=mode, debug=args.debug, seed=args.seed, year=args.year)
    gm.start()
