import asyncio
import logging
# Import stuff
import subprocess
from obs_handler import obs_handler
import threading
from common.xml_handler import XMLHandler
from game_controller.main import GameBoyAdvanceController
from twitch_handler.twitch_handler import Bot, BotManager
from twitch_handler.stream_live_checker import StreamLiveChecker
from obs_handler.obs_handler import OBSHandler
from twitch_handler.stream_listener import StreamListenerBot
from common.logsettings import LogSettings

global global_logger

async def startTask(twitchBotManager, streamListenerBot):
    # include the restart checking routine as well, or not it wouldnt run
    # it would run automatically if you used the bot.run() wrapper
    await asyncio.gather(
        twitchBotManager.run(),
        streamListenerBot.run()
    )

async def start_obs(obshandler: OBSHandler):
    await obshandler.start_obs()

if __name__ == '__main__':
    # Launch OBS
    #test = subprocess.call(r'C:\Program Files\obs-studio\bin\64bit\obs64.exe', cwd='C:/Program Files/obs-studio/bin/64bit/')

    #print(test)
    # oBSHandler = obs_handler.OBSHandler()
    # oBSHandler.call_obs()
    # print("Called OBS")
    # Launch Game

    # get current asych loop if there is any
    loop = asyncio.get_event_loop()

    # Instantiate logger
    logSettings = LogSettings()
    global_logger = logSettings
    global_logger.InitializeBasicLogSettings()

    # Get config data
    xmlHandler = XMLHandler('config.xml')
    global_logger.logger.info("Config loaded")
    # global_logger.info("Config loaded")

    # Instantiate game controller
    gameController = GameBoyAdvanceController()

    # Instantiate obs handler
    obsHandler = OBSHandler()
    loop.run_until_complete(start_obs(obsHandler))

    # Instantiate stream live checker
    streamLiveCheckerBot = StreamLiveChecker(channel_name=xmlHandler.channel_name)

    # Instantiate twitchbot
    twitchBotManager = BotManager(gameController, access_token=xmlHandler.access_token, channel_name=xmlHandler.channel_name,
                           obs_handler=obsHandler, stream_live_checker_handler=streamLiveCheckerBot)

    # twitchBot.run()
    # streamListenerBot = StreamListenerBot(channel_name=xmlHandler.channel_name,
    #                                       obs_handler=obsHandler,
    #                                       twitch_handler_coroutine= twitchBot)


# Start asych
    #asyncio.run(startTask(twitchBot, streamListenerBot))

    loop.run_until_complete(startTask(twitchBotManager, streamLiveCheckerBot))


