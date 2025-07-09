import asyncio
import logging

import win32gui

from common import window_switcher
from obs_handler.obs_handler import OBSHandler
from twitch_handler.stream_live_checker import StreamLiveChecker


class StreamListenerBot():
    """
    Bot to listen to stream heartbeat and restart if necessary
    Made is sep
    """
    def __init__(self, channel_name,
                 obs_handler: OBSHandler = None,
                 twitch_handler_coroutine = None):
        """
        Obj of game controller needs to be passed to bot

        :param game_controller:
        """
        self.obs_handler = obs_handler
        self.channel_name = channel_name

        # Flag to tell if stream is officially live once
        self.is_live_once = False

        # Place coroutines as attributes
        self.stream_live_checker = StreamLiveChecker(channel_name=channel_name)
        self.stream_live_checker_coroutine = self.stream_live_checker.listen_for_orders()
        self.stream_listener_coroutine = self.restart_stream()
        self.twitch_handler_coroutine = twitch_handler_coroutine

        # Logger
        self._logger = logging.getLogger(__name__)

    ################################
    # Self defined
    ################################
    async def restart_stream(self):
        """
        Restart OBS if it is not live
        """
        #for debugging
        self.is_live_once = True

        while True:
            await asyncio.sleep(10)
            self._logger.info("SteamListener went to check status")
            if self.stream_live_checker._is_live == True and self.is_live_once==False:
                self.is_live_once = True
                self._logger.info("Stream is recorded to be officially live")

            if self.stream_live_checker._is_live == False and self.is_live_once==True:
                await self.obs_handler.restart_obs()
                # Reset the live once flag back
                self.is_live_once = False

                try:
                    window_handle = window_switcher.find_window_by_title("VisualBoyAdvance-M 2.1.11")
                    win32gui.SetForegroundWindow(window_handle)
                except Exception as e:
                    self._logger.error("Setting emulator as active window failed")
                    self._logger.exception(e)

                # below is suppose to add routine to the running loop
                # but ive never quite tried it yet lol
                # better use this one
                # https://stackoverflow.com/questions/34499400/how-to-add-a-coroutine-to-a-running-asyncio-loop
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(self.twitch_handler_coroutine).cancel()

                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(self.twitch_handler_coroutine)


    async def run(self):
        """
        Taking inspiration from twitchio bot
        """
        # try:
        #     # if theres already an active async loop
        #     loop = asyncio.get_running_loop()
        #     loop.create_task(self.stream_listener_coroutine)
        #     loop.create_task(self.stream_live_checker_coroutine)
        #
        #     is_async = True
        # except RuntimeError:
        #     # it will raise this error if there's no active loop
        #     # asyncio.create_task(self.stream_listener_coroutine)
        #     # asyncio.create_task(self.stream_live_checker_coroutine)
        #
        #     await asyncio.gather(self.stream_listener_coroutine,
        #                          self.stream_live_checker_coroutine)
        await asyncio.gather(self.stream_listener_coroutine,
                             self.stream_live_checker_coroutine)
