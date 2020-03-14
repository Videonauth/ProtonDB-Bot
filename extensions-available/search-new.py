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


class Result(object):
    """
    Main data class for the search database.
    """
    # Constructor, here all variables the data class has are initialized
    def __init__(self) -> None:
        # Fill the three time variables (this is the only place where they are the same).
        # self.created is to be treated immutable!
        self.created = time.time()
        self.last_updated = self.created
        self.last_modified = self.created

        # Pre initialize the steam variables
        self.steam_id = int(-1)
        self.steam_name = str('')
        self.steam_price_euro = float(0.00)
        self.steam_price_us = float(0.00)
        self.steam_description = str('')

        # Initialize the list of known abrevations.
        self.known_abrevations = list([])

        # Initialize metrics variables
        self.last_shown = self.created
        self.count_shown = int(0)

    def __str__(self):
        return f'Data Object: {self.steam_id}: {self.steam_name}'

    def get_dict(self) -> dict:
        return dict(
            created=self.created,
            last_updated=self.last_updated,
            last_modified=self.last_modified,
            steam_id=self.steam_id,
            steam_name=self.steam_name,
            steam_description=self.steam_description,
            steam_price_euro=self.steam_price_euro,
            steam_price_us=self.steam_price_us,
            known_abrevations=self.known_abrevations,
            last_shown=self.last_shown,
            count_shown=self.count_shown
        )


_data = dict({})
_save_output = dict({})


class Search(commands.Cog):

    def __init__(self, client):
        self.client = client

        # class specific initialisations
        if os.path.exists(f'data/data.json'):
            _tmp_data = core.json_to_dict(f'data/data.json')
            print(len(_tmp_data))
            for _key, _value in _tmp_data.items():
                _tmp_result = Result()
                if int(_key) == _value.get(f'steam_id'):
                    _tmp_result.steam_id = _value.get(f'steam_id')
                else:
                    break
                _tmp_result.created = _value.get('created')
                _tmp_result.last_updated = _value.get('last_updated')
                _tmp_result.last_modified = _value.get('last_modified')
                _tmp_result.steam_id = _value.get('steam_id')
                _tmp_result.steam_name = _value.get('steam_name')
                _tmp_result.steam_description = _value.get('steam_description')
                _tmp_result.steam_price_euro = _value.get('steam_price_euro')
                _tmp_result.steam_price_us = _value.get('steam_price_us')
                _tmp_result.known_abrevations = _value.get('known_abrevations')
                _tmp_result.last_shown = _value.get('last_shown')
                _tmp_result.count_shown = _value.get('count_shown')
                _data.update({_tmp_result.steam_id: _tmp_result})
                print(_tmp_result)
            _tmp_data.clear()
        else:
            if not os.path.exists(f'data-input/games.json'):
                core.bash_command([f'curl', f'{__steam_app_list__}', f'-o', 'data-input/games.json'])
            _tmp_games = dict({})
            if os.path.exists(f'data-input/games.json'):
                _tmp_games = core.json_to_dict('data-input/games.json')
                _tmp_games = _tmp_games.get(f'applist')
                _tmp_games = _tmp_games.get(f'apps')
                for _entry in _tmp_games:
                    _tmp_result = Result()
                    _tmp_result.steam_id = _entry.get(f'appid')
                    _tmp_result.steam_name = _entry.get(f'name')
                    _data.update({_tmp_result.steam_id: _tmp_result})
                    _save_output.update({_tmp_result.steam_id: _tmp_result.get_dict()})
                core.dict_to_json(_save_output, f'data/data.json')
                _tmp_games = dict({})
                _save_output.clear()

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
        _result = Result()
        if search_text != f'':
            # for _key, _value in _data:
            #     print(f'{_key} : {_value}')
            #     if _value.steam_id == search_text:
            #         #_result.steam_id = _value.steam_id

            # TODO: search own db
            # TODO: if not present in own db or not found search steampowered.com
            # TODO: update own db
            if _result.steam_id is not int(-1):
                # TODO: output result
                return
            else:
                _output += f'Search turned up nothing.\n'
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
