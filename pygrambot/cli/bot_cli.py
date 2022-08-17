import fire
import os
from pygrambot.cli.templates import templates_list
from pygrambot.bot.bothandlers.bot import Bot


class BotCli:
    def init(self):
        if not os.path.exists('conf'):
            os.mkdir('conf')
        for template in templates_list:
            with open(os.path.join('conf/', template['name']), 'w+') as f:
                with open(template['path'], 'r') as sf:
                    f.write(sf.read())

    def start(self):
        Bot().start()


fire.Fire(BotCli)
