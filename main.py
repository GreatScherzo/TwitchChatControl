import asyncio
import logging
# Import stuff
import subprocess
from obs_handler import obs_handler
import threading
from common.xml_handler import XMLHandler
from game_controller.main import GameBoyAdvanceController, GameControllerFactory
from twitch_handler.twitch_handler import BotBase, BotManager
from twitch_handler.stream_live_checker import StreamLiveChecker
from obs_handler.obs_handler import OBSHandler
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
    gameControllerFactory = GameControllerFactory()
    gameController = gameControllerFactory.get_controller(xmlHandler.game_type)()

    # Instantiate obs handler
    obsHandler = OBSHandler()
    loop.run_until_complete(start_obs(obsHandler))

    # Instantiate stream live checker
    streamLiveCheckerBot = StreamLiveChecker(channel_name=xmlHandler.channel_name)

    # Instantiate twitchbot
    twitchBotManager = BotManager(gameController, access_token=xmlHandler.access_token,
                                  channel_name=xmlHandler.channel_name,
                                  game_type=xmlHandler.game_type, game_window_title=xmlHandler.game_window_title,
                                  obs_handler=obsHandler, stream_live_checker_handler=streamLiveCheckerBot)

    # Start async
    loop.run_until_complete(startTask(twitchBotManager, streamLiveCheckerBot))


