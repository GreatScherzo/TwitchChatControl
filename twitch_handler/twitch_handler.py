from twitchio.ext import commands
from game_controller.main import IGameController, GameBoyAdvanceController
from typing import Type
# hardcoded auth config for debug


class Bot(commands.Bot):

    def __init__(self, game_controller_obj: IGameController, access_token: str):
        """
        Obj of game controller needs to be passed to bot

        :param game_controller:
        """
        self.GameControllerObj = game_controller_obj

        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=access_token, prefix='!', initial_channels=['TwitchPlayStuff'])

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
        self.GameControllerObj.move_front_keyboard()
        print("Moved Up")

    @commands.command()
    async def down(self, ctx: commands.Context):
        self.GameControllerObj.move_back_keyboard()
        print("Moved Down")

    @commands.command()
    async def left(self, ctx: commands.Context):
        self.GameControllerObj.move_left_keyboard()
        print("Moved Left")

    @commands.command()
    async def right(self, ctx: commands.Context):
        self.GameControllerObj.move_right_keyboard()
        print("Moved Right")

    @commands.command()
    async def lup(self, ctx: commands.Context):
        self.GameControllerObj.move_front_long_keyboard()
        print("Long Pressed Up")

    @commands.command()
    async def ldown(self, ctx: commands.Context):
        self.GameControllerObj.move_back_long_keyboard()
        print("Long Pressed Down")

    @commands.command()
    async def lleft(self, ctx: commands.Context):
        self.GameControllerObj.move_left_long_keyboard()
        print("Long Pressed Left")

    @commands.command()
    async def lright(self, ctx: commands.Context):
        self.GameControllerObj.move_right_long_keyboard()
        print("Long Pressed Right")

    @commands.command()
    async def a(self, ctx: commands.Context):
        self.GameControllerObj.press_accept_keyboard()
        print("Pressed A")

    @commands.command()
    async def b(self, ctx: commands.Context):
        self.GameControllerObj.press_cancel_keyboard()
        print("Pressed B")

    @commands.command()
    async def rfa(self, ctx: commands.Context):
        self.GameControllerObj.press_accept_repeatfire_keyboard()
        print("Repeatfired A")

    @commands.command()
    async def rfb(self, ctx: commands.Context):
        self.GameControllerObj.press_cancel_repeatfire_keyboard()
        print("Repeatfired B")

    @commands.command()
    async def st(self, ctx: commands.Context):
        self.GameControllerObj.press_pause_keyboard()
        print("Pressed Start")

    @commands.command()
    async def se(self, ctx: commands.Context):
        self.GameControllerObj.press_pause_alt_keyboard()
        print("Pressed Select")

    @commands.command()
    async def TabL(self, ctx: commands.Context):
        self.GameControllerObj.press_L1_keyboard()
        print("Tabbed Left")

    @commands.command()
    async def TabR(self, ctx: commands.Context):
        self.GameControllerObj.press_R1_keyboard()
        print("Tabbed Right")

if __name__ == '__main__':
    # Testing the bot
    pokemonGameController = GameBoyAdvanceController()
    bot = Bot(pokemonGameController)
    bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
