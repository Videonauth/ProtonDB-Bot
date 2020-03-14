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

        # Initialize ProtonDB variables
        self.proton_db_current_rating = None
        self.proton_db_number_reports = None
        self.proton_db_trending = None
        self.proton_db_best_rating = None

    def __str__(self) -> str:
        return f'Data Object: {self.steam_id}: {self.steam_name}'

    def to_dict(self) -> dict:
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
            count_shown=self.count_shown,
            proton_db_current_rating=self.proton_db_current_rating,
            proton_db_number_reports=self.proton_db_number_reports,
            proton_db_trending=self.proton_db_trending,
            proton_db_best_rating=self.proton_db_best_rating
        )

    def from_dict(self, _value: dict):
        self.steam_id = _value.get(f'steam_id')
        self.created = _value.get('created')
        self.last_updated = _value.get('last_updated')
        self.last_modified = _value.get('last_modified')
        self.steam_id = _value.get('steam_id')
        self.steam_name = _value.get('steam_name')
        self.steam_description = _value.get('steam_description')
        self.steam_price_euro = _value.get('steam_price_euro')
        self.steam_price_us = _value.get('steam_price_us')
        self.known_abrevations = _value.get('known_abrevations')
        self.last_shown = _value.get('last_shown')
        self.count_shown = _value.get('count_shown')
        self.proton_db_current_rating = _value.get('proton_db_current_rating')
        self.proton_db_number_reports = _value.get('proton_db_number_reports')
        self.proton_db_trending = _value.get('proton_db_trending')
        self.proton_db_best_rating = _value.get('proton_db_best_rating')


_data = dict({})
_save_output = dict({})


class Search(commands.Cog):

    def __init__(self, client):
        self.client = client
        if os.path.exists(f'data/data.json'):
            _tmp_data = dict({})
            _tmp_data = core.json_to_dict(f'data/data.json')
            for _key, _value in _tmp_data.items():
                _tmp_result = Result()
                _tmp_result.from_dict(_value)
                _data.update({_tmp_result.steam_id: _tmp_result})
            _tmp_data.clear()
        else:
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
                _tmp_result = Result()
                _tmp_result.steam_id = _value.get(f'appid')
                _tmp_result.steam_name = _value.get(f'name')
                _data.update({_tmp_result.steam_id: _tmp_result})
                _save_output.update({_tmp_result.steam_id: _tmp_result.to_dict()})
            core.dict_to_json(_save_output, f'data/data.json')
            _tmp_data = list([])
            _save_output.clear()

    @commands.command(pass_context=True, hidden=True)
    async def dumpdb(self, context):
        """
        Dumps the database to file.

        Usage: [prefix]dumpdb

        :param context: The message context.
        """
        _search_log.info(f'context.author = {context.author}')
        _search_log.debug(f'context.message.author.mention = {context.message.author.mention}')
        _search_log.debug(f'context.message.author.id = {context.message.author.id}')
        _search_log.info(f'context.guild = {context.guild}')
        _search_log.info(f'context.channel = {context.channel}')
        _search_log.debug(f'context.message.content = {context.message.content}')
        _config = core.json_to_dict(f'config/bot-config.json')
        _permissions = core.json_to_dict(f'config/permissions.json')

        _muted_channels = _config.get(f'muted_channels')
        _admins = _permissions.get(f'admins')
        _moderators = _permissions.get(f'moderators')

        _allowed = False
        if str(context.author) == str(_config.get(f'bot_owner')):
            _allowed = True
        if str(context.author) in _admins:
            _allowed = True
        if not _allowed:
            _embed = discord.Embed(
                title=f'Warning:',
                description=f'Only bot owner and admins can issue this command.',
                colour=discord.Colour.red()
            )
            await context.send(embed=_embed)
            return

        _save_output.clear()
        for _key, _value in _data.items():
            _save_output.update({_key: _value.to_dict()})
        core.dict_to_json(_save_output, f'data/data.json')
        _save_output.clear()
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
        _result = Result()
        if search_text != f'':
            # Searching own database
            for _key, _value in _data.items():
                if str(_value.steam_id) == search_text:
                    _result.from_dict(_value.to_dict())
                    break
                if str(_value.steam_name) == search_text:
                    _result.from_dict(_value.to_dict())
                    break
                if search_text in _value.known_abrevations:
                    _result.from_dict(_value.to_dict())
                    break
            # searching Steam store
            if _result.steam_id == -1:
                # TODO: if not present in own db or not found search steampowered.com
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
                    print(_tmp_data)
            # TODO: update own db
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
