import asyncio

import win32gui
from twitchio.ext import commands
from twitchio.ext import routines
from game_controller.main import IGameController, GameBoyAdvanceController
from obs_handler.obs_handler import OBSHandler
import logging
from twitch_handler.stream_live_checker import StreamLiveChecker
from common import window_switcher

class Bot(commands.Bot):
    def __init__(self, game_controller_obj: IGameController, access_token: str, channel_name,
                 obs_handler: OBSHandler = None, stream_live_checker_handler: StreamLiveChecker = None ):
        """
        Obj of game controller needs to be passed to bot

        :param game_controller:
        """
        # Handler of various stuffs
        self.game_controller_obj = game_controller_obj
        self.obs_handler = obs_handler
        self.stream_live_checker_handler = stream_live_checker_handler

        # logger
        self._logger = logging.getLogger(__name__)

        # credentials
        self._access_token = access_token
        self.channel_name = channel_name

        # # flags
        # # set the flag below to True if you want to debug restarting routine
        # self.is_officially_live_once = False

        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=access_token, prefix='!', initial_channels=[channel_name])

    ################################
    # SelfDefined
    ################################
    # async def close_and_reset(self):
    #     # needed to be done when OBS is restarted
    #     self._logger.info("Atttempting to restart bot")
    #     await self.close()
    #     self._logger.info("Bot succesfully closed")
    #     # welp, self.start doesnt work
    #     #await self.start()
    #     # make the bot kill itself
    #     self._logger.info("Bot ready to commit suicide")
    #
    # async def restart_obs(self):
    #     await self.obs_handler.restart_obs()
    #     # Reset the flag
    #     self.is_officially_live_once = False
    #     self._logger.info("OBS successfully restarted")
    #
    # async def set_focus_window_to_emulator(self):
    #     try:
    #         window_handle = window_switcher.find_window_by_title("VisualBoyAdvance-M 2.1.11")
    #         win32gui.SetForegroundWindow(window_handle)
    #         self._logger.info("Emulator is set as active window")
    #     except Exception as e:
    #         self._logger.error("Setting emulator as active window failed")
    #         self._logger.exception(e)
    #
    # async def check_if_need_restarting(self):
    #     """
    #     Routine to check if stream is dead due to server problem and needed to be restarted
    #     Will only run if stream live checker and obs handler is passed to the class
    #     """
    #     while True:
    #         await asyncio.sleep(20)
    #         if self.stream_live_checker_handler and self.obs_handler:
    #             # check if its already officially live once
    #             is_live = await self.stream_live_checker_handler.getis_live()
    #
    #             if not self.is_officially_live_once:
    #                 self._logger.info("TwitchBot went to see if first official live status is recorded")
    #             else:
    #                 self._logger.info("TwitchBot went to check if stream needed restarting")
    #
    #             # register that it is officially live
    #             if is_live and not self.is_officially_live_once:
    #                 self.is_officially_live_once = True
    #                 self._logger.info("Stream is recorded to be officially live")
    #
    #             if not is_live and self.is_officially_live_once:
    #                 await self.restart_obs()
    #                 await self.set_focus_window_to_emulator()
    #                 await self.close_and_reset()
    #                 await asyncio.sleep(10)

    ################################
    # Overriden methods
    ################################
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')

    ################################
    # Get game commands
    ################################
    @commands.command()
    async def up(self, ctx: commands.Context):
        self.game_controller_obj.move_front_keyboard()
        self._logger.info("Moved Up")

    @commands.command()
    async def down(self, ctx: commands.Context):
        self.game_controller_obj.move_back_keyboard()
        self._logger.info("Moved Down")

    @commands.command()
    async def left(self, ctx: commands.Context):
        self.game_controller_obj.move_left_keyboard()
        self._logger.info("Moved Left")

    @commands.command()
    async def right(self, ctx: commands.Context):
        self.game_controller_obj.move_right_keyboard()
        self._logger.info("Moved Right")

    @commands.command()
    async def lup(self, ctx: commands.Context):
        self.game_controller_obj.move_front_long_keyboard()
        self._logger.info("Long Pressed Up")

    @commands.command()
    async def ldown(self, ctx: commands.Context):
        self.game_controller_obj.move_back_long_keyboard()
        self._logger.info("Long Pressed Down")

    @commands.command()
    async def lleft(self, ctx: commands.Context):
        self.game_controller_obj.move_left_long_keyboard()
        self._logger.info("Long Pressed Left")

    @commands.command()
    async def lright(self, ctx: commands.Context):
        self.game_controller_obj.move_right_long_keyboard()
        self._logger.info("Long Pressed Right")

    @commands.command()
    async def a(self, ctx: commands.Context):
        self.game_controller_obj.press_accept_keyboard()
        self._logger.info("Pressed A")

    @commands.command()
    async def b(self, ctx: commands.Context):
        self.game_controller_obj.press_cancel_keyboard()
        self._logger.info("Pressed B")

    @commands.command()
    async def rfa(self, ctx: commands.Context):
        self.game_controller_obj.press_accept_repeatfire_keyboard()
        self._logger.info("Repeatfired A")

    @commands.command()
    async def rfb(self, ctx: commands.Context):
        self.game_controller_obj.press_cancel_repeatfire_keyboard()
        self._logger.info("Repeatfired B")

    @commands.command()
    async def st(self, ctx: commands.Context):
        self.game_controller_obj.press_pause_keyboard()
        self._logger.info("Pressed Start")

    @commands.command()
    async def se(self, ctx: commands.Context):
        self.game_controller_obj.press_pause_alt_keyboard()
        self._logger.info("Pressed Select")

    @commands.command()
    async def TabL(self, ctx: commands.Context):
        self.game_controller_obj.press_L1_keyboard()
        self._logger.info("Tabbed Left")

    @commands.command()
    async def TabR(self, ctx: commands.Context):
        self.game_controller_obj.press_R1_keyboard()
        self._logger.info("Tabbed Right")


class BotManager:
    def __init__(self,
                 game_controller_obj: IGameController, access_token: str, channel_name,
                 obs_handler: OBSHandler = None, stream_live_checker_handler: StreamLiveChecker = None,
                 ):
        """
        Wrapper class to manage the bot without altering the bot too much
        """

        # Handler of various stuffs
        self.game_controller_obj = game_controller_obj
        self.obs_handler = obs_handler
        self.stream_live_checker_handler = stream_live_checker_handler

        # logger
        self._logger = logging.getLogger(__name__)

        # credentials
        self._access_token = access_token
        self.channel_name = channel_name
        
        # flags
        # set the flag below to True if you want to debug restarting routine
        self.is_officially_live_once = False

        # intervals
        self.restart_routine_interval = 60

        # instantiate bot (make sure to put it last in the constructor)
        self.bot = self._instantiate_bot()

    def _instantiate_bot(self):
        bot_instance = Bot(self.game_controller_obj, self._access_token, self.channel_name,
                       self.obs_handler, self.stream_live_checker_handler)
        return bot_instance

    # async def start_bot(self, bot: Bot):
    #     await bot.start()

    async def close_and_reset(self):
        # needed to be done when OBS is restarted
        self._logger.info("Atttempting to restart bot")
        await self.bot.close()
        self._logger.info("Bot succesfully closed")
        # welp, self.start doesnt work
        # await self.start()
        # make the bot kill itself
        self._logger.info("Bot ready to commit suicide")
        del self.bot
        # reinstantiate bot
        self.bot = self._instantiate_bot()

        # let routine join the loop by making it as a future
        curr_loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.bot.start(), loop=curr_loop)

        self._logger.info("Bot was able to revive itself")

    async def restart_obs(self):
        await self.obs_handler.restart_obs()
        # Reset the flag
        self.is_officially_live_once = False
        self._logger.info("OBS successfully restarted")

    async def set_focus_window_to_emulator(self):
        try:
            window_list = []
            win32gui.EnumWindows( window_switcher.win_enum_handler_list, window_list)
            true_window_handle = window_switcher.search_window_with_name("VisualBoyAdvance-M 2.1.11",
                                                                         window_list)
            if true_window_handle:
                win32gui.SetForegroundWindow(true_window_handle)
                self._logger.info("Focus set to game window")
        except Exception as e:
            self._logger.error("Setting emulator as active window failed")
            self._logger.exception(e)

    async def check_if_need_restarting(self):
        """
        Routine to check if stream is dead due to server problem and needed to be restarted
        Will only run if stream live checker and obs handler is passed to the class
        """
        while True:
            await asyncio.sleep(self.restart_routine_interval)
            if self.stream_live_checker_handler and self.obs_handler:
                # check if its already officially live once
                is_live = await self.stream_live_checker_handler.getis_live()

                if not self.is_officially_live_once:
                    self._logger.info("TwitchBot went to see if first official live status is recorded")
                else:
                    self._logger.info("TwitchBot went to check if stream needed restarting")

                # register that it is officially live
                if is_live and not self.is_officially_live_once:
                    self.is_officially_live_once = True
                    self._logger.info("Stream is recorded to be officially live")

                if not is_live and self.is_officially_live_once:
                    await self.restart_obs()
                    # gotta sleep to wait for obs to complete starting up
                    await asyncio.sleep(15)
                    await self.set_focus_window_to_emulator()
                    await self.close_and_reset()
                    await asyncio.sleep(5)

    async def run(self):
        await asyncio.gather(self.bot.start(), self.check_if_need_restarting())

if __name__ == '__main__':
    # Testing the bot
    pokemonGameController = GameBoyAdvanceController()
    bot = Bot(pokemonGameController)
    bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
