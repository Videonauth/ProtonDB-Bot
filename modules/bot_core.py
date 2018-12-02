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


def end_program(start_time, reason, stop_time):
    print(f'Process finished after {stop_time - start_time} seconds.')
    print(f'Process finished with exit code {reason}.')
    exit(reason)


if __name__ == '__main__':
    pass
