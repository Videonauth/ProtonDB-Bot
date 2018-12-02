#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# ProtonDB-Bot - bot.py
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 01.12.18 - 06:30
# Purpose: -
# Written for: Python 3.6.3
# ---------------------------------------------------------------------------
"""
ProtonDB Bot - bot.py
---------------------
Chat-bot for ProtonDB Official Server

Second rewrite to version 0.0.17
"""

# system imports
import sys
import os
import time

# project library import
import modules.bot_core as core

_delta_time_start = time.time()
_runtime_path = f'{os.path.dirname(os.path.realpath(__file__))}/'
_extension_dir = f'extensions'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        pass
    print(f'{_runtime_path}{_extension_dir}')
    core.end_program(_delta_time_start, 0, time.time())
