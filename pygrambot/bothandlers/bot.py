from pygrambot.bothandlers.handlers import Receiver, MainHandler
from config.bot_settings import TOKEN
import asyncio


class Bot:
    def __init__(self):
        self.token = TOKEN
        queue = asyncio.Queue()
        self.receiver = Receiver(self.token, queue)
        self.main_handler = MainHandler(self.token, queue, 2)

    async def _handlers(self):
        """
        Start of all handlers for the bot to work.
        """

        await self.receiver.start()
        await self.main_handler.start()

    async def stop(self):
        """
        Stop all handlers.
        """

        await self.receiver.stop()
        await self.main_handler.stop()

    def start(self):
        """
        Start bot.
        """
        loop = asyncio.get_event_loop()
        try:
            print('Bot has been started.')
            loop.create_task(self._handlers())
            loop.run_forever()
        except KeyboardInterrupt:
            loop.run_until_complete(self.stop())
            print('\nBot has been stopped.')
