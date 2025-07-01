from time import sleep

import requests
import asyncio
from queue import Queue

# Asynchronous Class that checks status of a stream if its still live
# can be used as a coroutine (listener)
class StreamLiveChecker:
    def __init__(self, channel_name):
        self.channel_name = channel_name

        # listening interval
        self.listening_interval = 30

        # thread safe variable to pass data and flags
        self._is_live:bool = False

    # async doesnt seem to be compatible with the
    # proper property. Setter is wrapped such that is
    # cant be await (it is not awaitable)
    # @property
    # async def is_live(self):
    #     # xpa lagi kot yg ni, x perlu exclusive access rasanya
    #     return self._is_live
    #
    # @is_live.setter
    # async def is_live(self, value):
    #     # lock variable first to get exclusive access
    #     lock = asyncio.Lock()
    #
    #     async with lock:
    #         self._is_live = value

    async def getis_live(self):
        return self._is_live

    async def setis_live(self, value):
        # lock variable first to get exclusive access
        lock = asyncio.Lock()
        async with lock:
            self._is_live = value


    async def _check_channel(self):
        # Check if channel is livestreaming or not
        channelName = self.channel_name
        contents = requests.get('https://www.twitch.tv/' + channelName).content.decode('utf-8')

        if 'isLiveBroadcast' in contents:
            print(channelName + ' is live')
            await self.setis_live(True)

        else:
            print(channelName + ' is not live')
            #self.is_live = False
            await self.setis_live(False)


    async def listen_for_orders(self):
        '''
        Asynchronously check the orders queue for new incoming orders
        '''
        while True:
            await self._check_channel()
            # See, if you request too frequently, the host would think that you are abusing their service
            # Request for about every 30 sec
            await asyncio.sleep(self.listening_interval)

    async def run(self):
        await asyncio.gather(self.listen_for_orders())

    #TODO: let corountine wait until stream is live again, then

if __name__ == '__main__':
    # create buffer
    qq = asyncio.Queue(maxsize=1)

    channel_name = 'twitchplayspokemon'
    a = StreamLiveChecker(channel_name=channel_name)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(a.listen_for_orders())