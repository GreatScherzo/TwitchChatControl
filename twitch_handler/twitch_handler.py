from twitchio.ext import commands
from game_controller.main import IGameController, PokemonGameController
from typing import Type
# hardcoded auth config here

access_token = ''

refresh_token = ''

client_id = ''


class Bot(commands.Bot):

    def __init__(self, game_controller_obj: IGameController):
        """
        Obj of game controller needs to be passed to bot

        :param game_controller:
        """
        self.GameControllerObj = game_controller_obj

        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=access_token, prefix='?', initial_channels=['greatscherzo'])

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
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        self.GameControllerObj.move_front_keyboard()


    @commands.command()
    async def down(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')


if __name__ == '__main__':
    # Testing the bot
    pokemonGameController = PokemonGameController()
    bot = Bot(pokemonGameController)
    bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
