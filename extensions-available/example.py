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

from discord.ext import commands


class Example:

    def __init__(self, client):
        self.client = client

    async def on_message_delete(self, message):
        await self.client.send_message(message.channel, 'Message deleted.')

    @commands.command()
    async def ping(self):
        await self.client.say('Pong!')


def setup(client):
    client.add_cog(Example(client))
