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
import discord
from discord.ext.commands import Bot
import requests
import steamfront
from steamfront import errors
import modules.core as core
import logging
import re

# import sqlite3
# import os
# test
# debug mode

DEBUG_MODE = True

# Loading configuration and setting constants
CONFIG = core.strip_quotes_from_dict(core.file_to_dict('bot-dev.config'))
BOT_TOKEN = CONFIG.get('BOT_TOKEN')
BOT_PREFIX = CONFIG.get('BOT_PREFIX')
BOT_OWNER = CONFIG.get('BOT_OWNER')
BOT_LIST = ['ProtonDB Bot BETA#9278', 'ProtonDB Bot#7175']

if DEBUG_MODE:
    print(f'BOT_TOKEN = {BOT_TOKEN}\n' +
          f'BOT_PREFIX = {BOT_PREFIX}\n' +
          f'BOT_OWNER = {BOT_OWNER}\n' +
          f'BOT_LIST = {BOT_LIST}\n')

# Constants, only change if you know what you're doing
GOOGLE_URL = 'https://www.google.com/search?safe=off&q='
STEAM_URL = 'https://store.steampowered.com/app/'
STEAMDB_URL = 'https://steamdb.info/app/'
PROTONDB_URL = 'https://www.protondb.com/api/v1/reports/summaries/'

if DEBUG_MODE:
    print(f'GOOGLE_URL = {GOOGLE_URL}\n' +
          f'STEAM_URL = {STEAM_URL}\n' +
          f'STEAMDB_URL = {STEAMDB_URL}\n' +
          f'PROTONDB_URL = {PROTONDB_URL}\n')

# Generating clients
bot_client = Bot(command_prefix=BOT_PREFIX)
steam_client = steamfront.Client()
# db_client = sqlite3.connect('cache.sql')

# removing general help command
bot_client.remove_command('help')

if DEBUG_MODE:
    print(f'bot_client = {bot_client}\n' +
          f'steam_client = {steam_client}\n')

# Lists for management
if core.file_exists('muted-channels-dev.list'):
    MUTED_CHANNELS = core.file_to_list('muted-channels-dev.list')
else:
    MUTED_CHANNELS = []
    core.list_to_file(MUTED_CHANNELS, 'muted-channels-dev.list')

MUTE_EXCEPTIONS = ['Text Channels', 'Voice Channels', 'General']
ADMIN_LIST = []

if core.file_exists('admin-dev.list'):
    ADMIN_LIST = core.file_to_list('admin-dev.list')
else:
    core.list_to_file([], 'admin-dev.list')

if DEBUG_MODE:
    print(f'MUTED_CHANNELS = {MUTED_CHANNELS}\n' +
          f'MUTE_EXCEPTIONS = {MUTE_EXCEPTIONS}\n' +
          f'ADMIN_LIST = {ADMIN_LIST}\n')

STRIP_PATTERN = r'[a-z.:/<>?]'

logging.basicConfig(filename='logs/bugtracker-dev.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


# When bot is loaded up
@bot_client.event
async def on_ready():
    print(f'Bot is ready to rumble!\n')


# when someone reacts to a message
@bot_client.event
async def on_reaction_add(reaction, user):
    if DEBUG_MODE:
        print(f'user = {user}\n' +
              f'reaction.message.server = {reaction.message.server}\n' +
              f'reaction.message.channel = {reaction.message.channel}\n' +
              f'reaction.message.author = {reaction.message.author}\n' +
              f'reaction.message.content = {reaction.message.content}\n' +
              f'reaction.emoji = {reaction.emoji}\n')

    if str(reaction.message.author) in BOT_LIST:
        if reaction.emoji == '🐛':
            output = f' {user} - {reaction.message.server} - {reaction.message.channel}\n' +\
                     f'{reaction.message.content}\n\n'
            logging.error(output)
            print('DONE!!')
    return


# Command !bothelp
@bot_client.command(pass_context=True)
async def bothelp(context):
    if DEBUG_MODE:
        print(f'context.message.author = {context.message.author}\n' +
              f'context.message.server = {context.message.server}\n' +
              f'context.message.channel = {context.message.channel}\n' +
              f'context.message.content = {context.message.content}\n')

    help_text = discord.Embed(
        color=discord.Colour.orange()
    )
    help_text.set_author(name='Help')
    help_text.add_field(name='bot', value='bot basis functions', inline=False)
    # await bot_client.send_message(context.message.author, embed=help_text)
    await bot_client.say(embed=help_text)


# Bot commands !bot <command>
@bot_client.command(pass_context=True)
async def bot(context, command='', *, message=''):
    if DEBUG_MODE:
        print(f'context.message.author = {context.message.author}\n' +
              f'context.message.server = {context.message.server}\n' +
              f'context.message.channel = {context.message.channel}\n' +
              f'context.message.content = {context.message.content}\n' +
              f'command = {command}\n' +
              f'message = {message}\n')

    # everyone can list admins
    if command == 'list-admins':
        output = f'{context.message.author.mention}\n' +\
                 f'The Bot owner is:\n' +\
                 f'@{BOT_OWNER}\n' +\
                 f'The following people are bot admins:\n'
        for admin in ADMIN_LIST:
            output += f'@{admin}\n'
        await bot_client.say(output)
        return

    # only bot owner can remove admins
    if command == 'remove-admin':
        # IF not bot owner exit
        if str(context.message.author) != BOT_OWNER:
            await bot_client.say(f'{context.message.author.mention} ' +
                                 f'you are not the bot owner, ignoring command!')
            return
        if message != '':
            if message in ADMIN_LIST:
                ADMIN_LIST.remove(message)
                core.list_to_file(ADMIN_LIST, 'admin-dev.list')
                await bot_client.say(f'{context.message.author.mention} ' +
                                     f'removed {message} successfully from admin list!')
                return
            else:
                await bot_client.say(f'{context.message.author.mention} ' +
                                     f'{message} is not in the admin list , so not removed!')
                return
        else:
            await bot_client.say(f'{context.message.author.mention} ' +
                                 f'you need to specify whom to remove from admin list!')
            return

    # only bot owner can add admins
    if command == 'add-admin':
        # IF not bot owner exit
        if str(context.message.author) != BOT_OWNER:
            await bot_client.say(f'{context.message.author.mention} ' +
                                 f'you are not the bot owner, ignoring command!')
            return
        if message != '':
            if message not in ADMIN_LIST:
                ADMIN_LIST.append(message)
                core.list_to_file(ADMIN_LIST, 'admin-dev.list')
                await bot_client.say(f'{context.message.author.mention} ' +
                                     f'added {message} successfully to admin list!')
                return
            else:
                await bot_client.say(f'{context.message.author.mention} ' +
                                     f'{message} is already in the admin list!')
                return
        else:
            await bot_client.say(f'{context.message.author.mention} ' +
                                 f'you need to specify whom to add to the admin list!')
            return

    # admins and bot owner can use this
    if command == 'unmute-channel':
        # IF not bot admin or owner exit
        allowed = False
        if str(context.message.author) in ADMIN_LIST:
            allowed = True
        if str(context.message.author) == BOT_OWNER:
            allowed = True
        if not allowed:
            await bot_client.say(f'{context.message.author.mention} ' +
                                 f'you are not the bot owner or an admin, ignoring command!')
            return
        if message != '':
            if message in MUTED_CHANNELS:
                MUTED_CHANNELS.remove(message)
                core.list_to_file(MUTED_CHANNELS, 'muted-channels-dev.list')
                await bot_client.say(f'{context.message.author.mention} ' +
                                     f'"{message}" was removed from the muted channels!')
                return
            else:
                await bot_client.say(f'{context.message.author.mention} ' +
                                     f'"{message}" is not muted so no action needed!')
                return
        else:
            if str(context.message.channel) in MUTED_CHANNELS:
                MUTED_CHANNELS.remove(str(context.message.channel))
                core.list_to_file(MUTED_CHANNELS, 'muted-channels-dev.list')
                await bot_client.say(f'{context.message.author.mention} ' +
                                     f'"{str(context.message.channel)}" ' +
                                     f'was removed from the muted channels!')
                return
            else:
                await bot_client.say(f'{context.message.author.mention} ' +
                                     f'"{str(context.message.channel)}" ' +
                                     f'is not muted so no action needed!')
                return

    # admins and bot owner can use this
    if command == 'mute-channel':
        # IF not bot admin or owner exit
        allowed = False
        if str(context.message.author) in ADMIN_LIST:
            allowed = True
        if str(context.message.author) == BOT_OWNER:
            allowed = True
        if not allowed:
            await bot_client.say(f'{context.message.author.mention} ' +
                                 f'you are not the bot owner or an admin, ignoring command!')
            return
        if message != '':
            channel_list = []
            for channel in bot_client.get_all_channels():
                if str(channel) not in MUTE_EXCEPTIONS:
                    channel_list.append(str(channel))
            if message in channel_list:
                if message not in MUTED_CHANNELS:
                    MUTED_CHANNELS.append(message)
                    core.list_to_file(MUTED_CHANNELS, 'muted-channels-dev.list')
                    await bot_client.say(f'{context.message.author.mention} ' +
                                         f'"{message}" was added to the muted channels!')
                    return
                else:
                    await bot_client.say(f'{context.message.author.mention} ' +
                                         f'"{message}" is already on the list of muted channels!')
                    return
            else:
                await bot_client.say(f'{context.message.author.mention} ' +
                                     f'"{message}" is not a valid channel to mute!')
                return
        else:
            if str(context.message.channel) not in MUTE_EXCEPTIONS:
                if str(context.message.channel) not in MUTED_CHANNELS:
                    MUTED_CHANNELS.append(str(context.message.channel))
                    core.list_to_file(MUTED_CHANNELS, 'muted-channels-dev.list')
                    await bot_client.say(f'{context.message.author.mention} ' +
                                         f'"{str(context.message.channel)}" ' +
                                         f'was added to the muted channels!')
                    return
                else:
                    await bot_client.say(f'{context.message.author.mention} ' +
                                         f'"{str(context.message.channel)}" ' +
                                         f'is already on the list of muted channels!')
                    return
            else:
                await bot_client.say(f'{context.message.author.mention} ' +
                                     f'You can not mute "{str(context.message.channel)}"\n' +
                                     f'It is in the list of exceptions')
                return


# Search function !search <name> or !search <appid>
@bot_client.command(pass_context=True)
async def search(context, *, search_text=''):
    if DEBUG_MODE:
        print(f'context.message.author = {context.message.author}\n' +
              f'context.message.server = {context.message.server}\n' +
              f'context.message.channel = {context.message.channel}\n' +
              f'context.message.content = {context.message.content}\n' +
              f'search_text = {search_text}\n')

    allowed = True
    if str(context.message.channel) in MUTED_CHANNELS:
        allowed = False
    if str(context.message.author) in ADMIN_LIST:
        allowed = True
    if str(context.message.author) == BOT_OWNER:
        allowed = True
    if not allowed:
        await bot_client.say(f'{context.message.author.mention} ' +
                             f'The bot is muted in this channel, ' +
                             f'try another channel or private message.')
        return

    # Initialize variables
    output = f''
    data = None
    game = None
    if search_text is not '':
        # If got a search string
        if game is None:
            # Assume saerch_string is a number and try a steamfront search for AppId
            try:
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
                for cite in soup.find_all('cite'):
                    print(cite)
                    print(str(cite).find('/app/'))
                    if int(str(cite).find('/app/')) != -1:
                        search_result = str(cite)  # str(soup.find_all('cite')[0])
                        search_result = search_result.strip('<cite>https://steamdb.info/app/')
                        search_result = search_result.strip('/</cite>')
                        search_result = str(re.sub(STRIP_PATTERN, '', search_result))
                        print(search_result)
                        game = steam_client.getApp(appid=search_result)
                        print('beep')
                        break
            except (IndexError, TypeError, errors.AppNotFound) as e:
                print(e)
                game = None
        if game is None:
            # Try a google search for 'site:steamdb.info+search_text
            search_url = f'{GOOGLE_URL}site%3Asteamdb.info+{search_text.replace(" ", "+")}'
            soup = BeautifulSoup(requests.get(url=search_url).text, 'lxml')
            try:
                for cite in soup.find_all('cite'):
                    print(cite)
                    print(str(cite).find('sub'))
                    if int(str(cite).find('sub')) != -1:
                        search_result = str(cite)  # str(soup.find_all('cite')[0])
                        search_result = search_result.strip('<cite>https://steamdb.info/app/')
                        search_result = search_result.strip('/</cite>')
                        search_result = re.sub(STRIP_PATTERN, '', search_result)
                        print(search_result)
                        game = steam_client.getApp(appid=search_result)
                        print('beep')
                        break
            except (IndexError, TypeError, errors.AppNotFound):
                game = None
        if game is None:
            # Try a google search for 'site:store.steampowered.com+search_text
            search_url = f'{GOOGLE_URL}site%3Astore.steampowered.com+{search_text.replace(" ", "+")}'
            soup = BeautifulSoup(requests.get(url=search_url).text, 'lxml')
            try:
                for cite in soup.find_all('cite'):
                    print(cite)
                    print(str(cite).find('AppId'))
                    if int(str(cite).find('AppId')) != -1:
                        search_result = str(cite)   # str(soup.find_all('cite')[0])
                        # search_result = search_result.strip('<cite>https://store.steampowered.com/forums/?AppId=<b>')
                        # search_result = search_result.strip('</b></cite>')
                        search_result = re.sub(STRIP_PATTERN, '', search_result)
                        print(search_result)
                        game = steam_client.getApp(appid=search_result)
                        print('beep')
                        break
            except (IndexError, TypeError, errors.AppNotFound):
                game = None
        if game is None:
            # Try a google search for 'site:store.steampowered.com+search_text
            search_url = f'{GOOGLE_URL}site%3Astore.steampowered.com+{search_text.replace(" ", "+")}'
            soup = BeautifulSoup(requests.get(url=search_url).text, 'lxml')
            try:
                for cite in soup.find_all('cite'):
                    print(cite)
                    print(str(cite).find('/sub/'))
                    if int(str(cite).find('/sub/')) != -1:
                        search_result = str(cite)   # str(soup.find_all('cite')[0])
                        # search_result = search_result.strip('<cite>https://store.steampowered.com/sub/')
                        # search_result = search_result.strip('/</cite>')
                        search_result = re.sub(STRIP_PATTERN, '', search_result)
                        print(search_result)
                        game = steam_client.getApp(appid=search_result)
                        print('beep')
                        break
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
