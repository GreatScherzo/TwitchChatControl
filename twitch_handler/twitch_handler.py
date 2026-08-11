import asyncio

import win32gui
from twitchio.ext import commands
from twitchio.ext import routines
from game_controller.main import IGameController, GameBoyAdvanceController, UmamusumeController
from obs_handler.obs_handler import OBSHandler
import logging
from twitch_handler.stream_live_checker import StreamLiveChecker
from common import window_switcher
import time
import enum
from typing import Type

class BotBase(commands.Bot):
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

        # help dict
        self.help_dict:dict = {}

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

    # @commands.command()
    # async def hello(self, ctx: commands.Context):
    #     # Here we have a command hello, we can invoke our command with our prefix and command name
    #     # e.g ?hello
    #     # We can also give our commands aliases (different names) to invoke with.
    #
    #     # Send a hello back!
    #     # Sending a reply back to the channel is easy... Below is an example.
    #     await ctx.send(f'Hello {ctx.author.name}!')

    ################################
    # help
    ################################
    @commands.command(name='help', aliases=('controls', 'control'))
    async def disp_help(self, ctx: commands.Context) :
        """
        Display help to chat
        """
        message = ["{0}: {1}".format(keys, self.help_dict[keys]) for keys in self.help_dict]
        message_str = '\n'.join(message)
        await ctx.send(message_str)

    ################################
    # event join
    ################################
    async def event_join(self, channel, user):
        userdata = await self.fetch_users([user.name])

        message = ("Hi {0}! Welcome to the stream. "
                   "\n Use !help to display the commands available").format(userdata)

        await channel.send(message)


    ################################
    # Combo command
    ################################
    @commands.command()
    async def combo(self, ctx, *commands):
        for curr_comm in commands:
            # switch to every type of command
            if curr_comm == 'up':
                await self.up(ctx)
            elif curr_comm == 'down':
                await self.down(ctx)
            elif curr_comm == 'left':
                await self.left(ctx)
            elif curr_comm == 'right':
                await self.right(ctx)

    ################################
    # Get game commands
    ################################
    @commands.command()
    async def up(self, ctx: commands.Context):
        pass

    @commands.command()
    async def down(self, ctx: commands.Context):
        pass

    @commands.command()
    async def left(self, ctx: commands.Context):
        pass

    @commands.command()
    async def right(self, ctx: commands.Context):
        pass

class GameBoyAdvBot(BotBase):
    def __init__(self, game_controller_obj: IGameController, access_token: str, channel_name,
                 obs_handler: OBSHandler = None, stream_live_checker_handler: StreamLiveChecker = None ):

        super().__init__(game_controller_obj, access_token, channel_name, obs_handler, stream_live_checker_handler)

        self.help_dict = {'!combo, !multi': 'Used to input mutiple commands in order, eg: !combo l l a',

                          '!up, !u': 'Press up,',
                          '!down, !d': 'Press down',
                          '!left, !l':'Press left',
                          '!right, !r': 'Press right',

                          '!a !accept': 'Press A',
                          '!b, !cancel': 'Press B',

                          '!st': 'Press Start,',
                          '!select, !d': 'Press Select',

                          '!tabl, !tl': 'Press L',
                          '!tabr, !tr': 'Press R',

                          '!lup, !lu': 'Long press up,',
                          '!ldown, !ld': 'Long press down',
                          '!lleft, !ll': 'Long press left',
                          '!lright, !lr': 'Long press right',

                          '!rfa, !rfaccept': 'Rapid fire A',
                          '!rfb, !rfcancel': 'Rapid fire B',
                          }

    ################################
    # Help
    ################################
    @commands.command(name='help', aliases=('controls', 'control'))
    async def disp_help(self, ctx: commands.Context) :
        """
        Display help to chat
        """
        message = ["{0}: {1}".format(keys, self.help_dict[keys]) for keys in self.help_dict]
        message_str = ';     \n'.join(message)

        # The API can only send 500 words at a time, so we have to do that
        wordpersend = 500
        for i in range(0, len(message_str), wordpersend):
            await ctx.send(message_str[i:i+wordpersend])

    ################################
    # event join
    ################################
    async def event_join(self, channel, user):
        userdata = await self.fetch_users([user.name])

        message = ("Hi @{0}! Welcome to the stream. "
                   "\n Use !help to display the commands available").format(userdata[0].name)
        await channel.send(message)
        self._logger.info("User {0} joined the stream".format(userdata[0].name))

    ################################
    # Combo
    ################################
    @commands.command(aliases=('multi',))
    async def combo(self, ctx: commands.Context, *args):
        for curr_comm in args:
            # switch to every type of command
            # direction
            await asyncio.sleep(1)
            if curr_comm in ['up', 'u']:
                await self.up(ctx)
            elif curr_comm in ['down', 'd']:
                await self.down(ctx)
            elif curr_comm in ['left', 'l']:
                await self.left(ctx)
            elif curr_comm in ['right', 'r']:
                await self.right(ctx)
            # long press series
            elif curr_comm in ['lup', 'lu']:
                await self.lup(ctx)
            elif curr_comm in ['ldown', 'ld']:
                await self.ldown(ctx)
            elif curr_comm in ['lleft', 'll']:
                await self.lleft(ctx)
            elif curr_comm in ['lright', 'lr']:
                await self.lright(ctx)
            # accept, decline
            elif curr_comm in ['accept', 'a']:
                await self.accept(ctx)
            elif curr_comm in ['cancel', 'b']:
                await self.cancel(ctx)
            # rapid fire series
            elif curr_comm in ['rfaccept', 'rfa']:
                await self.rfaccept(ctx)
            elif curr_comm in ['rfcancel', 'rfb']:
                await self.rfcancel(ctx)
            # start, select
            elif curr_comm in ['start', 'st']:
                await self.st(ctx)
            elif curr_comm in ['select', 'sel']:
                await self.select(ctx)
            # tab buttons
            elif curr_comm in ['tabl', 'tl']:
                await self.tabl(ctx)
            elif curr_comm in ['tabr', 'tr']:
                await self.tabr(ctx)
            # default
            else:
                self._logger.info("Invalid command in combo")

    ################################
    # Get game commands
    ################################
    @commands.command(aliases=('u',))
    async def up(self, ctx: commands.Context):
        self.game_controller_obj.move_front_keyboard()
        self._logger.info("Moved Up")

    @commands.command(aliases=('d',))
    async def down(self, ctx: commands.Context):
        self.game_controller_obj.move_back_keyboard()
        self._logger.info("Moved Down")

    @commands.command(aliases=('l',))
    async def left(self, ctx: commands.Context):
        self.game_controller_obj.move_left_keyboard()
        self._logger.info("Moved Left")

    @commands.command(aliases=('r',))
    async def right(self, ctx: commands.Context):
        self.game_controller_obj.move_right_keyboard()
        self._logger.info("Moved Right")

    @commands.command(aliases=('lu',))
    async def lup(self, ctx: commands.Context):
        self.game_controller_obj.move_front_long_keyboard()
        self._logger.info("Long Pressed Up")

    @commands.command(aliases=('ld',))
    async def ldown(self, ctx: commands.Context):
        self.game_controller_obj.move_back_long_keyboard()
        self._logger.info("Long Pressed Down")

    @commands.command(aliases=('ll',))
    async def lleft(self, ctx: commands.Context):
        self.game_controller_obj.move_left_long_keyboard()
        self._logger.info("Long Pressed Left")

    @commands.command(aliases=('lr',))
    async def lright(self, ctx: commands.Context):
        self.game_controller_obj.move_right_long_keyboard()
        self._logger.info("Long Pressed Right")

    @commands.command(aliases=('a',))
    async def accept(self, ctx: commands.Context):
        self.game_controller_obj.press_accept_keyboard()
        self._logger.info("Pressed A")

    @commands.command(aliases=('b',))
    async def cancel(self, ctx: commands.Context):
        self.game_controller_obj.press_cancel_keyboard()
        self._logger.info("Pressed B")

    @commands.command(aliases=('rfa',))
    async def rfaccept(self, ctx: commands.Context):
        self.game_controller_obj.press_accept_repeatfire_keyboard()
        self._logger.info("Rapid fired A")

    @commands.command(aliases=('rfb',))
    async def rfcancel(self, ctx: commands.Context):
        self.game_controller_obj.press_cancel_repeatfire_keyboard()
        self._logger.info("Rapid fired B")

    @commands.command()
    async def st(self, ctx: commands.Context):
        self.game_controller_obj.press_pause_keyboard()
        self._logger.info("Pressed Start")

    @commands.command(aliases=('sel',))
    async def select(self, ctx: commands.Context):
        self.game_controller_obj.press_pause_alt_keyboard()
        self._logger.info("Pressed Select")

    @commands.command(aliases=('tl',))
    async def tabl(self, ctx: commands.Context):
        self.game_controller_obj.press_L1_keyboard()
        self._logger.info("Tabbed Left")

    @commands.command(aliases=('tr',))
    async def tabr(self, ctx: commands.Context):
        self.game_controller_obj.press_R1_keyboard()
        self._logger.info("Tabbed Right")

class PCGameBot(BotBase):
    def __init__(self, game_controller_obj: IGameController, access_token: str, channel_name,
                 obs_handler: OBSHandler = None, stream_live_checker_handler: StreamLiveChecker = None ):

        super().__init__(game_controller_obj, access_token, channel_name, obs_handler, stream_live_checker_handler)

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
    async def enter(self, ctx: commands.Context):
        self.game_controller_obj.press_accept_keyboard()
        self._logger.info("Pressed A")

    @commands.command()
    async def cancel(self, ctx: commands.Context):
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

class UmamusumeBot(PCGameBot):
    def __init__(self, game_controller_obj: UmamusumeController, access_token: str, channel_name,
                 obs_handler: OBSHandler = None, stream_live_checker_handler: StreamLiveChecker = None ):

        super().__init__(game_controller_obj, access_token, channel_name, obs_handler, stream_live_checker_handler)

        self.help_dict = {'!combo, !multi': 'Used to input mutiple commands in order, ex: !combo l l o',

                          '!up, !u': 'Move cursor up,',
                          '!down, !d': 'Move cursor down',
                          '!left, !l':'Move cursor left',
                          '!right, !r': 'Move cursor right',

                          '!enter, !o, !confirm': 'Confirm dialog, click on button',
                          '!cancel, !x, !back': 'Cancel, move back to previous menu',

                          '!scrollup, !su': 'Scroll up if there\'s a scroll bar',
                          '!scrolldown, !sd': 'Scroll down if there\'s a scroll bar',

                          '!pause, !p': 'Shortcut to open up pause menu during career',
                          '!tableft, !tl': 'Shift tab to left',
                          '!tabright, !tr': 'Shift tab to right',

                          '!juke, !j': 'Switch right menu to Jukebox',
                          '!sparks, !s': 'Switch right menu to Sparks',
                          '!log': 'Switch right menu to Log',
                          '!careerprofile, !cp': 'Switch right menu to Career Profile',
                          '!agenda, !a': 'Switch right menu to Agenda',
                          '!itemrequest, !ir': 'Switch right menu to Agenda',
                          '!menu, !m': 'Switch right menu to Menu',
                          }

    ################################
    # Help
    ################################
    @commands.command(name='help', aliases=('controls', 'control'))
    async def disp_help(self, ctx: commands.Context) :
        """
        Display help to chat
        """
        message = ["{0}: {1}".format(keys, self.help_dict[keys]) for keys in self.help_dict]
        message_str = ';     \n'.join(message)

        # The API can only send 500 words at a time, so we have to do that
        wordpersend = 500
        for i in range(0, len(message_str), wordpersend):
            await ctx.send(message_str[i:i+wordpersend])

    ################################
    # event join
    ################################
    async def event_join(self, channel, user):
        userdata = await self.fetch_users([user.name])

        message = ("Hi @{0}! Welcome to the stream. "
                   "\n Use !help to display the commands available").format(userdata[0].name)
        await channel.send(message)
        self._logger.info("User {0} joined the stream".format(userdata[0].name))

    ################################
    # Combo
    ################################
    @commands.command(aliases=('multi',))
    async def combo(self, ctx, *args):
        for curr_comm in args:
            # switch to every type of command
            if curr_comm in ['up', 'u']:
                await self.up(ctx)
            elif curr_comm in ['down', 'd']:
                await self.down(ctx)
            elif curr_comm in ['left', 'l']:
                await self.left(ctx)
            elif curr_comm in ['right', 'r']:
                await self.right(ctx)
            #
            elif curr_comm in ['enter', 'o', 'confirm']:
                await self.enter(ctx)
            elif curr_comm in ['cancel', 'x', 'back']:
                await self.cancel(ctx)
            #
            elif curr_comm in ['scrollup', 'su']:
                await self.scrollup(ctx)
            elif curr_comm in ['scrolldown', 'sd']:
                await self.scrolldown(ctx)
            #
            elif curr_comm in ['pause', 'p']:
                await self.pause(ctx)
            #
            elif curr_comm in ['tableft', 'tl']:
                await self.tableft(ctx)
            elif curr_comm in ['tabright', 'tr']:
                await self.tabright(ctx)
            #
            elif curr_comm in ['juke', 'j']:
                await self.juke(ctx)
            elif curr_comm in ['sparks', 's']:
                await self.sparks(ctx)
            elif curr_comm in ['log']:
                await self.loggame(ctx)
            elif curr_comm in ['careerprofile', 'cp']:
                await self.careerprofile(ctx)
            elif curr_comm in ['agenda', 'a']:
                await self.agenda(ctx)
            elif curr_comm in ['itemrequest', 'ir']:
                await self.itemrequest(ctx)
            elif curr_comm in ['menu', 'm']:
                await self.menu(ctx)
            else:
                self._logger.info("Invalid command in combo")

    ################################
    # Get game commands
    ################################

    @commands.command(aliases=('u',))
    async def up(self, ctx: commands.Context):
        self.game_controller_obj.move_front_keyboard()
        self._logger.info("Moved Up")

    @commands.command(aliases=('d',))
    async def down(self, ctx: commands.Context):
        self.game_controller_obj.move_back_keyboard()
        self._logger.info("Moved Down")

    @commands.command(aliases=('l',))
    async def left(self, ctx: commands.Context):
        self.game_controller_obj.move_left_keyboard()
        self._logger.info("Moved Left")

    @commands.command(aliases=('r',))
    async def right(self, ctx: commands.Context):
        self.game_controller_obj.move_right_keyboard()
        self._logger.info("Moved Right")

   # Accept, decline
    @commands.command(aliases=('o', 'confirm',))
    async def enter(self, ctx: commands.Context):
        self.game_controller_obj.press_accept_keyboard()
        self._logger.info("Pressed enter")

    @commands.command(aliases=('x', 'back'))
    async def cancel(self, ctx: commands.Context):
        self.game_controller_obj.press_cancel_keyboard()
        self._logger.info("Pressed cancel")

    # Scroll up, down
    @commands.command(aliases=('su',))
    async def scrollup(self, ctx: commands.Context):
        self.game_controller_obj.scroll_up_keyboard()
        self._logger.info("Scrolled up")

    @commands.command(aliases=('sd',))
    async def scrolldown(self, ctx: commands.Context):
        self.game_controller_obj.scroll_up_keyboard()
        self._logger.info("Scrolled Down")

    # shorcut to menu
    @commands.command(aliases=('p',))
    async def pause(self, ctx: commands.Context):
        self.game_controller_obj.move_back_keyboard()
        self._logger.info("Opened career pause menu")

    # tab left, right
    @commands.command(aliases=('tl',))
    async def tableft(self, ctx: commands.Context):
        self.game_controller_obj.tab_left_keyboard()
        self._logger.info("Tabbed left")

    @commands.command(aliases=('tr',))
    async def tabright(self, ctx: commands.Context):
        self.game_controller_obj.tab_right_keyboard()
        self._logger.info("Tabbed right")

    # shortcut to right menu tabs
    @commands.command(aliases=('j',))
    async def juke(self, ctx: commands.Context):
        self.game_controller_obj.shortcut_jukebox_keyboard()
        self._logger.info("Shifted right menu to Jukebox tab")

    @commands.command(aliases=('s',))
    async def sparks(self, ctx: commands.Context):
        self.game_controller_obj.shortcut_sparks_keyboard()
        self._logger.info("Shifted right menu to Sparks tab")

    @commands.command(name='log')
    async def loggame(self, ctx: commands.Context):
        self.game_controller_obj.shortcut_log_keyboard()
        self._logger.info("Shifted right menu to Log tab")

    @commands.command(aliases=('cp',))
    async def careerprofile(self, ctx: commands.Context):
        self.game_controller_obj.shortcut_careerprofile_keyboard()
        self._logger.info("Shifted right menu to Career Profile tab")

    @commands.command(aliases=('a',))
    async def agenda(self, ctx: commands.Context):
        self.game_controller_obj.shortcut_agenda_keyboard()
        self._logger.info("Shifted right menu to Agenda tab")

    @commands.command(aliases=('ir',))
    async def itemrequest(self, ctx: commands.Context):
        self.game_controller_obj.shortcut_itemrequest_keyboard()
        self._logger.info("Shifted right menu to Item Request tab")

    @commands.command(aliases=('m',))
    async def menu(self, ctx: commands.Context):
        self.game_controller_obj.shortcut_menu_keyboard()
        self._logger.info("Shift right menu to Menu tab")


# class BotType(enum.Enum):
#     gameboy_adv = 1
#     pc_game = 2


class BotFactory:
    """
    Author: Zarin
    Bot Factory
    """

    def __init__(self):
        pass

    def get_bot(self, bot_type: str):
        """
        below returns the class, not the instance of the class
        instantiate it after getting it
        Args:
            datatable_type: insert datatabletype selections

        Returns:

        """
        if bot_type == 'gameboy_adv':
            return GameBoyAdvBot
        elif bot_type == 'pc_game':
            return PCGameBot
        elif bot_type == 'umamusume':
            return UmamusumeBot
        else:
            raise Exception("Bot not found from selection")


class BotManager:
    def __init__(self,
                 game_controller_obj: IGameController, access_token: str, channel_name,
                 game_type, game_window_title,
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

        # other configs from config.xml. Isnt used for instatiation of bot
        self._game_type = game_type
        self._game_window_title = game_window_title

        # flags
        # set the flag below to True if you want to debug restarting routine
        self.is_officially_live_once = False
        self.timer_needs_restart = False # flag to reset official live listener timeout timer
        self.is_foreground_correct = False #

        # intervals
        self.restart_routine_interval = 60
        self.official_live_timeout = 20 # minutes

        # instantiate bot (make sure to put it last in the constructor)
        self.bot = self._instantiate_bot(self._game_type)

    def _instantiate_bot(self, game_type):
        """
        Private method to instantiate the bot.
        Requires game_type as a method
        """
        botFactory = BotFactory()
        ChosenBot = botFactory.get_bot(bot_type=game_type)
        bot_instance = ChosenBot(self.game_controller_obj, self._access_token, self.channel_name,
                                 self.obs_handler, self.stream_live_checker_handler)
        return bot_instance

    # async def start_bot(self, bot: Bot):
    #     await bot.start()

    async def close_and_reset(self):
        # needed to be done when OBS is restarted
        self._logger.info("Atttempting to restart bot")

        # sometimes, the bot thinks that it itself is None, and it produces an AttributeError
        try:
            await self.bot.close()
        except AttributeError as e:
            self._logger.error("Attribute error occurred when closing."
                               "Probably that weird Null error again where the closing timing is faster")
        except Exception as e:
            self._logger.error("Unexpected error occurred, {0}".format(e))

        self._logger.info("Bot succesfully closed")
        # welp, self.start doesnt work
        # await self.start()
        # make the bot kill itself
        self._logger.info("Bot ready to commit suicide")
        del self.bot
        # reinstantiate bot
        self.bot = self._instantiate_bot(self._game_type)

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
        attempts = 3
        is_successful = False
        # attempt several times (sometimes, timeout happens. probably due to the emulator not responding well)
        for attempt in range(attempts):
            try:
                window_list = []
                win32gui.EnumWindows( window_switcher.win_enum_handler_list, window_list)
                # true_window_handle = window_switcher.search_window_with_name("VisualBoyAdvance-M 2.1.11",
                #                                                              window_list)
                true_window_handle = window_switcher.search_window_with_name(self._game_window_title,
                                                                             window_list)
                if true_window_handle:
                    win32gui.SetForegroundWindow(true_window_handle)
                    self._logger.info("Focus set to game window")
                    is_successful = True
                    self.is_foreground_correct = True
                else:
                    self._logger.warning("Emulator window not found. Please check config")
                    self.is_foreground_correct = False
            except Exception as e:
                self._logger.error("Setting emulator as active window failed")
                self._logger.exception(e)
                self.is_foreground_correct = False

            if is_successful:
                break

            await asyncio.sleep(5)

    async def check_if_need_restarting(self):
        """
        Routine to check if stream is dead due to server problem and needed to be restarted
        Will only run if stream live checker and obs handler is passed to the class
        """
        # set 15 min timeout as server error can occur before official live status is recorded
        official_live_check_start = time.time()

        while True:
            await asyncio.sleep(self.restart_routine_interval)

            # if the handlers have been input into the class
            if self.stream_live_checker_handler and self.obs_handler:
                if self.timer_needs_restart == True:
                    # reset timeout timer
                    official_live_check_start = time.time()
                    self.timer_needs_restart = False
                else:
                    pass

                # check if its already officially live once
                is_live = await self.stream_live_checker_handler.getis_live()

                if not self.is_officially_live_once:
                    self._logger.info("TwitchBot went to see if first official live status is recorded")
                else:
                    self._logger.info("TwitchBot went to check if stream needed restarting")

                # Check timer
                if not self.is_officially_live_once:
                    end = time.time()
                    timeout_secs = self.official_live_timeout * 60

                    # restart if timeout
                    if end-official_live_check_start > timeout_secs:
                        self._logger.info("Timeout occur. Restarting the stream")
                        await self.restart_procedure()

                # register that it is officially live
                if is_live and not self.is_officially_live_once:
                    self.is_officially_live_once = True
                    self._logger.info("Stream is recorded to be officially live")

                # case if already officially live but didnt receive live status
                if not is_live and self.is_officially_live_once:
                    await self.restart_procedure()

    async def restart_procedure(self):
        # set restart timer flag
        self.timer_needs_restart = True
        await self.restart_obs()
        # gotta sleep to wait for obs to complete starting up
        await asyncio.sleep(10)
        await self.set_focus_window_to_emulator()
        while (self.is_foreground_correct == False):
            # the game needs to be in front, or all would be naught
            await self.set_focus_window_to_emulator()
        await self.close_and_reset()
        await asyncio.sleep(5)

    async def run(self):
        await self.set_focus_window_to_emulator()
        await asyncio.gather(self.bot.start(), self.check_if_need_restarting())

if __name__ == '__main__':
    # Testing the bot
    pokemonGameController = GameBoyAdvanceController()
    bot = BotBase(pokemonGameController)
    bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
