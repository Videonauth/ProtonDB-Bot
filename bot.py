#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# ProtonDB-Bot - bot.py
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 09.11.18 - 15:01
# Purpose: -
# Written for: Python 3.6.3
# ---------------------------------------------------------------------------
from json import JSONDecodeError
from bs4 import BeautifulSoup
from discord.ext.commands import Bot
import requests
import steamfront
from steamfront import errors
import modules.core as core

CONFIG = core.strip_quotes_from_dict(core.file_to_dict('bot.config'))
BOT_TOKEN = CONFIG.get('BOT_TOKEN')
BOT_PREFIX = '!'
PROTONDB_URL = 'https://www.protondb.com/api/v1/reports/summaries/'
GOOGLE_URL = 'https://www.google.com/search?safe=off&q='

# Generating clients
bot_client = Bot(command_prefix=BOT_PREFIX)
steam_client = steamfront.Client()


@bot_client.command(description='Checks for a game and reports findings',
                    brief='ProtonDB game search',
                    pass_context=True)
async def search(context, *, search_text=''):
    print(context.message.author)
    print(context.message.channel)
    if str(context.message.channel) == 'protondb-discussion':
        print(context.message.content)
        print(context.message.server)
        return
    print(context.message.content)
    print(context.message.server)
    # TODO: make channel filters
    # Initialize variables
    output = f''
    data = None
    game = None
    if search_text is not '':
        # If got a search string
        if game is None:
            # Assume saerch_string is a number and try a steamfront search for AppId
            try:
                print(search_text)
                game = steam_client.getApp(appid=search_text)
            except (IndexError, TypeError, errors.AppNotFound):
                game = None
        if game is None:
            # Assume that search_text is no plain AppId and instead do a steamfront search for Name.
            try:
                game = steam_client.getApp(name=search_text, caseSensitive=False)
            except (IndexError, TypeError, errors.AppNotFound):
                game = None
        if game is None:
            # Try a google search for 'site:steamdb.info+search_text
            search_url = f'{GOOGLE_URL}site%3Asteamdb.info+{search_text.replace(" ", "+")}'
            soup = BeautifulSoup(requests.get(url=search_url).text, 'lxml')
            try:
                search_result = str(soup.find_all('cite')[0])
                print(search_result)
                search_result = search_result.strip('<cite>https://steamdb.info/app/')
                search_result = search_result.strip('</cite>')
                print(search_result)
                game = steam_client.getApp(appid=search_result)
            except (IndexError, TypeError, errors.AppNotFound):
                game = None
        if game is None:
            # Try a google search for 'site:store.steampowered.com+search_text
            search_url = f'{GOOGLE_URL}site%3Astore.steampowered.com+{search_text.replace(" ", "+")}'
            soup = BeautifulSoup(requests.get(url=search_url).text, 'lxml')
            try:
                search_result = str(soup.find_all('cite')[0])
                print(search_result)
                search_result = search_result.strip('<cite>https://store.steampowered.com/forums/?AppId=<b>')
                search_result = search_result.strip('</b></cite>')
                print(search_result)
                game = steam_client.getApp(appid=search_result)
            except (IndexError, TypeError, errors.AppNotFound):
                game = None
        if game is None:
            # TODO: expand search
            # After all searches failed output a message
            output += f'{context.message.author.mention} This is no game as far I found out,'
            output += f'best see for yourself.\n'
            # output += f'{GOOGLE_URL}site%3Asteamdb.info+{search_text.replace(" ", "+")}\n'
            # output += f'{GOOGLE_URL}site%3Astore.steampowered.com+{search_text.replace(" ", "+")}\n'
            output += f'{GOOGLE_URL}{search_text.replace(" ", "+")}\n'
            output += f'Remember you can always do a search for AppID "!search <AppID>"\n'
            print(output)
            await bot_client.say(output)
            return
    else:
        # If not got a search string
        output += f'{context.message.author.mention} '
        output += f'you want to search for something you need to give directions!'
        await bot_client.say(output)
        return
    if game is not None:
        http_response = requests.get(url=f'{PROTONDB_URL}{game.appid}.json')
        if str(http_response.status_code) != '404':
            try:
                data = dict(http_response.json())
            except JSONDecodeError:
                pass
        else:
            data = None
        output += f'{context.message.author.mention} I found the following for "{search_text}":\n\n'
        output += f'Game Name: {game.name}\n'
        output += f'Game appID: {game.appid}\n\n'
        output += f'ProtonDB link: https://www.protondb.com/app/{game.appid}\n'
        if data is None:
            if dict(game.platforms).get('linux') is True:
                output += f'```Runs Native```\n'
            elif dict(game.platforms).get('linux') is False:
                output += f'```It seems there are no reports yet. You can add one```'
                output += f'Report game: <https://www.protondb.com/contribute?appId={game.appid}>\n\n'
        else:
            if dict(game.platforms).get('linux') is True:
                output += f'```Runs Native\n\n'
            else:
                output += f'```'
            output += f'Current rating:    {data.get("tier")}\n'
            output += f'Number of reports: {data.get("total")}\n'
            output += f'Trending:          {data.get("trendingTier")}\n'
            output += f'Best rating given: {data.get("bestReportedTier")}```'
            if dict(game.platforms).get('linux') is True:
                output += f'\n'
            else:
                output += f'Report game: <https://www.protondb.com/contribute?appId={game.appid}>\n\n'
        output += f'Steam link: <https://store.steampowered.com/app/{game.appid}>\n'
        output += f'SteamDB link: <https://steamdb.info/app/{game.appid}>\n'
        try:
            output += f'Metacritic link: <{dict(game.metacritic).get("url")}>\n'
            output += f'```Metacritic: {dict(game.metacritic).get("score")}/100\n'
        except TypeError:
            output += f'```Metacritic: N/A\n'
        try:
            output += f'Price:      {dict(game.price_overview).get("final_formatted")}```\n'
        except TypeError:
            output += f'Price:      N/A```\n'
        await bot_client.say(output)
        return
    else:
        return

if __name__ == '__main__':
    bot_client.run(BOT_TOKEN)
