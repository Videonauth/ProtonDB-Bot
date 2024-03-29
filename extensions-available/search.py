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

__version__ = f'0.0.19'
__google__ = f'https://www.google.com/search?safe=off&q='
__duck__ = f'https://duckduckgo.com/?q='
__steam__ = f'https://store.steampowered.com/app/'
__steamdb__ = 'https://steamdb.info/app/'
__protondb__ = 'https://www.protondb.com/api/v1/reports/summaries/'
__protondbsearch__ = 'https://www.protondb.com/search?q='
__strip_pattern__ = r'[a-zA-Z.:=/<>?]'

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
_log_level = logging.DEBUG
core.setup_logger(f'search-log', f'logs/search.log', level=_log_level)
_search_log = logging.getLogger(f'search-log')

# ---------------------------------------------------------------------------
# Setting up steam client
# ---------------------------------------------------------------------------
_steam_client = steamfront.Client()


class Search(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def search(self, context, *, search_text=''):
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

        # _output = f'{context.message.author.mention}\n'
        _output = f''
        _data = None
        _game = None
        _embed = f''
        if search_text is not f'':

            # Assume search_string is a number and try a steamfront search for AppId
            if _game is None:
                try:
                    _game = _steam_client.getApp(appid=search_text)
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Try a google search for 'site:steamdb.info+search_text' divided by '/app/'
            # "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"
            if _game is None:
                _url = f'{__google__}site%3Asteamdb.info+{search_text.replace(" ", "+")}'
                _soup = Soup(
                    requests.get(
                        url=_url,
                        headers={f'User-Agent': f'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;'
                                 f' rv:66.0) Gecko/20100101 Firefox/66.0',
                                 f'Referer': '-'}
                    ).text, f'lxml'
                )
                try:
                    for _cite in _soup.find_all(f'cite'):
                        if int(str(_cite).find(f'/app/')) != -1:
                            _search_result = str(_cite)
                            _search_result = _search_result.strip(f'<cite class="iUh30">')
                            _search_result = _search_result.strip(f'</cite>')
                            _search_result = str(re.sub(__strip_pattern__, f'', _search_result))
                            _game = _steam_client.getApp(appid=_search_result)
                            break
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Try a google search for 'site:steamdb.info+search_text' divided by 'sub'
            if _game is None:
                _url = f'{__google__}site%3Asteamdb.info+{search_text.replace(" ", "+")}'
                _soup = Soup(
                    requests.get(
                        url=_url,
                        headers={f'User-Agent': f'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;'
                                 f' rv:66.0) Gecko/20100101 Firefox/66.0',
                                 f'Referer': '-'}
                    ).text, f'lxml'
                )
                try:
                    for _cite in _soup.find_all(f'cite'):
                        if int(str(_cite).find(f'sub')) != -1:
                            _search_result = str(_cite)
                            _search_result = _search_result.strip(f'<cite class="iUh30">')
                            _search_result = _search_result.strip(f'</cite>')
                            _search_result = str(re.sub(__strip_pattern__, f'', _search_result))
                            _game = _steam_client.getApp(appid=_search_result)
                            break
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Try a google search for 'site:store.steampowered.com+search_text divided by 'AppId'
            if _game is None:
                _url = f'{__google__}site%3Astore.steampowered.com+{search_text.replace(" ", "+")}'
                _soup = Soup(
                    requests.get(
                        url=_url,
                        headers={f'User-Agent': f'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;'
                                 f' rv:66.0) Gecko/20100101 Firefox/66.0',
                                 f'Referer': '-'}
                    ).text, f'lxml'
                )
                try:
                    for _cite in _soup.find_all(f'cite'):
                        if int(str(_cite).find(f'AppId')) != -1:
                            _search_result = str(_cite)
                            _search_result = _search_result.strip(f'<cite class="iUh30">')
                            _search_result = _search_result.strip(f'</cite>')
                            _search_result = str(re.sub(__strip_pattern__, f'', _search_result))
                            _game = _steam_client.getApp(appid=_search_result)
                            break
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Try a google search for 'site:store.steampowered.com+search_text divided by 'sub'
            if _game is None:
                _url = f'{__google__}site%3Astore.steampowered.com+{search_text.replace(" ", "+")}'
                _soup = Soup(
                    requests.get(
                        url=_url,
                        headers={f'User-Agent': f'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;'
                                 f' rv:66.0) Gecko/20100101 Firefox/66.0',
                                 f'Referer': '-'}
                    ).text, f'lxml'
                )
                try:
                    for _cite in _soup.find_all(f'cite'):
                        if int(str(_cite).find(f'/sub/')) != -1:
                            _search_result = str(_cite)
                            _search_result = _search_result.strip(f'<cite class="iUh30">')
                            _search_result = _search_result.strip(f'</cite>')
                            _search_result = str(re.sub(__strip_pattern__, f'', _search_result))
                            _game = _steam_client.getApp(appid=_search_result)
                            break
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

                # Assume that search_text is no plain AppId and instead do a steamfront search for Name.
                if _game is None:
                    try:
                        _game = _steam_client.getApp(name=search_text, caseSensitive=False)
                    except (IndexError, TypeError, errors.AppNotFound):
                        _game = None

            # if all searches have failed add this to output
            if _game is None:
                _output += f'I\'m sorry, but I could not find any usable input data for your search term.\n'
                _output += f'\n'
                _output += f'[Search with Google.]({__google__ + search_text.replace(" ", "+")})\n\n'
                _output += f'[Search with Duck Duck Go.]({__duck__ + search_text.replace(" ", "*")})\n\n'
                _output += f'[Search on ProtonDB.]({__protondbsearch__ + search_text.replace(" ", "+")})\n'
                _embed = discord.Embed(
                    title=f'Search failure:',
                    description=_output,
                    colour=discord.Colour.orange()
                )

        # if we got no search string
        else:
            _output += f'If you want me to search something for you you need to specify it.\n'
            _embed = discord.Embed(
                title=f'Error:',
                description=_output,
                colour=discord.Colour.red()
            )

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
            _ratings_value = str()
            _ratings_value += f'[ProtonDB link](https://www.protondb.com/app/{_game.appid})\n'
            if _data is None:
                if dict(_game.platforms).get('linux') is True:
                    _ratings_value += f'```Runs Native```\n'
                elif dict(_game.platforms).get('linux') is False:
                    _ratings_value += f'```It seems there are no reports yet. You can add one```'
                    _ratings_value += \
                        f'[Write a report.](<https://www.protondb.com/contribute?appId={_game.appid}>)\n\n'
            else:
                if dict(_game.platforms).get('linux') is True:
                    _ratings_value += f'```Runs Native\n\n'
                else:
                    _ratings_value += f'```'
                _ratings_value += f'Current rating:    {_data.get("tier")}\n'
                _ratings_value += f'Number of reports: {_data.get("total")}\n'
                _ratings_value += f'Trending:          {_data.get("trendingTier")}\n'
                _ratings_value += f'Best rating given: {_data.get("bestReportedTier")}```'
                if dict(_game.platforms).get('linux') is True:
                    _ratings_value += f'\n'
                else:
                    _ratings_value += \
                        f'[Write a report.](<https://www.protondb.com/contribute?appId={_game.appid}>)\n\n'
            _steamlink = str()
            _steamlink += f'[Steam link](<https://store.steampowered.com/app/{_game.appid}>)\n'
            _steamdblink = str()
            _steamdblink += f'[SteamDB link](<https://steamdb.info/app/{_game.appid}>)\n'
            _metacritic = str()
            try:
                _metacritic += f'[{dict(_game.metacritic).get("score")}/100](<{dict(_game.metacritic).get("url")}>)\n'
            except TypeError:
                _metacritic += f'N/A\n'
            _price = str()
            try:
                _price += \
                    f'[{dict(_game.price_overview).get("final_formatted")}](<https://store.' \
                    f'steampowered.com/app/{_game.appid}>)\n'
            except TypeError:
                _price += f'N/A\n\n'
            try:
                _about = str(_game.about_the_game)
            except TypeError:
                _about = None
            if _about is not None:
                # sanitize input
                _about = _about.replace(f'\r\n', f'')
                _about = _about.replace(f'<br>', f'\n')
                _about = _about.replace(f'<strong>', f'**')
                _about = _about.replace(f'</strong>', f'**')
                _about = _about.replace(f'<i>', f'*')
                _about = _about.replace(f'</i>', f'*')
                _about = _about.replace(f'<img src="', f'[Image](')
                _about = _about.replace(f'">', f')')
                _about = _about.replace(f'" >', f')')
                _about = _about.replace(f'<br />', f'\n')
                _about = _about.replace(f'\n\n\n', f'\n\n')
                _about = _about.replace(f'\n\n\n\n', f'\n\n')
            _embed = discord.Embed(
                # title=f'Search result:',
                # description=f'I found the following for "{search_text}".\n\n',
                colour=discord.Colour.from_rgb(0xff, 0xff, 0xff)
            )
            _embed.add_field(name=f'Game Name', value=_game.name, inline=False)
            _embed.add_field(name=f'Game appID', value=_game.appid, inline=False)
            _embed.add_field(name=f'ProtonDB ratings', value=_ratings_value, inline=False)
            _embed.add_field(name=f'Steam', value=_steamlink, inline=True)
            _embed.add_field(name=f'SteamDB', value=_steamdblink, inline=True)
            _embed.add_field(name=f'Metacritic score', value=_metacritic, inline=True)
            _embed.add_field(name=f'Price', value=_price, inline=True)
            _embed.add_field(
                name=f'About',
                # Max is 1024
                value=_about[0: 300 - 9] + f'...\n[Read more](https://store.steampowered.com/app/{_game.appid})',
                inline=False
            )
            _embed.set_image(url=f'https://steamcdn-a.akamaihd.net/steam/apps/{_game.appid}/header.jpg')
        # _embed.set_thumbnail(url=f'https://steamcdn-a.akamaihd.net/steam/apps/{_game.appid}/header.jpg')
        await context.send(embed=_embed)

    @commands.command(pass_context=True)
    async def protondb(self, context, *, search_text=''):
        """
        Initiates a search only on protondb for a game.

        Usage: [prefix]protondb <(game-name|appid)>

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

        # _output = f'{context.message.author.mention}\n'
        _output = f''
        _data = None
        _game = None
        _embed = f''
        if search_text is not f'':

            # Assume search_string is a number and try a steamfront search for AppId
            if _game is None:
                try:
                    _game = _steam_client.getApp(appid=search_text)
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Try a google search for 'site:steamdb.info+search_text' divided by '/app/'
            # "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"
            if _game is None:
                _url = f'{__google__}site%3Asteamdb.info+{search_text.replace(" ", "+")}'
                _soup = Soup(
                    requests.get(
                        url=_url,
                        headers={f'User-Agent': f'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;'
                                 f' rv:66.0) Gecko/20100101 Firefox/66.0',
                                 f'Referer': '-'}
                    ).text, f'lxml'
                )
                try:
                    for _cite in _soup.find_all(f'cite'):
                        if int(str(_cite).find(f'/app/')) != -1:
                            _search_result = str(_cite)
                            _search_result = _search_result.strip(f'<cite class="iUh30">')
                            _search_result = _search_result.strip(f'</cite>')
                            _search_result = str(re.sub(__strip_pattern__, f'', _search_result))
                            _game = _steam_client.getApp(appid=_search_result)
                            break
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Try a google search for 'site:steamdb.info+search_text' divided by 'sub'
            if _game is None:
                _url = f'{__google__}site%3Asteamdb.info+{search_text.replace(" ", "+")}'
                _soup = Soup(
                    requests.get(
                        url=_url,
                        headers={f'User-Agent': f'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;'
                                 f' rv:66.0) Gecko/20100101 Firefox/66.0',
                                 f'Referer': '-'}
                    ).text, f'lxml'
                )
                try:
                    for _cite in _soup.find_all(f'cite'):
                        if int(str(_cite).find(f'sub')) != -1:
                            _search_result = str(_cite)
                            _search_result = _search_result.strip(f'<cite class="iUh30">')
                            _search_result = _search_result.strip(f'</cite>')
                            _search_result = str(re.sub(__strip_pattern__, f'', _search_result))
                            _game = _steam_client.getApp(appid=_search_result)
                            break
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Try a google search for 'site:store.steampowered.com+search_text divided by 'AppId'
            if _game is None:
                _url = f'{__google__}site%3Astore.steampowered.com+{search_text.replace(" ", "+")}'
                _soup = Soup(
                    requests.get(
                        url=_url,
                        headers={f'User-Agent': f'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;'
                                 f' rv:66.0) Gecko/20100101 Firefox/66.0',
                                 f'Referer': '-'}
                    ).text, f'lxml'
                )
                try:
                    for _cite in _soup.find_all(f'cite'):
                        if int(str(_cite).find(f'AppId')) != -1:
                            _search_result = str(_cite)
                            _search_result = _search_result.strip(f'<cite class="iUh30">')
                            _search_result = _search_result.strip(f'</cite>')
                            _search_result = str(re.sub(__strip_pattern__, f'', _search_result))
                            _game = _steam_client.getApp(appid=_search_result)
                            break
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Try a google search for 'site:store.steampowered.com+search_text divided by 'sub'
            if _game is None:
                _url = f'{__google__}site%3Astore.steampowered.com+{search_text.replace(" ", "+")}'
                _soup = Soup(
                    requests.get(
                        url=_url,
                        headers={f'User-Agent': f'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;'
                                 f' rv:66.0) Gecko/20100101 Firefox/66.0',
                                 f'Referer': '-'}
                    ).text, f'lxml'
                )
                try:
                    for _cite in _soup.find_all(f'cite'):
                        if int(str(_cite).find(f'/sub/')) != -1:
                            _search_result = str(_cite)
                            _search_result = _search_result.strip(f'<cite class="iUh30">')
                            _search_result = _search_result.strip(f'</cite>')
                            _search_result = str(re.sub(__strip_pattern__, f'', _search_result))
                            _game = _steam_client.getApp(appid=_search_result)
                            break
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # Assume that search_text is no plain AppId and instead do a steamfront search for Name.
            if _game is None:
                try:
                    _game = _steam_client.getApp(name=search_text, caseSensitive=False)
                except (IndexError, TypeError, errors.AppNotFound):
                    _game = None

            # if all searches have failed add this to output
            if _game is None:
                _output += f'I\'m sorry, but I could not find any usable input data for your search term.\n'
                _output += f'\n'
                _output += f'[Search with Google.]({__google__ + search_text.replace(" ", "+")})\n\n'
                _output += f'[Search with Duck Duck Go.]({__duck__ + search_text.replace(" ", "*")})\n'
                _embed = discord.Embed(
                    title=f'Search failure:',
                    description=_output,
                    colour=discord.Colour.orange()
                )

        # if we got no search string
        else:
            _output += f'If you want me to search something for you you need to specify it.\n'
            _embed = discord.Embed(
                title=f'Error:',
                description=_output,
                colour=discord.Colour.red()
            )

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
            _ratings_value = str()
            _ratings_value += f'[ProtonDB link](https://www.protondb.com/app/{_game.appid})\n'
            if _data is None:
                if dict(_game.platforms).get('linux') is True:
                    _ratings_value += f'```Runs Native```\n'
                elif dict(_game.platforms).get('linux') is False:
                    _ratings_value += f'```It seems there are no reports yet. You can add one```'
                    _ratings_value += \
                        f'[Write a report.](<https://www.protondb.com/contribute?appId={_game.appid}>)\n\n'
            else:
                if dict(_game.platforms).get('linux') is True:
                    _ratings_value += f'```Runs Native\n\n'
                else:
                    _ratings_value += f'```'
                _ratings_value += f'Current rating:    {_data.get("tier")}\n'
                _ratings_value += f'Number of reports: {_data.get("total")}\n'
                _ratings_value += f'Trending:          {_data.get("trendingTier")}\n'
                _ratings_value += f'Best rating given: {_data.get("bestReportedTier")}```'
                if dict(_game.platforms).get('linux') is True:
                    _ratings_value += f'\n'
                else:
                    _ratings_value += \
                        f'[Write a report.](<https://www.protondb.com/contribute?appId={_game.appid}>)\n\n'
            _embed = discord.Embed(
                # title=f'Search result:',
                # description=f'I found the following for "{search_text}".\n\n',
                colour=discord.Colour.from_rgb(0xff, 0xff, 0xff)
            )
            _embed.add_field(name=f'Game Name', value=_game.name, inline=False)
            _embed.add_field(name=f'Game appID', value=_game.appid, inline=False)
            _embed.add_field(name=f'ProtonDB ratings', value=_ratings_value, inline=False)
            # _embed.set_image(url=f'https://steamcdn-a.akamaihd.net/steam/apps/{_game.appid}/header.jpg')
        await context.send(embed=_embed)


def setup(client):
    client.add_cog(Search(client))
