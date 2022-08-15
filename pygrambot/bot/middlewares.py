from pygrambot.data_objects.objects import UpdateDt
from config.bot_settings import RELATIVE_PATH_TO_MIDDLEWARES
import time
from pygrambot.bot.botcommands.api_commands import SendCommand
from config.bot_settings import TOKEN


class NewMiddleware:
    """
    Class for creating middleware.
    To do this, you need to inherit from this class and implement the run method.
    """
    _middlewares_list: list = []

    @classmethod
    async def run(cls, updatedt: UpdateDt) -> UpdateDt:
        """
        Middleware startup method.

        :return: UpdateDt
        """
        return updatedt


class ThrottlingMiddleware(NewMiddleware):
    time = time.time()
    timeout: float = 1
    message: str = 'Too many messages.'

    @classmethod
    async def set_message(cls, message: str):
        cls.message = message
        return cls

    @classmethod
    async def run(cls, updatedt: UpdateDt) -> UpdateDt:
        t1 = cls.time
        t2 = time.time()
        cls.time = time.time()
        if t1:
            msg_time = t2 - t1
            if msg_time < cls.timeout:
                await SendCommand(TOKEN).sendMessage(updatedt.chat.id, text=cls.message,
                                                     reply_to_message_id=updatedt.message.message_id)
                updatedt.message.text = ''
        return updatedt

    @classmethod
    def set_timeout_sec(cls, value: float):
        cls.timeout = value
        return cls


def get_middlewares() -> list[NewMiddleware]:
    """
    Returns a list with all middlewares.
    """
    middl = []
    for path in RELATIVE_PATH_TO_MIDDLEWARES:
        p = path.replace('/', '.').replace('\\', '.')
        if p.endswith('.'):
            p = p[:len(p) - 1] + p[len(p):]
        module = __import__(p, fromlist=['middlewares'])
        middl_module = getattr(module, 'middlewares')

        for i in middl_module.middlewareslist:
            middl.append(i)
    return middl
