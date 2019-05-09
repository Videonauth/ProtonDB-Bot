#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# ProtonDB-Bot - extensions-available/example.py
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 23.04.2019 - 13:24
# Purpose: -
# Written for: Python 3.6.3
# ---------------------------------------------------------------------------

import discord
from discord.ext import commands
import modules.core as core


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    # @commands.Cog.listener()
    # async def on_message_delete(self, message):
    #     await message.channel.send(f'Message deleted.')

    @commands.command(pass_context=True, hidden=True)
    async def moderation(self, context, command: str = f'', value: str = f'', *, message: str = f''):
        """
        Ads or removes admins or moderators. Admins can only be set in by the bot owner.
        Moderators can be added or removed by either bot owner or admins.

        Usage: [prefix]moderation <(add|remove)> <(admin|moderator)> <name>

        Note: <name> has to be a full discord member name. Example: name#1234

        :param context: The message context.
        :param command: The command add or remove.
        :param value: What to add or remove usually either admin or moderator.
        :param message: The user to add or remove ad admin or moderator.
        """
        _config = core.json_to_dict(f'config/bot-config.json')
        _permissions = core.json_to_dict(f'config/permissions.json')
        if command == f'add':
            if value == f'admin':
                if str(context.author) == str(_config.get(f'bot_owner')):
                    if message not in list(_permissions.get(f'admins')):
                        # TODO: implement user check
                        _temp_list = list(_permissions.get(f'admins'))
                        _temp_list.append(message)
                        core.dict_update(_permissions, f'admins', _temp_list)
                        core.dict_to_json(_permissions, f'config/permissions.json')
                        _embed = discord.Embed(
                            title=f'Success:',
                            description=f'Added {message} to bot admins.',
                            colour=discord.Colour.green()
                        )
                        await context.send(embed=_embed)
                        return
                    else:
                        _embed = discord.Embed(
                            title=f'Warning:',
                            description=f'{message} is already a bot admin.',
                            colour=discord.Colour.orange()
                        )
                        await context.send(embed=_embed)
                        return
                else:
                    _embed = discord.Embed(
                        title=f'Failure:',
                        description=f'You are not the bot owner, ignoring command.',
                        colour=discord.Colour.red()
                    )
                    await context.send(embed=_embed)
                    return
            if value == f'moderator':
                if str(context.author) == str(_config.get(f'bot_owner'))\
                        or str(context.author) in list(_permissions.get(f'admins')):
                    if message not in list(_permissions.get(f'moderators')):
                        _temp_list = list(_permissions.get(f'moderators'))
                        _temp_list.append(message)
                        core.dict_update(_permissions, f'moderators', _temp_list)
                        core.dict_to_json(_permissions, f'config/permissions.json')
                        _embed = discord.Embed(
                            title=f'Success:',
                            description=f'Added {message} to bot moderators.',
                            colour=discord.Colour.green()
                        )
                        await context.send(embed=_embed)
                        return
                    else:
                        _embed = discord.Embed(
                            title=f'Warning:',
                            description=f'{message} is already a bot moderator.',
                            colour=discord.Colour.orange()
                        )
                        await context.send(embed=_embed)
                        return
                else:
                    _embed = discord.Embed(
                        title=f'Failure:',
                        description=f'You are not the bot owner or an admin, ignoring command.',
                        colour=discord.Colour.red()
                    )
                    await context.send(embed=_embed)
                    return
        if command == f'remove':
            if value == f'admin':
                if str(context.author) == str(_config.get(f'bot_owner')):
                    if message in list(_permissions.get(f'admins')):
                        _temp_list = list(_permissions.get(f'admins'))
                        _temp_list.remove(message)
                        core.dict_update(_permissions, f'admins', _temp_list)
                        core.dict_to_json(_permissions, f'config/permissions.json')
                        _embed = discord.Embed(
                            title=f'Success:',
                            description=f'Removed {message} as bot admin.',
                            colour=discord.Colour.green()
                        )
                        await context.send(embed=_embed)
                        return
                    else:
                        _embed = discord.Embed(
                            title=f'Warning:',
                            description=f'{message} is not a bot admin.',
                            colour=discord.Colour.orange()
                        )
                        await context.send(embed=_embed)
                        return
                else:
                    _embed = discord.Embed(
                        title=f'Failure:',
                        description=f'You are not the bot owner, ignoring command.',
                        colour=discord.Colour.red()
                    )
                    await context.send(embed=_embed)
                    return
            if value == f'moderator':
                if str(context.author) == str(_config.get(f'bot_owner'))\
                        or str(context.author) in list(_permissions.get(f'admins')):
                    if message in list(_permissions.get(f'moderators')):
                        _temp_list = list(_permissions.get(f'moderators'))
                        _temp_list.remove(message)
                        core.dict_update(_permissions, f'moderators', _temp_list)
                        core.dict_to_json(_permissions, f'config/permissions.json')
                        _embed = discord.Embed(
                            title=f'Success:',
                            description=f'Removed {message} as bot moderator.',
                            colour=discord.Colour.green()
                        )
                        await context.send(embed=_embed)
                        return
                    else:
                        _embed = discord.Embed(
                            title=f'Warning:',
                            description=f'{message} is not a bot moderator.',
                            colour=discord.Colour.orange()
                        )
                        await context.send(embed=_embed)
                        return
                else:
                    _embed = discord.Embed(
                        title=f'Failure:',
                        description=f'You are not the bot owner or an admin, ignoring command.',
                        colour=discord.Colour.red()
                    )
                    await context.send(embed=_embed)
                    return

    @commands.command(pass_context=True)
    async def alive(self, context):
        """
        A simple command to check if the bot is still present and running. Can be used by anyone.
        Does not obey mute settings.

        Usage: [prefix]alive

        :param context: The message context.
        """
        _embed = discord.Embed(
            title=f'Response:',
            description=f'I am here!',
            colour=discord.Colour.green()
        )
        await context.send(embed=_embed)


def setup(client):
    client.add_cog(Moderation(client))
