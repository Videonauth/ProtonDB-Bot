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
bot = dict()

# ---------------------------------------------------------------------------
# Importing time and fetching script start time. This has to stay on top.
# ---------------------------------------------------------------------------
try:
    import time
except ImportError:
    print(f'Could not import "time" library. Shutting down.')
    exit(1)
else:
    bot.update({'start_time': time.time()})


# ---------------------------------------------------------------------------
# Dictionary helper functions. Do NOT use after importing core. Theses are
# mere copies of functions contained in core.py
# ---------------------------------------------------------------------------
def dict_update(dict_item: dict, key: str, value) -> dict:
    """
    Updating a key,value pair to a dictionary then return it. Remember keys are unique so if you not pass the exact key
    you wil generate a new one.

    :param dict_item: A dict object to be changed.
    :param key: Key to be changed.
    :param value: Value to be inserted into key.
    :return dict: The changed dict object.
    """
    dict_item.update({key: value})
    return dict_item


def dict_to_stdout(dict_item: dict) -> bool:
    """
    Prints the dict objects contents to screen.

    :param dict_item: A dict object to print out.
    :return bool: True on finish.
    """
    for _key, _value in dict_item.items():
        print(f'{_key}: {_value}')
    return True


# ---------------------------------------------------------------------------
# Importing datetime for providing in error output.
# ---------------------------------------------------------------------------
try:
    import datetime
except ImportError:
    print(f'Could not import "datetime" library. Shutting down.')
    exit(1)


# ---------------------------------------------------------------------------
# Importing sys and fetching python version and platform.
# ---------------------------------------------------------------------------
try:
    import sys
except ImportError:
    print(f'Could not import "sys" library. Shutting down.')
    exit(1)
else:
    bot = dict_update(bot, f'python_platform', sys.platform)
    bot = dict_update(bot, f'python_version', str(sys.version).split(' ')[0])
    bot = dict_update(bot, f'gcc_version', str(sys.version).split('\n')[1].strip('[]GC '))

# ---------------------------------------------------------------------------
# Importing os and doing file and directory integrity checks.
# ---------------------------------------------------------------------------
try:
    import os
except ImportError:
    print(f'Could not import "os" library. Shutting down.')
    exit(1)
else:
    bot = dict_update(bot, f'runtime_path', f'{os.path.dirname(os.path.realpath(__file__))}/')
    bot = dict_update(bot, f'name_self', str(__file__).strip('.').strip('/'))

# ---------------------------------------------------------------------------
# Importing logging
# ---------------------------------------------------------------------------
try:
    import logging
except ImportError:
    print(f'Could not import "logging" library. Shutting down.')
    exit(1)
else:
    bot = dict_update(bot, f'log_level', logging.DEBUG)

# ---------------------------------------------------------------------------
# Importing shutil
# ---------------------------------------------------------------------------
try:
    import shutil
except ImportError:
    print(f'Could not import "shutil" library. Shutting down.')
    exit(1)


def create_dir(path: str, permission: oct = 0o700):
    """
    Creates a directory.

    :param path:
    :param permission:
    :return:
    """
    try:
        print(f'Creating "{path}" directory.')
        os.mkdir(f'{path}', mode=permission)
    except PermissionError:
        print(f'Lacking permission to create directories. Shutting down.')
        exit(1)
    else:
        pass


def raw_to_file(filename: str, raw: str) -> bool:
    """
    Saves raw data to file.

    :param filename: the path to be saved to.
    :param raw: The content for the file.
    :return bool: True on success.
    """
    try:
        with open(filename, mode='x') as _file:
            _file.write(raw)
    except FileExistsError:
        try:
            os.remove(filename)
            _file.write(raw)
        except PermissionError as _error:
            print(f'{datetime.datetime.today()} {_error}')
            exit(1)
        else:
            return True
    except PermissionError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    else:
        return True


# ---------------------------------------------------------------------------
#  Importing requests (dependency)
# ---------------------------------------------------------------------------
try:
    import requests
except ImportError:
    print(f'Could not import "requests" library. Shutting down.')
    exit(1)

# ---------------------------------------------------------------------------
# Installation procedure (only makes sense when executing bot.py not on
# import, thus running in its own main request
# ---------------------------------------------------------------------------
_install = False

if sys.argv and len(sys.argv) > 1:
    if sys.argv[1] == f'install':
        _install = True

if __name__ == '__main__' and _install:
    bot = dict_update(bot, f'directories_expected', [
        [f'config', f'setup'],
        [f'modules', f'create'],
        [f'templates', f'create'],
        [f'logs', f'create'],
        [f'extensions-available', f'create'],
        [f'extensions-enabled', f'create'],
    ])
    bot = dict_update(bot, f'files_expected', [
        [f'modules/botcore.py', f'install'],
        [f'templates/gitignore', f'install'],
        [f'.gitignore', f'create', f'templates/gitignore'],
        [f'LICENSE', f'install'],
        [f'extensions-available/example.py', f'install'],
    ])
    bot = dict_update(bot, f'prompt', f'> ')

    for _directory in bot.get('directories_expected'):
        if not os.path.exists(bot.get('runtime_path') + _directory[0]):
            if _directory[1] == f'setup':
                create_dir(f'{bot.get("runtime_path") + _directory[0]}')
            if _directory[1] == f'create':
                create_dir(f'{bot.get("runtime_path") + _directory[0]}')

    for _name in bot.get('files_expected'):
        if not os.path.exists(bot.get('runtime_path') + _name[0]):
            if _name[1] == f'install':
                _url = __github__ + _name[0]
                _content = requests.get(url=_url)
                print(f'Installing "{_name[0]}" from "{_url}".')
                raw_to_file(f'{bot.get("runtime_path") + _name[0]}', str(_content.text))
            if _name[1] == f'create':
                if os.path.exists(f'{bot.get("runtime_path") + _name[2]}'):
                    print(f'Copying file "{bot.get(f"runtime_path") + _name[2]}" to ' +
                          f'"{bot.get(f"runtime_path") + _name[0]}".')
                    shutil.copyfile(f'{bot.get("runtime_path") + _name[2]}',
                                    f'{bot.get("runtime_path") + _name[0]}',
                                    follow_symlinks=False)
                elif not os.path.exists(f'{bot.get("runtime_path") + _name[2]}'):
                    _url = __github__ + _name[2]
                    _content = requests.get(url=_url)
                    print(f'Installing "{_name[0]}" from "{_url}".')
                    raw_to_file(f'{bot.get("runtime_path") + _name[0]}', str(_content.text))


if __name__ == '__main__':
    try:
        dict_to_stdout(bot)
        while True:
            break
    except KeyboardInterrupt:
        print(f'\nKeyboard interrupt detected. Shutting down.')
        exit(1)
    else:
        exit(0)
