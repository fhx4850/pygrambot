from pygrambot.bot.botcommands.commands import NewCommand
from p_bot.handlers import TestHandler, AaaaHandler


class TestCommand(NewCommand):
    command = 'test'
    description = 'test11111'
    handler = TestHandler


class Aa(NewCommand):
    command = 'aaa'
    description = 'aaa111'
    handler = AaaaHandler
