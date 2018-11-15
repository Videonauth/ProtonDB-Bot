#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# ProtonDB Bot - core.py
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 09.11.18 - 15:01
# Purpose: -
# Written for: Python 3.6.3
# ---------------------------------------------------------------------------

# External imports
import os
import datetime
import stat
import time

# Local imports


def strip_newline(lines):
    return list(map(lambda x: x.strip('\n'), lines))


def append_newline(lines):
    return list(map(lambda x: f'{x}\n', lines))


def end_program(start_time, reason, stop_time):
    print(f'Process finished after {stop_time - start_time} seconds.')
    print(f'Process finished with exit code {reason}.')
    exit(reason)


def strip_quotes_from_dict(dictionary_item):
    _output = dict()
    delimiter = '\"'
    for _key, _value in dictionary_item.items():
        _output.update({_key: _value.strip(delimiter)})
    _tmp = _output
    _output = dict()
    delimiter = '\''
    for _key, _value in _tmp.items():
        _output.update({_key: _value.strip(delimiter)})
    return _output


def dict_to_list(dictionary_item, delimiter='='):
    _output = []
    for _key, _value in dictionary_item.items():
        _output.append(f'{_key}{delimiter}{_value}')
    return _output


def dict_get_key_for_value(dictionary_item, value):
    for _key, _value in dictionary_item.items():
        if _value == value:
            return _key
    return None


def dict_get_value_for_key(dictionary_item, key):
    for _key, _value in dictionary_item.items():
        if _key == key:
            return _value
    return None


def dict_is_all_none(dictionary_item):
    for _key, _value in dictionary_item.items():
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
        return strip_newline(_lines)


def list_to_dict(list_item, delimiter='='):
    _output = dict()
    for _line in list_item:
        if not _line[0] == '#':
            _output.update({_line.split(delimiter)[0]: _line.split(delimiter)[1]})
    return _output


def dict_to_stdout(dictionary_item):
    for _key, _value in dictionary_item.items():
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
    list_item = append_newline(list_item)
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


def dict_to_file(dictionary_item, name):
    list_to_file(dict_to_list(dictionary_item), name)


def i_am_root():
    if os.getuid() is 0:
        return True
    else:
        return False


def who_am_i():
    return os.getuid()


def get_file_permissions(name):
    # TODO: parse the permissions to a proper format (get_file_permissions)
    return stat.filemode(os.stat(name).st_mode)


if __name__ == '__main__':
    pass
