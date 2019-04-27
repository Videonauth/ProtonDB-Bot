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
# Dictionary helper functions. Do NOT use after importing core.
# ---------------------------------------------------------------------------
def dict_update(dictionary_item: dict, key: str, value) -> dict:
    """
    Adding a key,value pair to a dictionary then return it.

    :param dictionary_item:
    :param key:
    :param value:
    :return dict:
    """
    dictionary_item.update({key: value})
    return dictionary_item


def dump_dict_pretty(dictionary_item: dict):
    """
    Dumps the given dictionary to st_out

    :param dictionary_item:
    """
    for _key, _value in dictionary_item.items():
        print(f'{_key} = {_value}')


# ---------------------------------------------------------------------------
# Importing time and fetching script start time. This has to stay on top.
# ---------------------------------------------------------------------------
try:
    import time
except ImportError:
    print(f'Could not import "time" library. Shutting down.')
    exit(1)
finally:
    bot = dict_update(bot, 'start_time', time.time())

# ---------------------------------------------------------------------------
# Importing sys and fetching python version and platform.
# ---------------------------------------------------------------------------
try:
    import sys
except ImportError:
    print(f'Could not import "sys" library. Shutting down.')
    exit(1)
finally:
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
finally:
    bot = dict_update(bot, f'runtime_path', f'{os.path.dirname(os.path.realpath(__file__))}/')
    bot = dict_update(bot, f'name_self', str(__file__).strip('.').strip('/'))

# ---------------------------------------------------------------------------
#  Importing requests
# ---------------------------------------------------------------------------
try:
    import requests
except ImportError:
    print(f'Could not import "requests" library. Shutting down.')
    exit(1)


# ---------------------------------------------------------------------------
# Importing logging
# ---------------------------------------------------------------------------
try:
    import logging
except ImportError:
    print(f'Could not import "logging" library. Shutting down.')
    exit(1)
finally:
    bot = dict_update(bot, f'log_level', logging.DEBUG)

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
    finally:
        pass


def write_to_file(file: str, content: str):
    try:
        with open(file, mode='x') as _file:
            _file.write(content)
    except FileExistsError:
        try:
            os.remove(file)
            with open(file, mode='w') as _file:
                _file.write(content)
        except PermissionError:
            print(f'Lacking permission to create files. Shutting down.')
            exit(1)
    except PermissionError:
        print(f'Lacking permission to create files. Shutting down.')
        exit(1)


# ---------------------------------------------------------------------------
# Installation procedure (only makes sense when executing bot.py not on
# import, thus running in its own main request
# ---------------------------------------------------------------------------
if __name__ == '__main__':
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
                print(f'Do you want to install now?')
                print(f'[y/n][yes/no] return for [n/no]')
                _input = input(bot.get('prompt'))
                if _input == '':
                    print(f'Shutting down.')
                    exit(0)
                elif _input == 'n' or _input == 'no':
                    print(f'Shutting down.')
                    exit(0)
                elif _input == 'y' or _input == 'yes':
                    create_dir(f'{bot.get("runtime_path") + _directory[0]}')
                else:
                    print(f'Not expected input. Shutting down.')
                    exit(1)
            if _directory[1] == f'create':
                create_dir(f'{bot.get("runtime_path") + _directory[0]}')

    for _name in bot.get('files_expected'):
        if not os.path.exists(bot.get('runtime_path') + _name[0]):
            if _name[1] == f'install':
                _url = __github__ + _name[0]
                _content = requests.get(url=_url)
                print(f'Installing "{_name[0]}" from "{_url}".')
                write_to_file(f'{bot.get("runtime_path") + _name[0]}', str(_content.text))
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
                    write_to_file(f'{bot.get("runtime_path") + _name[0]}', str(_content.text))


if __name__ == '__main__':
    try:
        # dict_dump_stdout(bot)
        while True:
            break
    except KeyboardInterrupt:
        print(f'\nKeyboard interrupt detected. Shutting down.')
        exit(1)
    finally:
        exit(0)
