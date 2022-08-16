from pygrambot.exceptions.main_exc import UpdateError
from pygrambot.bot.botcommands.api_commands import SendCommand
import asyncio
from pygrambot.data_objects.objects import UpdateDt
from pygrambot.bot.botcommands.commands import get_commands
from pygrambot.bot.middlewares import get_middlewares, CatchNextMessageMiddleware


class Receiver:
    """
    Starts a bot listening thread to collect messages.
    """
    def __init__(self, token: str, queue: asyncio.Queue):
        self.token = token
        self.sendcommand = SendCommand(self.token)
        self.queue: asyncio.Queue = queue
        self._task: asyncio.Task = None

    async def _receve(self):
        """
        Continuously receive updates and write them to the queue.
        """
        offset = 0
        while True:
            updates = await self.parse_updates(await self.sendcommand.getUpdates(timeout=60, offset=offset))
            for upd in updates:
                offset = upd.update_id + 1
                self.queue.put_nowait(upd)

    async def parse_updates(self, updates: dict) -> list[UpdateDt]:
        """
        The method takes a dictionary of bot update values and converts each message to an UpdateDt data type.
        """
        updates_list = []
        if updates['ok']:
            for update in updates['result']:
                # create new instance UpdateDt
                update_dt = UpdateDt()
                update_dt.new_message()
                update_dt.new_chat()

                update_dt.update_id = update['update_id']
                for key in update['message']:
                    if key == 'from':
                        for fromk in update['message']['from']:
                            setattr(update_dt.message, fromk, str(update['message']['from'][fromk]))
                    elif key == 'chat':
                        for chat in update['message']['chat']:
                            setattr(update_dt.chat, chat, str(update['message']['chat'][chat]))
                    else:
                        setattr(update_dt.message, key, str(update['message'][key]))
                updates_list.append(update_dt)
            return updates_list
        else:
            raise UpdateError()

    async def start(self):
        self._task = asyncio.create_task(self._receve())

    async def stop(self):
        self._task.cancel()


class MainHandler:
    """
    The class starts an uninterrupted thread that receives an update from a queue created by the receiver.
    Then it sends them for processing by other handlers.
    """
    def __init__(self, token: str, queue: asyncio.Queue, concurrent_workers: int):
        self.token = token
        self.sendcommand = SendCommand(self.token)
        self.queue = queue
        self._tasks: list[asyncio.Task] = []
        self.concurrent_workers = concurrent_workers

    async def handle_update(self, upd: UpdateDt):
        """
        Processing a single message.
        """

        try:
            u = upd
            for middl in get_middlewares():
                if middl.enable:
                    u = await middl.run(upd)
            for command in await get_commands():
                if u.message.text == command.command:
                    command.handler.updatedt = u
                    await command.handler().start()
                    # When one handler is executed, the others are unavailable.
                    break
                elif command.command == '*':
                    command.handler.updatedt = u
                    await command.handler().start()
        except Exception as e:
            raise e

    async def _handler(self):
        """
        Collection of new updates and processing by the base handler.
        """
        while True:
            upd = await self.queue.get()
            await self.handle_update(upd)
            self.queue.task_done()

    async def start(self):
        self._tasks = [asyncio.create_task(self._handler()) for _ in range(self.concurrent_workers)]

    async def stop(self):
        await self.queue.join()
        for task in self._tasks:
            task.cancel()


class CustomHandler:
    """
    Class for adding custom handlers.
    To use it, you need to create a handler class and inherit from this class,
    the callback is performed in the start method.
    """

    updatedt: UpdateDt = None

    async def start(self):
        """
        Handler start.
        """
        raise NotImplementedError


class CatchNextMessage(CustomHandler):
    """
    The handler passes the captured message to the CatchNextMessageMiddleware.
    """
    async def start(self):
        await CatchNextMessageMiddleware.add_message(self.updatedt.message.id)


class CatchMessageHandler(CustomHandler):
    """
    Handling the captured message.
    """
    async def start(self):
        try:
            if 'catch_msg' in self.updatedt.data and self.updatedt.data['catch_msg']:
                for data in self.updatedt.data['catch_msg']:
                    await self.handle(data)
                    del self.updatedt.data['catch_msg'][0]
        except Exception as e:
            pass

    async def handle(self, updatedt):
        pass
