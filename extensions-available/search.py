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

from discord.ext import commands


class Search(commands.Cog):

    def __init__(self, client):
        self.client = client

    # TODO: remove this block
    # @commands.Cog.listener()
    # async def on_message_delete(self, message):
    #     await message.channel.send(f'Message deleted.')
    #
    # @commands.command()
    # async def ping(self, context):
    #     await context.send(f'Pong!')

    @commands.command()
    async def search(self, context):
        await context.send(f'searching')


def setup(client):
    client.add_cog(Search(client))
