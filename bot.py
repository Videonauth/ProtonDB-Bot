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
    bot.update({f'python_platform': sys.platform})
    bot.update({f'python version': str(sys.version).split(' ')[0]})
    bot.update({f'gcc_version': str(sys.version).split('\n')[1].strip('[]GC ')})

# ---------------------------------------------------------------------------
# Importing os and doing file and directory integrity checks.
# ---------------------------------------------------------------------------
try:
    import os
except ImportError:
    print(f'Could not import "os" library. Shutting down.')
    exit(1)
else:
    bot.update({f'runtime_path': os.path.dirname(os.path.realpath(__file__))})
    bot.update({f'name_self': str(__file__).strip('.').strip('/')})

# ---------------------------------------------------------------------------
# Importing logging
# ---------------------------------------------------------------------------
try:
    import logging
except ImportError:
    print(f'Could not import "logging" library. Shutting down.')
    exit(1)
else:
    bot.update({f'log_level': logging.DEBUG})

# ---------------------------------------------------------------------------
# Importing shutil
# ---------------------------------------------------------------------------
try:
    import shutil
except ImportError:
    print(f'Could not import "shutil" library. Shutting down.')
    exit(1)

# ---------------------------------------------------------------------------
#  Importing dependencies or install them if missing.
# TODO: implement
# ---------------------------------------------------------------------------
try:
    import requests
except ImportError:
    print(f'Could not import "requests" library. Shutting down.')
    exit(1)

# ---------------------------------------------------------------------------
# defining the input prompt the bot will use
# ---------------------------------------------------------------------------
bot.update({f'prompt': f'> '})

# ---------------------------------------------------------------------------
# defining the directory and file structure needed to load the bot.
# Each entry is a tuple of which first entry is the path to check and the
# second is the action to be taken if it not exists, the second part of the
# tuples are only relevant for the installation routine. directories are
# simple entries as they simply will get created.
# ---------------------------------------------------------------------------
bot.update({f'directories_expected': [
    f'config',
    f'modules',
    f'templates',
    f'logs',
    f'extensions-available',
    f'extensions-enabled',
]})
bot.update({f'files_expected': [
    [f'modules/core.py', f'install'],
    [f'templates/gitignore', f'install'],
    [f'.gitignore', f'create', f'templates/gitignore'],
    [f'LICENSE', f'install'],
    [f'extensions-available/example.py', f'install'],
]})

# ---------------------------------------------------------------------------
# Installation procedure (only makes sense when executing bot.py not on
# import.
# ---------------------------------------------------------------------------
if sys.argv and len(sys.argv) > 1:
    if sys.argv[1] == f'install':
        # Creating directories
        for _directory in bot.get(f'directories_expected'):
            if not os.path.exists(os.path.join(bot.get(f'runtime_path'), _directory)):
                try:
                    os.mkdir(os.path.join(bot.get(f'runtime_path'), _directory))
                except FileNotFoundError:
                    try:
                        os.makedirs(os.path.join(bot.get(f'runtime_path'), _directory))
                    except PermissionError:
                        print(f'Lacking permissions to create directories.')
                        exit(1)
                    else:
                        pass
                except FileExistsError:
                    pass
                except PermissionError:
                    print(f'Lacking permissions to create directories.')
                else:
                    pass
        # Create files
        for _name in bot.get(f'files_expected'):
            if not os.path.exists(os.path.join(bot.get(f'runtime_path'), _name[0])):
                if _name[1] == f'install':
                    _url = __github__ + _name[0]
                    _response = requests.get(url=_url)
                    if _response.status_code != 200:
                        print(f'The server sent {_response.status_code}. Shutting down.')
                        exit(1)
                    else:
                        try:
                            with open(os.path.join(bot.get(f'runtime_path'), _name[0]), mode='x') as _file:
                                _file.write(_response.text)
                        except FileExistsError:
                            try:
                                os.remove(os.path.join(bot.get(f'runtime_path'), _name[0]))
                                with open(os.path.join(bot.get(f'runtime_path'), _name[0]), mode='w') as _file:
                                    _file.write(_response.text)
                            except PermissionError:
                                print(f'Lacking permissions to create files.')
                                exit(1)
                        except PermissionError:
                            print(f'Lacking permissions to create files.')
                            exit(1)
                if _name[1] == f'create':
                    if len(_name) > 2:
                        if os.path.exists(os.path.join(bot.get(f'runtime_path'), _name[2])):
                            try:
                                shutil.copyfile(os.path.join(bot.get(f'runtime_path'), _name[2]),
                                                os.path.join(bot.get(f'runtime_path'), _name[0]))
                            except PermissionError:
                                print(f'Lacking permissions to create files.')
                                exit(1)
                        else:
                            _url = __github__ + _name[2]
                            _response = requests.get(url=_url)
                            if _response.status_code != 200:
                                print(f'The server sent {_response.status_code}. Shutting down.')
                                exit(1)
                            else:
                                try:
                                    with open(os.path.join(bot.get(f'runtime_path'), _name[0]), mode='x') as _file:
                                        _file.write(_response.text)
                                except FileExistsError:
                                    try:
                                        os.remove(os.path.join(bot.get(f'runtime_path'), _name[0]))
                                        with open(os.path.join(bot.get(f'runtime_path'), _name[0]), mode='w') as _file:
                                            _file.write(_response.text)
                                    except PermissionError:
                                        print(f'Lacking permissions to create files.')
                                        exit(1)
                                except PermissionError:
                                    print(f'Lacking permissions to create files.')
                                    exit(1)
else:
    for _directory in bot.get(f'directories_expected'):
        if not os.path.exists(os.path.join(bot.get(f'runtime_path'), _directory)):
            print(f'The bot is missing files it needs to run. Shutting down.')
            print(f'You can fix this by issuing "{bot.get("name_self")} install".')
            exit(1)
    for _file in bot.get(f'files_expected'):
        if not os.path.exists(os.path.join(bot.get(f'runtime_path'), _file[0])):
            print(f'The bot is missing files it needs to run. Shutting down.')
            print(f'You can fix this by issuing "{bot.get("name_self")} install".')
            exit(1)


if __name__ == '__main__':
    try:
        for _key, _value in bot.items():
            print(f'{_key}: {_value}')

        while True:
            break
    except KeyboardInterrupt:
        print(f'\nKeyboard interrupt detected. Shutting down.')
        exit(1)
    else:
        exit(0)
