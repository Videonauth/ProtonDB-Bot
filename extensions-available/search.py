#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# ProtonDB-Bot - extensions-available/search.py
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 23.04.2019 - 13:24
# Purpose: -
# Written for: Python 3.6.3
# ---------------------------------------------------------------------------

__version__ = f'0.0.18'
__google__ = f'https://www.google.com/search?safe=off&q='
__duck__ = f'https://duckduckgo.com/?q='
__steam__ = f'https://store.steampowered.com/app/'
__steamdb__ = 'https://steamdb.info/app/'
__protondb__ = 'https://www.protondb.com/api/v1/reports/summaries/'
__strip_pattern__ = r'[a-z.:/<>?]'

# ---------------------------------------------------------------------------
# importing basic libraries
# ---------------------------------------------------------------------------
import logging
import re
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
# Initialize logging
# ---------------------------------------------------------------------------
core.setup_logger(f'searcg-log',f'logs/search.log')
_search_log = logging.getLogger(f'search-log')
_search_log.debug(f'Bot starting up.')

# ---------------------------------------------------------------------------
# Setting up steam client
# ---------------------------------------------------------------------------
_steam_client = steamfront.Client()


class Search(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def search(self, context, *, search_text=''):
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
            await context.send(f'{context.message.author.mention}\nThe bot is muted in this channel.')
            return

        _output = f'{context.message.author.mention}\n'
        _data = None
        _game = None
        if search_text is not f'':

            # Assume search_string is a number and try a steamfront search for AppId
            if _game is None:
                try:
                    _game = _steam_client.getApp(appid=search_text)
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Assume that search_text is no plain AppId and instead do a steamfront search for Name.
            if _game is None:
                try:
                    _game = _steam_client.getApp(name=search_text, caseSensitive=False)
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Try a google search for 'site:steamdb.info+search_text' divided by '/app/'
            if _game is None:
                _url = f'{__google__}site%3Asteamdb.info+{search_text.replace(" ", "+")}'
                _soup = Soup(requests.get(url=_url).text, f'lxml')
                try:
                    for _cite in _soup.find_all(f'cite'):
                        if int(str(_cite).find(f'/app/')) != -1:
                            _search_result = str(_cite)
                            _search_result = str(re.sub(__strip_pattern__, f'', _search_result))
                            _game = _steam_client.getApp(appid=_search_result)
                            break
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Try a google search for 'site:steamdb.info+search_text' divided by 'sub'
            if _game is None:
                _url = f'{__google__}site%3Asteamdb.info+{search_text.replace(" ", "+")}'
                _soup = Soup(requests.get(url=_url).text, f'lxml')
                try:
                    for _cite in _soup.find_all(f'cite'):
                        if int(str(_cite).find(f'sub')) != -1:
                            _search_result = str(_cite)
                            _search_result = str(re.sub(__strip_pattern__, f'', _search_result))
                            _game = _steam_client.getApp(appid=_search_result)
                            break
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Try a google search for 'site:store.steampowered.com+search_text divided by 'AppId'
            if _game is None:
                _url = f'{__google__}site%3Astore.steampowered.com+{search_text.replace(" ", "+")}'
                _soup = Soup(requests.get(url=_url).text, f'lxml')
                try:
                    for _cite in _soup.find_all(f'cite'):
                        if int(str(_cite).find(f'AppId')) != -1:
                            _search_result = str(_cite)
                            _search_result = str(re.sub(__strip_pattern__, f'', _search_result))
                            _game = _steam_client.getApp(appid=_search_result)
                            break
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # if all searches have failed add this to output
            if _game is None:
                _output += f'I\'m sorry, but I could not find any usable input data for your search term.\n'
                _output += f'\n'
                _output += f'[Search with Google.]({__google__ + search_text.replace(" ", "+")})\n\n'
                _output += f'[Search with Duck Duck Go.]({__duck__ + search_text.replace(" ", "*")})\n'

        # if we got no search string
        else:
            _output += f'If you want me to search something for you you need to specify it.\n'

        # if we got a _game object we compose the output data
        if _game is not None:
            # Hitting protondb only then we have some of the data already.
            # Prevents unnecessary web traffic.
            _request = requests.get(url=f'{__protondb__ + str(_game.appid)}.json',
                                    headers={f'User-Agent': f'ProtonDB Bot {__version__}',
                                             f'Referer': 'ProtonDB Chat'})
            if str(_request.status_code) != '404':
                try:
                    _data = dict(_request.json())
                except JSONDecodeError:
                    pass
            else:
                _data = None
            _output += f'I found the following for "{search_text}":\n\n'
            _output += f'Game Name: {_game.name}\n'
            _output += f'Game appID: {_game.appid}\n\n'
            _output += f'[ProtonDB link](https://www.protondb.com/app/{_game.appid})\n'
            if _data is None:
                if dict(_game.platforms).get('linux') is True:
                    _output += f'```Runs Native```\n'
                elif dict(_game.platforms).get('linux') is False:
                    _output += f'```It seems there are no reports yet. You can add one```'
                    _output += f'[Write a report.](<https://www.protondb.com/contribute?appId={_game.appid}>)\n\n'
            else:
                if dict(_game.platforms).get('linux') is True:
                    _output += f'```Runs Native\n\n'
                else:
                    _output += f'```'
                _output += f'Current rating:    {_data.get("tier")}\n'
                _output += f'Number of reports: {_data.get("total")}\n'
                _output += f'Trending:          {_data.get("trendingTier")}\n'
                _output += f'Best rating given: {_data.get("bestReportedTier")}```'
                if dict(_game.platforms).get('linux') is True:
                    _output += f'\n'
                else:
                    _output += f'[Write a report.](<https://www.protondb.com/contribute?appId={_game.appid}>)\n\n'
            _output += f'[Steam link](<https://store.steampowered.com/app/{_game.appid}>)\n'
            _output += f'[SteamDB link](<https://steamdb.info/app/{_game.appid}>)\n'
            try:
                _output += f'[Metacritic link](<{dict(_game.metacritic).get("url")}>)\n'
                _output += f'```Metacritic: {dict(_game.metacritic).get("score")}/100\n'
            except TypeError:
                _output += f'```Metacritic: N/A\n'
            try:
                _output += f'Price:      {dict(_game.price_overview).get("final_formatted")}```\n'
            except TypeError:
                _output += f'Price:      N/A```\n'
        _embed = discord.Embed(
            # title=f'test',
            description=_output,
            colour=discord.Colour.orange()
        )
        _embed.set_image(url=f'https://steamcdn-a.akamaihd.net/steam/apps/{_game.appid}/header.jpg')
        # _embed.set_thumbnail(url=f'https://steamcdn-a.akamaihd.net/steam/apps/{_game.appid}/header.jpg')
        await context.send(embed=_embed)


def setup(client):
    client.add_cog(Search(client))
