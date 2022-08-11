from pygrambot.exceptions.handlers import UpdateError
from pygrambot.data_objects.objects import UpdateDt
from pygrambot.bothandlers.commands import SendCommand
import asyncio


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
                            setattr(update_dt.message, fromk, update['message']['from'][fromk])
                    elif key == 'chat':
                        for chat in update['message']['chat']:
                            setattr(update_dt.chat, chat, update['message']['chat'][chat])
                    else:
                        setattr(update_dt.message, key, update['message'][key])
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
        pass

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
