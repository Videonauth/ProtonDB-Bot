#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# ProtonDB-Bot - bot.py
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 25.04.19 - 14:33
# Purpose: -
# Written for: Python 3.7.1
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Defining version variable and github link
# ---------------------------------------------------------------------------
__version__ = f'0.0.17'
__github__ = f'https://raw.githubusercontent.com/Videonauth/ProtonDB-Bot/{__version__}/'

# ---------------------------------------------------------------------------
# Data dictionary for the bot
# ---------------------------------------------------------------------------
bot = dict()

# ---------------------------------------------------------------------------
# Importing time and fetching script start time. This has to stay on top.
# ---------------------------------------------------------------------------
try:
    import time
except ImportError:
    time = None
    print(f'Could not import "time" library. Shutting down.')
    exit(1)
else:
    bot.update({'start_time': time.time()})

# ---------------------------------------------------------------------------
# Importing datetime for providing in error output.
# ---------------------------------------------------------------------------
try:
    import datetime
except ImportError:
    datetime = None
    print(f'Could not import "datetime" library. Shutting down.')
    exit(1)

# ---------------------------------------------------------------------------
# Importing sys and fetching python version and platform.
# ---------------------------------------------------------------------------
try:
    import sys
except ImportError:
    sys = None
    print(f'Could not import "sys" library. Shutting down.')
    exit(1)
else:
    bot.update({f'python_platform': sys.platform})
    bot.update({f'python version': str(sys.version).split(' ')[0]})
    bot.update({f'gcc_version': str(sys.version).split('\n')[1].strip('[]GC ')})

# ---------------------------------------------------------------------------
# Importing os and doing file and directory integrity checks.
# ---------------------------------------------------------------------------
try:
    import os
except ImportError:
    os = None
    print(f'Could not import "os" library. Shutting down.')
    exit(1)
else:
    bot.update({f'runtime_path': os.path.dirname(os.path.realpath(__file__))})
    bot.update({f'name_self': str(__file__).strip('.').strip('/')})

# ---------------------------------------------------------------------------
# Importing logging
# ---------------------------------------------------------------------------
try:
    import logging
except ImportError:
    logging = None
    print(f'Could not import "logging" library. Shutting down.')
    exit(1)
else:
    bot.update({f'log_level': logging.DEBUG})

# ---------------------------------------------------------------------------
# Importing shutil
# ---------------------------------------------------------------------------
try:
    import shutil
except ImportError:
    shutil = None
    print(f'Could not import "shutil" library. Shutting down.')
    exit(1)

# ---------------------------------------------------------------------------
# Importing subprocess
# ---------------------------------------------------------------------------
try:
    import subprocess
except ImportError:
    subprocess = None
    print(f'Could not import "subprocess" library. Shutting down.')
    exit(1)

# ---------------------------------------------------------------------------
#  Importing dependencies or install them if missing.
# ---------------------------------------------------------------------------
try:
    import requests
    import discord
    from discord.ext.commands import Bot
    from discord.ext.commands import CommandNotFound
except ImportError:
    requests = None
    discord = None
    Bot = None
    CommandNotFound = None
    print(f'The bot relies on some external packages to be present for running. One or more of them are missing:'
          f' "requests, discord, steamfront, bs4". You can install with your favorite package manager.')
    print(f'Example: "pip3 install requests discord steamfront bs4".')
    exit(0)

# ---------------------------------------------------------------------------
# defining the input prompt the bot will use
# ---------------------------------------------------------------------------
bot.update({f'prompt': f'> '})

# ---------------------------------------------------------------------------
# defining the directory and file structure needed to load the bot.
# Each entry is a tuple of which first entry is the path to check and the
# second is the action to be taken if it not exists, the second part of the
# tuples are only relevant for the installation routine. directories are
# simple entries as they simply will get created.
# ---------------------------------------------------------------------------
bot.update({f'directories_expected': [
    f'config',
    f'modules',
    f'templates',
    f'logs',
    f'extensions-available',
    f'extensions-enabled',
]})
bot.update({f'files_expected': [
    [f'modules/core.py', f'install'],
    [f'templates/gitignore', f'install'],
    [f'.gitignore', f'create', f'templates/gitignore'],
    [f'LICENSE', f'install'],
    [f'extensions-available/example.py', f'install'],
]})

# ---------------------------------------------------------------------------
# Installation procedure (only makes sense when executing bot.py not on
# import.
# ---------------------------------------------------------------------------
if sys.argv and len(sys.argv) > 1:
    if sys.argv[1] == f'install':
        # Creating directories
        for _directory in bot.get(f'directories_expected'):
            if not os.path.exists(os.path.join(bot.get(f'runtime_path'), _directory)):
                try:
                    os.mkdir(os.path.join(bot.get(f'runtime_path'), _directory))
                except FileNotFoundError:
                    try:
                        os.makedirs(os.path.join(bot.get(f'runtime_path'), _directory))
                    except PermissionError:
                        print(f'Lacking permissions to create directories.')
                        exit(1)
                    else:
                        pass
                except FileExistsError:
                    pass
                except PermissionError:
                    print(f'Lacking permissions to create directories.')
                else:
                    pass
        # Create files
        for _name in bot.get(f'files_expected'):
            if not os.path.exists(os.path.join(bot.get(f'runtime_path'), _name[0])):
                if _name[1] == f'install':
                    _url = __github__ + _name[0]
                    _response = requests.get(url=_url)
                    if _response.status_code != 200:
                        print(f'The server sent {_response.status_code}. Shutting down.')
                        exit(1)
                    else:
                        try:
                            with open(os.path.join(bot.get(f'runtime_path'), _name[0]), mode='x') as _file:
                                _file.write(_response.text)
                        except FileExistsError:
                            try:
                                os.remove(os.path.join(bot.get(f'runtime_path'), _name[0]))
                                with open(os.path.join(bot.get(f'runtime_path'), _name[0]), mode='w') as _file:
                                    _file.write(_response.text)
                            except PermissionError:
                                print(f'Lacking permissions to create files.')
                                exit(1)
                        except PermissionError:
                            print(f'Lacking permissions to create files.')
                            exit(1)
                if _name[1] == f'create':
                    if len(_name) > 2:
                        if os.path.exists(os.path.join(bot.get(f'runtime_path'), _name[2])):
                            try:
                                shutil.copyfile(os.path.join(bot.get(f'runtime_path'), _name[2]),
                                                os.path.join(bot.get(f'runtime_path'), _name[0]))
                            except PermissionError:
                                print(f'Lacking permissions to create files.')
                                exit(1)
                        else:
                            _url = __github__ + _name[2]
                            _response = requests.get(url=_url)
                            if _response.status_code != 200:
                                print(f'The server sent {_response.status_code}. Shutting down.')
                                exit(1)
                            else:
                                try:
                                    with open(os.path.join(bot.get(f'runtime_path'), _name[0]), mode='x') as _file:
                                        _file.write(_response.text)
                                except FileExistsError:
                                    try:
                                        os.remove(os.path.join(bot.get(f'runtime_path'), _name[0]))
                                        with open(os.path.join(bot.get(f'runtime_path'), _name[0]), mode='w') as _file:
                                            _file.write(_response.text)
                                    except PermissionError:
                                        print(f'Lacking permissions to create files.')
                                        exit(1)
                                except PermissionError:
                                    print(f'Lacking permissions to create files.')
                                    exit(1)
        exit(0)
else:
    for _directory in bot.get(f'directories_expected'):
        if not os.path.exists(os.path.join(bot.get(f'runtime_path'), _directory)):
            print(f'The bot is missing files it needs to run. Shutting down.')
            print(f'You can fix this by issuing "{bot.get("name_self")} install".')
            exit(1)
    for _file in bot.get(f'files_expected'):
        if not os.path.exists(os.path.join(bot.get(f'runtime_path'), _file[0])):
            print(f'The bot is missing files it needs to run. Shutting down.')
            print(f'You can fix this by issuing "{bot.get("name_self")} install".')
            exit(1)

# ---------------------------------------------------------------------------
# Importing modules/core.py.
# ---------------------------------------------------------------------------
try:
    import modules.core as core
except ImportError:
    core = None
    print(f'Something is amiss, could not import botcore. Shutting down.')
    exit(1)

# ---------------------------------------------------------------------------
# Initialize logging.
# ---------------------------------------------------------------------------
core.setup_logger(f'bot-log', os.path.join(bot.get('runtime_path'), f'logs/bot.log'))
_bot_log = logging.getLogger(f'bot-log')
_bot_log.debug(f'Bot starting up.')

# ---------------------------------------------------------------------------
# Loading permission lists or create empty files if absent.
# ---------------------------------------------------------------------------
if os.path.exists(os.path.join(bot.get(f'runtime_path'), f'config/permissions.json')):
    core.dict_update(bot,
                     f'permissions',
                     core.json_to_dict(os.path.join(bot.get(f'runtime_path'), f'config/permissions.json')))
else:
    _permissions = dict()
    _permissions.update({
        f'admins': [],
        f'moderators': []
    })
    core.dict_to_json(_permissions, os.path.join(bot.get(f'runtime_path'), f'config/permissions.json'))
    core.dict_update(bot, f'permissions', _permissions)

# ---------------------------------------------------------------------------
# Loading config file or create config if absent.
# ---------------------------------------------------------------------------
if os.path.exists(os.path.join(bot.get(f'runtime_path'), f'config/bot-config.json')):
    core.dict_update(bot,
                     f'config',
                     core.json_to_dict(os.path.join(bot.get(f'runtime_path'), f'config/bot-config.json')))
else:
    _config = dict()
    _bot_log.info(f'Please enter the bot token:')
    _input = input(bot.get(f'prompt'))
    core.dict_update(_config, f'bot_token', _input)
    _bot_log.info(f'Please enter the bot owner:')
    _input = input(bot.get(f'prompt'))
    core.dict_update(_config, f'bot_owner', _input)
    _bot_log.info(f'Please enter the bot prefix:')
    _input = input(bot.get(f'prompt'))
    core.dict_update(_config, f'bot_prefix', _input)
    core.dict_update(_config, f'muted_channels', [])
    core.dict_to_json(_config, os.path.join(bot.get(f'runtime_path'), f'config/bot-config.json'))
    core.dict_update(bot, f'config', _config)

# ---------------------------------------------------------------------------
# Defining clients.
# ---------------------------------------------------------------------------
_bot_client = Bot(command_prefix=dict(bot.get(f'config')).get(f'bot_prefix'))

# ---------------------------------------------------------------------------
# defining basic bot functions
# ---------------------------------------------------------------------------
@_bot_client.event
async def on_ready():
    """
    Sends message to stdout and bot.log when the bot has started up
    """
    _bot_log.info('Logged in as:')
    _bot_log.info(f'Bot name: {_bot_client.user.name}')
    _bot_log.info(f'Bot ID: {_bot_client.user.id}')
    _bot_log.info(f'Bot is ready.')
    return


@_bot_client.event
async def on_command_error(context, error):
    """
    Avoids discord.py to throw an error on a wrong command.

    :param context: The message context.
    :param error: The error message.
    :raises: error if the error is not CommandNotFound
    """
    if isinstance(error, CommandNotFound) and context:
        return
    raise error

# ---------------------------------------------------------------------------
# defining basic bot owner commands
# ---------------------------------------------------------------------------
@_bot_client.command(pass_context=True, hidden=True)
async def load(context, extension: str = ''):
    """
    Loads an extension module into the chat bot

    Usage: [prefix]load <extension>

    :param context: The message context.
    :param extension: The extension name to load.
    """
    if str(context.message.author) == str(dict(bot.get(f'config')).get(f'bot_owner')):
        try:
            _bot_client.load_extension(f'extensions-enabled.' + extension)
            _bot_log.info(f'Loaded extension: {extension}.')
            await context.send(f'{context.message.author.mention}\nLoaded {extension}.')
            return
        except (AttributeError, ImportError, discord.ClientException):
            _bot_log.warning(f'Failed to load extension: {_extension}.')
            await context.send(f'{context.message.author.mention}\nFailed to load {extension}.')
            return
    else:
        await context.send(f'{context.message.author.mention}\nYou are not the bot owner, ignoring command.')
        return


@_bot_client.command(pass_context=True, hidden=True)
async def unload(context, extension: str = ''):
    """
    Unloads an extension from the chat bot

    Usage: [prefix]unload <extension>

    :param context: The message context
    :param extension: The extension name to unload.
    """
    if str(context.message.author) == str(dict(bot.get(f'config')).get(f'bot_owner')):
        try:
            _bot_client.unload_extension(f'extensions-enabled.' + extension)
            _bot_log.info(f'Unloaded extension: {extension}')
            await context.send(f'{context.message.author.mention}\nUnloaded {extension}.')
            return
        except (AttributeError, ImportError, discord.ClientException):
            _bot_log.warning(f'Failed to unload extension: {extension}')
            await context.send(f'{context.message.author.mention}\nFailed to unload {extension}.')
            return
    else:
        await context.send(f'{context.message.author.mention}\nYou are not the bot owner, ignoring command.')
        return


@_bot_client.command(pass_context=True, hidden=True)
async def shutdown(context):
    """
    Shuts the bot down.

    Usage: [prefix]shutdown

    :param context: The message context
    """
    if str(context.message.author) == str(dict(bot.get(f'config')).get(f'bot_owner')):
        await context.send(f'{context.message.author.mention}\nGoodbye cruel world.')
        await _bot_client.logout()
        await _bot_client.close()
        exit(0)
    else:
        await context.send(f'{context.message.author.mention}\nYou are not the bot owner, ignoring command.')
        return


@_bot_client.command(pass_context=True, hidden=True)
async def modules(context, extension: str):
    """
    Lists the extension available or enabled.

    Usage: [prefix]modules <(available|enabled)>

    :param context: The message context
    :param extension: A string containing either available or enabled
    """
    if str(context.message.author) == str(dict(bot.get(f'config')).get(f'bot_owner')):
        _output = f''
        if extension == f'available':
            _path_available = os.path.join(bot.get(f'runtime_path'), f'extensions-available/')
            _list_available = [
                f.replace('.py', '') for f in os.listdir(_path_available) if os.path.isfile(os.path.join(
                    _path_available,
                    f
                ))
            ]
            for _module in _list_available:
                _output += f'{_module}\n'
            if _output:
                await context.send(f'{context.message.author.mention}\nThe following modules are available:\n{_output}')
            else:
                await context.send(f'{context.message.author.mention}\nThe are no modules available.')
            return
        elif extension == f'enabled':
            _path_enabled = os.path.join(bot.get(f'runtime_path'), f'extensions-enabled/')
            _list_enabled = [
                f.replace('.py', '') for f in os.listdir(_path_enabled) if os.path.isfile(os.path.join(
                    _path_enabled,
                    f
                ))
            ]
            for _module in _list_enabled:
                _output += f'{_module}\n'
            if _output:
                await context.send(f'{context.message.author.mention}\nThe following modules are enabled:\n{_output}')
            else:
                await context.send(f'{context.message.author.mention}\nThe are no modules enabled.')
        else:
            return
    else:
        await context.send(f'{context.message.author.mention}\nYou are not the bot owner, ignoring command.')
        return


@_bot_client.command(pass_context=True, hidden=True)
async def enable(context, extension: str):
    """
    Enables an extension if it is present in 'extensions-available'.

    Usage: [prefix]enable <extension>

    :param context: The message context.
    :param extension: The extension name to enable
    """
    if str(context.message.author) == str(dict(bot.get(f'config')).get(f'bot_owner')):
        if os.path.exists(os.path.join(bot.get(f'runtime_path'), f'extensions-available/{extension}.py')):
            try:
                core.bash_command([
                    f'ln',
                    f'-s',
                    os.path.join(bot.get(f'runtime_path'), f'extensions-available/{extension}.py'),
                    os.path.join(bot.get(f'runtime_path'), f'extensions-enabled/{extension}.py')
                ])
            except PermissionError:
                await context.send(f'{context.message.author.mention}\nThe bot is lacking permissions'
                                   f'to create symlinks.')
                return
            else:
                try:
                    _bot_client.load_extension(f'extensions-enabled.{extension}')
                except (AttributeError, ImportError):
                    _bot_log.warning(f'Failed to load extension: {_extension}')
                else:
                    await context.send(f'{context.message.author.mention}\nEnabled {extension}')
                finally:
                    return
        else:
            await context.send(f'{context.message.author.mention}\nThis is not a known extension.')
            return
    else:
        await context.send(f'{context.message.author.mention}\nYou are not the bot owner, ignoring command.')
        return


@_bot_client.command(pass_context=True, hidden=True)
async def disable(context, extension: str):
    """
    Disables an extension if it is present in 'extensions-available'.

    Usage: [prefix]disable <extension>

    :param context: The message context.
    :param extension: The extension name to disable
    """
    if str(context.message.author) == str(dict(bot.get(f'config')).get(f'bot_owner')):
        if os.path.exists(os.path.join(bot.get(f'runtime_path'), f'extensions-enabled/{extension}.py')):
            try:
                os.remove(os.path.join(bot.get(f'runtime_path'), f'extensions-enabled/{extension}.py'))
            except PermissionError:
                await context.send(f'{context.message.author.mention}\nThe bot is lacking permissions'
                                   f'to remove symlinks.')
                return
            else:
                try:
                    _bot_client.unload_extension(f'extensions-enabled.{extension}')
                except (AttributeError, ImportError):
                    _bot_log.warning(f'Failed to load extension: {_extension}')
                else:
                    await context.send(f'{context.message.author.mention}\nDisabled {extension}')
                finally:
                    return
        else:
            await context.send(f'{context.message.author.mention}\nThe {extension} is not enabled. Nothing to disable.')
    else:
        await context.send(f'{context.message.author.mention}\nYou are not the bot owner, ignoring command.')
        return


@_bot_client.command(pass_context=True, hidden=True)
async def mute(context, channel: str):
    """
    Adds a channel on the list of muted channels.

    Usage: [prefix]mute <channel>

    :param context: The message context.
    :param channel: The channel to mute without the leading #
    """
    if str(context.message.author) == str(dict(bot.get(f'config')).get(f'bot_owner')):
        if channel not in dict(bot.get(f'config')).get(f'muted_channels'):
            _channels = list()
            for _channel in _bot_client.get_all_channels():
                _channels.append(str(_channel))
            if channel in _channels:
                _temp_config = dict(bot.get(f'config'))
                _muted_channels = list(_temp_config.get(f'muted_channels'))
                _muted_channels.append(channel)
                core.dict_update(_temp_config, f'muted_channels', _muted_channels)
                core.dict_update(bot, f'config', _temp_config)
                core.dict_to_json(_temp_config, os.path.join(bot.get(f'runtime_path'), f'config/bot-config.json'))
                await context.send(f'{context.message.author.mention}\nMuted {channel}.')
                return
            else:
                await context.send(f'{context.message.author.mention}\n{channel} is not a valid channel.')
                return
        else:
            await context.send(f'{context.message.author.mention}\n{channel} is already muted. Doing nothing.')
            return
    else:
        await context.send(f'{context.message.author.mention}\nYou are not the bot owner, ignoring command.')
        return


@_bot_client.command(pass_context=True, hidden=True)
async def unmute(context, channel):
    """
    Removes a channel from the list of muted channels.

    Usage: [prefix]unmute <channel>

    :param context: The message context.
    :param channel: The channel to unmute without the leading #
    """
    if str(context.message.author) == str(dict(bot.get(f'config')).get(f'bot_owner')):
        _temp_config = dict(bot.get(f'config'))
        _muted_channels = list(_temp_config.get(f'muted_channels'))
        if channel in _muted_channels:
            _muted_channels.remove(channel)
            core.dict_update(_temp_config, f'muted_channels', _muted_channels)
            core.dict_update(bot, f'config', _temp_config)
            core.dict_to_json(_temp_config, os.path.join(bot.get(f'runtime_path'), f'config/bot-config.json'))
            await context.send(f'{context.message.author.mention}\nUnmuted {channel}.')
            return
        else:
            await context.send(f'{context.message.author.mention}\n{channel} is not muted. Doing nothing.')
            return
    else:
        await context.send(f'{context.message.author.mention}\nYou are not the bot owner, ignoring command.')
        return


if __name__ == '__main__':
    # ---------------------------------------------------------------------------
    # Loading extensions.
    # ---------------------------------------------------------------------------
    _path = os.path.join(bot.get(f'runtime_path'), f'extensions-enabled/')
    _extension_list = [f.replace('.py', '') for f in os.listdir(_path) if os.path.isfile(os.path.join(_path, f))]
    for _extension in _extension_list:
        try:
            _bot_client.load_extension('extensions-enabled.' + _extension)
            _bot_log.info(f'Loaded extension: {_extension} from {_extension}.py')
        except (AttributeError, ImportError):
            _bot_log.warning(f'Failed to load extension: {_extension}')

    # ---------------------------------------------------------------------------
    # Run bot.
    # ---------------------------------------------------------------------------
    try:
        _bot_client.run(dict(bot.get(f'config')).get(f'bot_token'))
        print(f'\n')
    except KeyboardInterrupt:
        print(f'\nKeyboard interrupt detected. Shutting down.')
        exit(1)
    else:
        exit(0)
