from pygrambot.bot.botcommands.commands import NewCommand
from _mybot.handlers import StartHandler, ProcessingCatchMsg, CatchMultMsg


class StartCommand(NewCommand):
    command = '*'
    description = 'Starting bot.'
    handler = StartHandler


class CatchMsg(NewCommand):
    command = 'catch'
    handler = ProcessingCatchMsg


class Test(NewCommand):
    command = 'm'
    handler = CatchMultMsg.add_stop_commands(['stop'])
