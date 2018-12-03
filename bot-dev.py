#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# ProtonDB-Bot - bot-dev.py
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

# system library imports
# import sys
import os
import time
# import datetime
# import json
# import requests
import logging
# from contextlib import suppress
import re

# dependency library import
# import discord
from discord.ext.commands import Bot
# from bs4 import BeautifulSoup as Soup
import steamfront
# from steamfront import errors

# project library import
import modules.botcore as core

# define debug mode
_debug_mode = True

# set log level (possible options DEBUG, INFO, WARNING, ERROR, CRITICAL)
_log_level = logging.DEBUG

# define version string
__version__ = '0.0.17'

# exit flag
_exit_flag = False

# fetching start time
_delta_time_start = time.time()

# url constants (only change if you know what you're doing)
_google_url = 'https://www.google.com/search?safe=off&q='
_steam_url = 'https://store.steampowered.com/app/'
_steamdb_url = 'https://steamdb.info/app/'
_protondb_url = 'https://www.protondb.com/api/v1/reports/summaries/'

# fetching runtime path
_runtime_path = f'{os.path.dirname(os.path.realpath(__file__))}/'

# loading config and set variables
if os.path.exists(f'{_runtime_path}config/bot-config-dev.json'):
    _config = core.json_to_dict(f'{_runtime_path}config/bot-config-dev.json')
else:
    _config = dict()
    _config['bot_token'] = str(input('Enter your bot token: '))
    _config['bot_prefix'] = str(input('Enter your bot prefix: '))
    _config['bot_owner'] = str(input('Enter the bot owner: '))
    _config['bot_list'] = str(input('Enter bot names as list: '))
    _config['bot_extension_dir'] = str(input('Enter the bot extension dir name: '))
    if not os.path.exists(f'{_runtime_path}config'):
        os.makedirs(f'{_runtime_path}config', mode=0o744)
    core.dict_to_json(_config, f'{_runtime_path}config/bot-config-dev.json')
_bot_token = _config.get('bot_token')
_bot_prefix = _config.get('bot_prefix')
_bot_owner = _config.get('bot_owner')
_bot_list = _config.get('bot_list')
_bot_extension_dir = _config.get('bot_extension_dir')

# creating clients
_bot_client = Bot(command_prefix=_bot_prefix)
_steam_client = steamfront.Client()  # might move into own module

# initialize logging
if not os.path.exists(f'{_runtime_path}logs'):
    os.makedirs(f'{_runtime_path}logs', mode=0o744)
core.setup_logger('bot-client', f'{_runtime_path}logs/bot-client.log', level=_log_level)
core.setup_logger('bug-tracker', f'{_runtime_path}logs/bugtracker.log', level=_log_level)
_bot_client_log = logging.getLogger('bot-client')
_bug_tracker_log = logging.getLogger('bug-tracker')
_bot_client_log.debug('Bot starting up.')

# initialize permission lists
if os.path.exists(f'{_runtime_path}config/admins-dev.json'):
    _admin_list = core.json_to_dict(f'{_runtime_path}config/admins-dev.json').get('admins')
else:
    _admin_list = []
if os.path.exists(f'{_runtime_path}config/moderators-dev.json'):
    _moderator_list = core.json_to_dict(f'{_runtime_path}config/moderators-dev.json').get('moderators')
else:
    _moderator_list = []


# defining basic bot functionality
@_bot_client.event
async def on_ready():
    """
    Sends message to stdout and bot-client.log when the bot has started up
    """
    _bot_client_log.debug('Logged in as:')
    _bot_client_log.debug(f'Bot name: {_bot_client.user.name}')
    _bot_client_log.debug(f'Bot ID: {_bot_client.user.id}')
    _bot_client_log.info(f'Bot is ready.')


@_bot_client.command(pass_context=True)
async def bot(context, command: str ='', value: str ='', *, message: str =''):
    if _debug_mode:
        print(f'context.message.author = {context.message.author}\n' +
              f'context.message.author.mention = {context.message.author.mention}\n' +
              f'context.message.author.id = {context.message.author.id}\n' +
              f'context.message.server = {context.message.server}\n' +
              f'context.message.channel = {context.message.channel}\n' +
              f'context.message.content = {context.message.content}\n' +
              f'command = {command}\n' +
              f'value = {value}\n' +
              f'message = {message}\n')

    if command == 'add':
        if value == 'admin':
            if str(context.message.author) == str(_bot_owner):
                if message not in _admin_list:
                    # TODO: check if user exists
                    _admin_list.append(message)
                    core.dict_to_json(dict(admins=_admin_list), f'{_runtime_path}config/admins-dev.json')
                    _bot_client_log.info(f'{message} added as admin.')
                    await _bot_client.say(f'{context.message.author.mention} added {message} to admin list.')
                    return
                else:
                    await _bot_client.say(f'{context.message.author.mention} {message} is already in admin list.')
                    return
            else:
                await _bot_client.say(f'{context.message.author.mention} you are not the bot owner, ignoring command.')
                return
        if value == 'moderator':
            if str(context.message.author) == str(_bot_owner) or str(context.message.author) in _admin_list:
                if message not in _moderator_list:
                    # TODO: check if user exists
                    _moderator_list.append(message)
                    core.dict_to_json(dict(moderators=_moderator_list), f'{_runtime_path}config/moderators-dev.json')
                    _bot_client_log.info(f'{message} added as moderator.')
                    await _bot_client.say(f'{context.message.author.mention} added {message} to moderator list.')
                    return
                else:
                    await _bot_client.say(f'{context.message.author.mention} {message} is already in moderator list.')
                    return
            else:
                await _bot_client.say(f'{context.message.author.mention} you are not the bot owner nor an admin,' +
                                      f'ignoring command.')
                return

    if command == 'remove':
        if value == 'admin':
            if str(context.message.author) == str(_bot_owner):
                if message in _admin_list:
                    # TODO: check if user exists
                    _admin_list.remove(message)
                    core.dict_to_json(dict(admins=_admin_list), f'{_runtime_path}config/admins-dev.json')
                    _bot_client_log.info(f'{message} removed as admin.')
                    await _bot_client.say(f'{context.message.author.mention} removed {message} as admin.')
                    return
                else:
                    await _bot_client.say(f'{context.message.author.mention} {message} is not on admin list.')
                    return
            else:
                await _bot_client.say(f'{context.message.author.mention} you are not the bot owner, ignoring command.')
                return
        if value == 'moderator':
            if str(context.message.author) == str(_bot_owner) or str(context.message.author) in _admin_list:
                if message in _moderator_list:
                    # TODO: check if user exists
                    _moderator_list.remove(message)
                    core.dict_to_json(dict(moderators=_moderator_list), f'{_runtime_path}config/moderators-dev.json')
                    _bot_client_log.info(f'{message} removed as moderator.')
                    await _bot_client.say(f'{context.message.author.mention} removed {message} as moderator.')
                    return
                else:
                    await _bot_client.say(f'{context.message.author.mention} {message} is not on moderator list.')
                    return
            else:
                await _bot_client.say(f'{context.message.author.mention} you are not the bot owner nor an admin,' +
                                      f'ignoring command.')
                return

    if command == 'exit':
        if str(context.message.author) == str(_bot_owner):
            _bot_client_log.info(f'{context.message.author} issued shut down command.')
            await _bot_client.say(f'{context.message.author.mention} goodbye cruel world.')
            await _bot_client.logout()
            await _bot_client.close()
            global _exit_flag
            _exit_flag = True
            core.end_program(_delta_time_start, 0)
            return
        else:
            await _bot_client.say(f'{context.message.author.mention} Only the bot owner can issue this command.')
            return

    # TODO: remove this functionality
    if command == 'test':
        userid = re.sub('[<>@]', '', value)
        print(re.findall('[@<>0-9]', value))
        print(len(value) == len(re.findall('[@<>0-9]', value)))
        print(f'userID = {userid}')
        user = await _bot_client.get_user_info(userid)
        print(f'{user.name}#{user.discriminator}')
        return
    #     em = discord.Embed(description=f'[test](https://videonauth.ddns.net)', color=discord.Color.orange())
    #     await _bot_client.say(embed=em)
    #     return


if __name__ == '__main__':
    # loading extensions
    _path = f'{_runtime_path}{_bot_extension_dir}/'
    _file_list = [f.replace('.py', '') for f in os.listdir(_path) if os.path.isfile(os.path.join(_path, f))]
    for _extension in _file_list:
        try:
            print(_path + _extension)
            _bot_client.load_extension(_bot_extension_dir + '.' + _extension)
            _bot_client_log.info(f'Loaded extension: {_extension} from {_extension}.py')
        except (AttributeError, ImportError) as _error:
            _bot_client_log.warning(f'Failed to load extension: {_extension}')

    # running bot
    try:
        _bot_client.run(_bot_token)
        _bot_client_log.debug('Bot has stopped.')
    except KeyboardInterrupt:
        pass
    finally:
        if not _exit_flag:
            core.end_program(_delta_time_start, 0)
