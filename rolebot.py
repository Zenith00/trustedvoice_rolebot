import CONFIG
import zutils

import logging
import discord

logging.basicConfig(level=CONFIG.LOGGING_LEVEL)

class MicroClient(discord.Client):
    commands = {}

    async def on_ready(self):
        logging.info("Ready!")

    async def on_connect(self):
        logging.info("Connected")

    async def on_message(self, message):
        content = message.content # type:str
        if message.content.startswith(CONFIG.PREFIX):

    @zutils.parametrized
    def command(self, name: str = None, **attrs):
        def deco(func):
            return Command(func, fname=name, **attrs)
        return deco

    def add_command(self):
        pass


class Command:
    def __init__(self, func: function, fname: str = None, **kwargs):
        self.func = func
        self.case_sens = kwargs.get("case_sens", True)
        if not fname:
            self.fname = self.func.__name__  # type:str


@MicroClient.command(case_sens=False)
def offering(ctx):
    pass


MicroClient.run(CONFIG.BOT_TOKEN, bot=False)

