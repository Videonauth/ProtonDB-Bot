#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# ProtonDB-Bot - extensions-available/search-new.py
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 23.04.2019 - 13:24
# Purpose: -
# Written for: Python 3.6.3
# ---------------------------------------------------------------------------

__version__ = f'0.0.19'
__google__ = f'https://www.google.com/search?safe=off&q='
__duck_duck_go__ = f'https://duckduckgo.com/?q='
__steam__ = f'https://store.steampowered.com/app/'
__steam_search__ = f'https://store.steampowered.com/search/?term='
__steam_app_list__ = f'https://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json'
__steamdb__ = 'https://steamdb.info/app/'
__protondb__ = 'https://www.protondb.com/api/v1/reports/summaries/'
__fake_firefox__ = f'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv: 74.0) Gecko/20100101 Firefox/74.0'
__strip_pattern__ = r'[a-zA-Z.:=/<>?]'
__wait_time__ = float(50.000)

# ---------------------------------------------------------------------------
# importing basic libraries
# ---------------------------------------------------------------------------
import time
import logging
import os
import re
import string
from json import JSONDecodeError

# ---------------------------------------------------------------------------
# importing dependencies
# ---------------------------------------------------------------------------
import discord
from discord.ext import commands
import steamfront
from steamfront import errors
import requests
from bs4 import BeautifulSoup as Soup

# ---------------------------------------------------------------------------
# importing core library
# ---------------------------------------------------------------------------
import modules.core as core
from modules.data import Data as Data

# ---------------------------------------------------------------------------
# Initialize logging (changed for testing)
# ---------------------------------------------------------------------------
_log_level = logging.DEBUG
core.setup_logger(f'search-new-log', f'logs/search-new.log', level=_log_level)
_search_log = logging.getLogger(f'search-new-log')

# ---------------------------------------------------------------------------
# Setting up steam client
# ---------------------------------------------------------------------------
_steam_client = steamfront.Client()

_data = dict({})


class Search(commands.Cog):

    def __init__(self, client):
        self.client = client
        if os.path.exists(f'data/data.json'):
            _tmp_data = dict({})
            _tmp_data = core.json_to_dict(f'data/data.json')
            for _key, _value in _tmp_data.items():
                _tmp_result = Data()
                _tmp_result.from_dict(_value)
                _data.update({_tmp_result.steam_id: _tmp_result})
            _tmp_data.clear()
            _search_log.debug(f'Data entries total: {len(_data)}.')
        else:
            _save_output = dict({})
            _tmp_data = list([])
            _url = __steam_app_list__
            _response = requests.get(
                url=_url,
                headers={f'User-Agent': __fake_firefox__,
                         f'Referer': '-'}
            )
            if _response.status_code != 200:
                _search_log.critical(f'Could not fetch url={_url}.')
                _search_log.critical(f'Response: {_response.status_code}')
                exit(1)
            _tmp_data = _response.json()[f'applist'][f'apps']
            for _value in _tmp_data:
                _tmp_result = Data()
                _tmp_result.steam_id = _value.get(f'appid')
                _tmp_result.steam_name = _value.get(f'name')
                _data.update({_tmp_result.steam_id: _tmp_result})
                _save_output.update({_tmp_result.steam_id: _tmp_result.to_dict()})
            core.dict_to_json(_save_output, f'data/data.json')
            _search_log.debug(f'Data entries total: {len(_data)}.')
            _tmp_data = list([])
            _save_output.clear()

    @commands.command(pass_context=True, hidden=True)
    async def db(self, context, command, *, text=f''):
        if command == f'dump':
            _save_output = dict({})
            for _key, _value in _data.items():
                _save_output.update({_value.steam_id: _value.to_dict()})
            core.dict_to_json(_save_output, f'data/data.json')
            _output = str(f'Dumped database to file: "data/data.json".')
            _search_log.debug(_output)
            _embed = discord.Embed(
                title=f'Success:',
                description=_output,
                colour=discord.Colour.green()
            )
            await context.send(embed=_embed)
            return
        if command == f'teach':
            _parameters_list = text.split(f' ')
            # First in the list has to be the steam_id i want to teach something to
            # we get the db entry from _data
            _result = Data()
            _tmp_int = int(_parameters_list[0])
            _tmp_object = _data.get(_tmp_int)
            _tmp_dict = _tmp_object.to_dict()
            _result.from_dict(_tmp_dict)
            # Second in the list has to be the kind of data to teach
            _abbreviation = str(f'')
            if _parameters_list[1] == f'abbr.':
                for _value in _parameters_list[2: len(_parameters_list)]:
                    _abbreviation += f'{_value} '.lower()
                _result.known_abbreviations.append(_abbreviation[0: len(_abbreviation) - 1])
            _output = str(f'Learning "{_abbreviation[0: len(_abbreviation) - 1]}" abbreviation '
                          f'for "{_result.steam_id}: {_result.steam_name}".')
            _search_log.debug(_output)
            _embed = discord.Embed(
                title=f'Success:',
                description=_output,
                colour=discord.Colour.green()
            )
            await context.send(embed=_embed)
            _data.update({_result.steam_id: _result})
            return

    @commands.command(pass_context=True)
    async def search(self, context, *, search_text=f''):
        """
        Initiates a search for a game.

        Usage: [prefix]search <(game-name|appid)>

        Note: bot owner, admins and moderators can override mute settings and perform a search in every channel.

        :param context: The message context.
        :param search_text: The game name or the games appid.
        """
        _search_log.info(f'context.author = {context.author}')
        _search_log.debug(f'context.message.author.mention = {context.message.author.mention}')
        _search_log.debug(f'context.message.author.id = {context.message.author.id}')
        _search_log.info(f'context.guild = {context.guild}')
        _search_log.info(f'context.channel = {context.channel}')
        _search_log.debug(f'context.message.content = {context.message.content}')
        _search_log.info(f'search_text = {search_text}')
        _config = core.json_to_dict(f'config/bot-config.json')
        _permissions = core.json_to_dict(f'config/permissions.json')

        _muted_channels = _config.get(f'muted_channels')
        _admins = _permissions.get(f'admins')
        _moderators = _permissions.get(f'moderators')

        _allowed = True
        if str(context.channel) in _muted_channels:
            _allowed = False
        if str(context.author) == str(_config.get(f'bot_owner')):
            _allowed = True
        if str(context.author) in _admins:
            _allowed = True
        if str(context.author) in _moderators:
            _allowed = True
        if not _allowed:
            _embed = discord.Embed(
                title=f'Warning:',
                description=f'The bot is muted in this channel.',
                colour=discord.Colour.orange()
            )
            await context.send(embed=_embed)
            return

        _output = f''
        _result = Data()
        _web_result = bool(False)
        if search_text != f'':
            # Searching own database
            for _key, _value in _data.items():
                if str(_value.steam_id) == search_text:
                    _search_log.debug(f'Match found in steam_id for search_text = {search_text}.')
                    _result.from_dict(_value.to_dict())
                    break
                if str(_value.steam_name).lower() == search_text.lower():
                    _search_log.debug(f'Match found in steam_name for search_text = {search_text}.')
                    _result.from_dict(_value.to_dict())
                    break
                if search_text.lower() in _value.known_abbreviations:
                    _search_log.debug(f'Match found in known_abbreviations for search_text = {search_text}.')
                    _result.from_dict(_value.to_dict())
                    break
            # Searching Steam. url=https://store.steampowered.com/search/?term=
            if _result.steam_id == -1:
                _url = f'{__steam_search__}{search_text.replace(" ", "+")}'
                _response = requests.get(
                    url=_url,
                    headers={f'User-Agent': __fake_firefox__,
                             f'Referer': '-'}
                )
                if _response.status_code == 200:
                    _tmp_list = _response.text.split(f'<!-- List Items -->')
                    _tmp_list = _tmp_list[1].split(f'<!-- End List Items -->')
                    _tmp_data = _tmp_list[0]
                    _tmp_data = Soup(_tmp_data, f'lxml')
                    _tmp_data = _tmp_data.find_all(f'a')[0]
                    _tmp_list = str(_tmp_data).split(f'data-ds-appid="')
                    _tmp_list = _tmp_list[1].split(f'"')
                    _tmp_data = int(_tmp_list[0])
                    _tmp_db_entry = _data.get(_tmp_data)
                    _result.from_dict(_tmp_db_entry.to_dict())
                    _web_result = bool(True)
            if (_result.last_updated_steamfront + __wait_time__) < time.time():
                _search_log.debug(f'Trying to fetch steamfront data.')
                try:
                    _tmp_steamfront = _steam_client.getApp(appid=str(_result.steam_id))
                except steamfront.errors.AppNotFound:
                    # TODO: get the data elsewhere if steamfront denies us data means usually
                    #  the game isn't available in germany
                    _search_log.debug(f'Steamfront gave an AppNotFound error.')
                    _result.last_updated_steamfront = time.time()
                    pass
                else:
                    _search_log.debug(f'Steamfront data successfully updated.')
                    _result.from_dict(_tmp_steamfront.raw)
                    _result.last_updated_steamfront = time.time()
            if search_text.lower() not in _result.known_abbreviations:
                if not _web_result:
                    _result.known_abbreviations.append(search_text.lower())
            # Count up the number of being shown
            _result.last_shown = time.time()
            _result.count_shown += int(1)
            # Update own db
            _data.update({_result.steam_id: _result})
            if _result.steam_id != -1:
                # TODO: output result
                _output += f'{_result.steam_name}.\n'
                _output += f'{_result.steam_id}.\n'
                _embed = discord.Embed(
                    description=_output,
                    colour=discord.Colour.from_rgb(0xff, 0xff, 0xff)
                )
                await context.send(embed=_embed)
                return
            else:
                _output += f'I\'m sorry, but I could not find any usable input data for your search term.\n'
                _output += f'\n'
                _output += f'[Search with Google.]({__google__ + search_text.replace(" ", "+")})\n\n'
                _output += f'[Search with Duck Duck Go.]({__duck_duck_go__ + search_text.replace(" ", "*")})\n'
                _embed = discord.Embed(
                    title=f'Error:',
                    description=_output,
                    colour=discord.Colour.red()
                )
                await context.send(embed=_embed)
                return
        else:
            _output += f'If you want me to search something for you you need to specify it.\n'
            _embed = discord.Embed(
                title=f'Error:',
                description=_output,
                colour=discord.Colour.red()
            )
            await context.send(embed=_embed)
            return


def setup(client):
    client.add_cog(Search(client))
