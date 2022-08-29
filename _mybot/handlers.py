from pygrambot.bot.bothandlers.handlers import CustomHandler, CatchMultipleMessages, CatchNextMessage, FormHandler
from pygrambot.bot.botcommands.api_commands import SendCommand
from config.bot_settings import TOKEN


class StartHandler(CustomHandler):
    async def start(self):
        print('start')


class ProcessingCatchMsg(CatchNextMessage):
    async def handle(self, updatedt):
        print(updatedt.message.text)


class CatchMultMsg(CatchMultipleMessages):
    async def handle(self, updatedt):
        await SendCommand(TOKEN).sendMessage(updatedt.chat.id, updatedt.message.text)


class Form(FormHandler):
    fields = ['test1', 'test2', 'test3']

    async def handle(self, updatedt):
        print(updatedt.message.id, updatedt.data['form'])
