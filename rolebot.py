import CONFIG
import zutils

import logging
import discord

logging.basicConfig(level=CONFIG.LOGGING_LEVEL)

CONFIG.ID_TO_ROLE = dict([(v, k) for k, v in CONFIG.ROLE_TO_ID.items()])
CONFIG.ciID_TO_ROLE = dict([(v, k.lower()) for k, v in CONFIG.ROLE_TO_ID.items()])
CONFIG.ciROLE_TO_ID = dict([(k.lower(), v) for k, v in CONFIG.ROLE_TO_ID.items()])

class MicroClient(discord.Client):
    commands = {}

    async def on_ready(self):
        logging.info("Ready!")

    async def on_connect(self):
        logging.info("Connected")

    async def on_message(self, message):
        if message.content.startswith(CONFIG.PREFIX):
            command_raw = message.content[len(CONFIG.PREFIX):].lower()
            if command_raw in self.commands:
                await self.commands[command_raw].execute(Contexter(message))

    @zutils.parametrized
    def command(func, self, name: str = None, **attrs):
        logging.info(f"Registered function: func: {func}, override name = {name}")
        command = Command(func, fname=name, **attrs)
        self.add_command(command)
        return command

    def add_command(self, command):
        self.commands[command.fname] = command

class Command:
    def __init__(self, func, pre=None, post=None, fname: str = None, **kwargs):
        self.fname = fname
        self.func = func
        self.pres = []
        self.posts = []
        self.case_sens = kwargs.get("case_sens", True)
        self.ack = kwargs.get("ack", "")
        if not self.fname:
            self.fname = func.__name__  # type:str
        self.fname = self.fname.lower()

        if self.ack == "react":
            async def add_checkmark(ctx):
                await ctx.m.add_reaction("✅")

            self.posts.append(add_checkmark)

        elif self.ack == "delete":
            async def delete_m(ctx):
                await ctx.m.delete()

            self.posts.append(delete_m)

    async def execute(self, ctx):
        [await pre(ctx) for pre in self.pres]
        await self.func(ctx)
        [await post(ctx) for post in self.posts]

class Contexter:
    def __init__(self, message):
        self.m = message

    def find_role(self, query):
        if isinstance(query, int):
            return next(role for role in self.m.guild.roles if role.id == query)
        if isinstance(query, str):
            try:
                res = next(role for role in self.m.guild.roles if role.name == query)
            except StopIteration:
                res = next(role for role in self.m.guild.roles if role.name.lower() == query.lower())
            return res

client = MicroClient()

# Offering
@client.command(ack=CONFIG.ACK_TYPE)
async def offering(ctx: Contexter):
    await ctx.m.author.add_roles(ctx.find_role("offering"))

@client.command(ack=CONFIG.ACK_TYPE)
async def offeringt(ctx: Contexter):
    if ctx.find_role("offering") in ctx.m.author.roles:
        await ctx.m.author.remove_roles(ctx.find_role("offering"))
    else:
        await ctx.m.author.add_roles(ctx.find_role("offering"))

@client.command(name="-offering", ack=CONFIG.ACK_TYPE)
async def deoffering(ctx):
    await ctx.m.author.remove_roles(ctx.find_role("offering"))

# Seeking
@client.command(ack=CONFIG.ACK_TYPE)
async def looking(ctx: Contexter):
    await ctx.m.author.add_roles(ctx.find_role("looking"))

@client.command(ack=CONFIG.ACK_TYPE)
async def lookingt(ctx: Contexter):
    if ctx.find_role("looking") in ctx.m.author.roles:
        await ctx.m.author.remove_roles(ctx.find_role("looking"))
    else:
        await ctx.m.author.add_roles(ctx.find_role("looking"))

@client.command(name="-looking", ack=CONFIG.ACK_TYPE)
async def delooking(ctx):
    await ctx.m.author.remove_roles(ctx.find_role("looking"))



client.run(CONFIG.BOT_TOKEN, bot=True)
