from pygrambot.bot.bothandlers.handlers import CustomHandler
from pygrambot.bot.botcommands.api_commands import SendCommand
from pygrambot.telegram.keyboards import ReplyKeyboardMarkup, KeyboardButton
from config.bot_settings import TOKEN


class TestHandler(CustomHandler):
    _send = SendCommand(TOKEN)

    test = [
        [
            KeyboardButton(text='test')
        ]
    ]

    async def start(self):
        await self._send.sendMessage(chat_id=self.updatedt.chat.id, text=self.updatedt.message.text,
                                     reply_markup=ReplyKeyboardMarkup(self.test, resize_keyboard=True))


class AaaaHandler(CustomHandler):
    _send = SendCommand(TOKEN)

    async def start(self):
        await self._send.sendMessage(chat_id=self.updatedt.chat.id, text=self.updatedt.message.text, reply_to_message_id=self.updatedt.message.message_id)

