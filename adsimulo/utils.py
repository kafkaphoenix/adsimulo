"""Miscellaneous adsimulo methods."""

import os
from platform import system

from adsimulo.config import LOGFILE_PATH


def log(line):
    """Append output stream to a file."""
    with open(LOGFILE_PATH, 'a') as file:
        file.write(''.join(line + '\n'))


def clamp(val, nmin=0, nmax=1):
    """Restrict value between nmin and nmax."""
    return max(nmin, min(val, nmax))


def clear_shell():
    """Clear shell."""
    os_system = system()
    if os_system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
