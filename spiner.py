import itertools
import time


def spinner():
    """Show a simple spinner."""
    for spin in itertools.cycle('/-\|'):

        print(f'\r{spin}', end='', flush=True)
        time.sleep(0.2)