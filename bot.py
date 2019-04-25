#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# ProtonDB-Bot - bot.py
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 25.04.19 - 14:33
# Purpose: -
# Written for: Python 3.7.1
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Defining version variable and github link
# ---------------------------------------------------------------------------
__version__ = f'0.0.17'
__github__ = f'https://raw.githubusercontent.com/Videonauth/ProtonDB-Bot/{__version__}/'

# ---------------------------------------------------------------------------
# Data dictionary for the bot
# ---------------------------------------------------------------------------
dbot = dict()


# ---------------------------------------------------------------------------
# Dictionary helper functions. Do NOT use after importing core.
# ---------------------------------------------------------------------------
def add_to_dict(dictionary_item: dict, key: str, value) -> dict:
    """
    Adding a key,value pair to a dictionary then return it.

    :param dictionary_item:
    :param key:
    :param value:
    :return dict:
    """
    dictionary_item.update({key: value})
    return dictionary_item


# ---------------------------------------------------------------------------
# Importing time and fetching script start time. This has to stay on top.
# ---------------------------------------------------------------------------
try:
    import time
except ImportError:
    print(f'Could not import "time" library. Shutting down.')
    exit(1)
finally:
    dbot = add_to_dict(dbot, 'start_time', time.time())

# ---------------------------------------------------------------------------
# Importing sys and fetching python version and platform.
# ---------------------------------------------------------------------------
try:
    import sys
except ImportError:
    print(f'Could not import "sys" library. Shutting down.')
    exit(1)
finally:
    dbot = add_to_dict(dbot, 'python_version_raw', sys.version)
    dbot = add_to_dict(dbot, 'python_platform_raw', sys.platform)

# ---------------------------------------------------------------------------
# Importing os and doing file and directory integrity checks.
# ---------------------------------------------------------------------------
try:
    import os
except ImportError:
    print(f'Could not import "os" library. Shutting down.')
    exit(1)
finally:
    dbot = add_to_dict(dbot, f'runtime_path', f'{os.path.dirname(os.path.realpath(__file__))}/')
    dbot = add_to_dict(dbot, f'name_self', str(__file__).strip('.').strip('/'))

if __name__ == '__main__':
    try:
        print(dbot)
        while True:
            pass
    except KeyboardInterrupt:
        print(f'\nKeyboard interrupt detected. Shutting down.')
        exit(1)
    finally:
        exit(0)
