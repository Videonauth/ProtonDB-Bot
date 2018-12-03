#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# ProtonDB-Bot - bot_core.py
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
# import time
import datetime
import json
# import requests
import logging
from contextlib import suppress


def end_program(start_time: float, reason: int, stop_time: float):
    """
    Ends the program and outputs the time the program has run

    :param start_time: Delta time from 'time' library taken when the program was started.
    :param reason: Return code to exit on.
    :param stop_time: Delta time from 'time' library taken when this function was called.
    """
    print(f'\nProcess finished after {stop_time - start_time} seconds.')
    print(f'Process finished with exit code {reason}.')
    with suppress(SystemExit):
        exit(reason)


def json_to_dict(filename: str):
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


def setup_logger(logger_name: str, log_file_name: str, level: int =logging.DEBUG):
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
