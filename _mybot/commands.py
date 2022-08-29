from pygrambot.bot.botcommands.commands import NewCommand
from _mybot.handlers import StartHandler, ProcessingCatchMsg, CatchMultMsg, Form


class StartCommand(NewCommand):
    command = 'start'
    description = 'Starting bot.'
    handler = StartHandler


class CatchMsg(NewCommand):
    command = 'catch'
    handler = ProcessingCatchMsg


class Test(NewCommand):
    command = 'm'
    handler = CatchMultMsg.add_stop_commands(['stop'])


class StartForm(NewCommand):
    command = 'f'
    handler = Form
