#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# ProtonDB-Bot - botcore.py
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 02.12.18 - 02:54
# Purpose: -
# Written for: Python 3.6.3
# ---------------------------------------------------------------------------

# system library imports
# import sys
import os
import time
import datetime
import json
import stat
# import requests
import logging
# import shutil
import subprocess
from contextlib import suppress

__version__ = f'0.0.17'


def bash_command(command: list) -> str or None:
    """
    Utility function for running external commands

    :param command: A list object containing the command.
    :return str or None: A string containing stdout or None.
    """
    _new_env = dict(os.environ)
    _new_env['LC_ALL'] = 'C'
    try:
        _stdout = subprocess.check_output(command, env=_new_env)
    except subprocess.CalledProcessError:
        return None
    else:
        if _stdout:
            return _stdout
        else:
            return None


def list_strip_all_newline(list_item: list) -> list:
    """
    Strips all newline characters '\n' from all list_items in list object.

    :param list_item: A list object to be cleaned from newline characters.
    :return list: A list object which has been cleaned.
    """
    return list(map(lambda x: x.strip('\n'), list_item))


def list_append_all_newline(list_item: list) -> list:
    """
    Appends a newline character '\n' to every list_item in list object.

    :param list_item: A list object to append newlines to.
    :return list: A list object with newlines appended.
    """
    return list(map(lambda x: f'{x}\n', list_item))


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


def dict_add(dict_item: dict, key: str, value) -> dict:
    """
    A synonym of dict_update. Simply passes along data. Remember keys are unique so if you pass an existing key
    you will simply update/replace it.

    :param dict_item: A dict object to be passed through to dict_update.
    :param key: A key value to be passed through to dict_update.
    :param value: The value to be passed through to dict_update.
    :return dict: The return value of dict_update
    """
    return dict_update(dict_item, key, value)


def dict_dump_stdout(dict_item: dict):
    """
    Dumps the given dictionary to stdout.

    :param dict_item: A dictionary to be dumped on screen.
    """
    for _key, _value in dict_item.items():
        print(f'{_key} = {_value}')


def dict_strip_quotes(dict_item: dict) -> dict:
    """
    Strips quote characters from dict values.

    :param dict_item: A dictionary to work with.
    :return dict: A dictionary with quotes stripped.
    """
    _output = dict()
    delimiter = '\"'
    for _key, _value in dict_item.items():
        _output.update({_key: _value.strip(delimiter)})
    _tmp = _output
    _output = dict()
    delimiter = '\''
    for _key, _value in _tmp.items():
        _output.update({_key: _value.strip(delimiter)})
    return _output


def dict_to_list(dict_item: dict, delimiter: str = '=') -> list:
    """
    Convert a dict object into a list object using delimiter as separator.

    :param dict_item: A dictionary to be converted.
    :param delimiter: A separating delimiter to use. Default is '='.
    :return list: A list object containing dict_item joined by delimiter.
    """
    _output = []
    for _key, _value in dict_item.items():
        _output.append(f'{_key}{delimiter}{_value}')
    return _output


def dict_get_key_by_value(dict_item: dict, value) -> str or None:
    """
    Finds a key associated to a value if present returns key or None otherwise.

    :param dict_item: A dictionary object to be searched in.
    :param value: The value to compare.
    :return str or None: A key as a string or None if not found.
    """
    for _key, _value in dict_item.items():
        if _value == value:
            return _key
    return None


def dict_get_value_for_key(dict_item, key):
    for _key, _value in dict_item.items():
        if _key == key:
            return _value
    return None


def dict_is_all_none(dict_item):
    for _key, _value in dict_item.items():
        if _value is not None:
            return False
    return True


def file_to_list(name):
    try:
        with open(name) as _infile:
            _lines = _infile.readlines()
    except PermissionError as error:
        print(f'{datetime.datetime.today()} {error}')
        exit(1)
    except FileNotFoundError as error:
        print(f'{datetime.datetime.today()} {error}')
        exit(1)
    else:
        return list_strip_all_newline(_lines)


def list_to_dict(list_item, delimiter='='):
    _output = dict()
    for _line in list_item:
        if not _line[0] == '#':
            _output.update({_line.split(delimiter)[0]: _line.split(delimiter)[1]})
    return _output


def dict_to_stdout(dict_item):
    for _key, _value in dict_item.items():
        print(f'{_key}: {_value}')
    return True


def list_to_stdout(list_item):
    for _line in list_item:
        print(f'{_line}')
    return True


def file_exists(name):
    return os.path.exists(name)


def file_to_dict(name):
    return list_to_dict(file_to_list(name))


def list_to_file(list_item, name):
    _time = time.time()
    list_item = list_append_all_newline(list_item)
    try:
        with open(name, 'x') as file:
            file.writelines(list_item)
    except FileExistsError:
        try:
            # os.rename(name, f'{name}.backup {datetime.datetime.today()}')
            os.remove(name)
            with open(name, 'w') as file:
                file.writelines(list_item)
        except PermissionError:
            print(f'Permissions missing for file: {name}')
            end_program(_time, 1, time.time())
        else:
            return True
    except PermissionError:
        print(f'Permissions missing for file: {name}')
        end_program(_time, 1, time.time())
    else:
        return True


def dict_to_file(dict_item, name):
    list_to_file(dict_to_list(dict_item), name)


def i_am_root():
    if os.getuid() is 0:
        return True
    else:
        return False


def who_am_i():
    return os.getuid()


def get_file_permissions(name):
    return stat.filemode(os.stat(name).st_mode)


def end_program(start_time: float, reason: int):
    """
    Ends the program and outputs the time the program has run

    :param start_time: Delta time from 'time' library taken when the program was started.
    :param reason: Return code to exit on.
    """
    print(f'\nProcess finished after {time.time() - start_time} seconds.')
    print(f'Process finished with exit code {reason}.')
    with suppress(SystemExit):
        exit(reason)


def json_to_dict(filename: str) -> dict:
    """
    Loads a .json file and returns a dictionary on success.

    :param filename: File name as a string (can include a path)
    :return: dictionary containing the json data on success
    """
    try:
        with open(filename, mode='r') as _file:
            _data = json.load(_file)
    except FileNotFoundError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    except PermissionError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    else:
        return _data


def dict_to_json(data: dict, filename: str):
    """
    Saves a dictionary into a json file

    :param data: Dictionary containing the data
    :param filename: File name for the json file (can contain a path)
    :return: Returns True on success
    """
    try:
        with open(filename, mode='x') as _file:
            json.dump(data, _file, indent=2, sort_keys=True)
    except FileExistsError:
        try:
            os.remove(filename)
            with open(filename, mode='w') as _file:
                json.dump(data, _file, indent=2, sort_keys=True)
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


def setup_logger(logger_name: str, log_file_name: str, level: int = logging.DEBUG):
    """
    Helper function for setting up different loggers.

    :param logger_name: System intern name for getLogger function
    :param log_file_name: File name for the log file
    :param level: logging object (<class 'int'>) defining the log level (by default it logs all logging.DEBUG)
    """
    _logger = logging.getLogger(logger_name)
    _formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    _file_handler = logging.FileHandler(log_file_name, mode='a')
    _file_handler.setFormatter(_formatter)
    _stream_handler = logging.StreamHandler()
    _stream_handler.setFormatter(_formatter)
    _logger.setLevel(level)
    _logger.addHandler(_file_handler)
    _logger.addHandler(_stream_handler)


if __name__ == '__main__':
    pass
