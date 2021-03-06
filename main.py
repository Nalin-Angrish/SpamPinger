import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
load_dotenv()
import os, asyncio


help_command = commands.DefaultHelpCommand(no_category='All Commands')
bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), help_command=help_command)

tasks = {}

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print('------')


@bot.command(help="Spam Ping a user.", category="All Commands", aliases=["spam"])
async def ping(ctx, target:discord.User=None, *message):
	if target is None:
		return await ctx.send("Whom should i disturb?")
	if tasks.get(target.id) is None:
		await ctx.send(f"Spamming target: {target.mention}.")
		task = mass_ping(ctx, target, ' '.join(message))
		tasks[target.id] = {"task": task, "owner": ctx.author.id}
	else:
		await ctx.send(f"Don't you think i'm already spamming {target.mention}?")



@bot.command(help="Stop spam pinging a user.", category="All Commands")
async def stop(ctx, target:discord.User=None):
	if target is None:
		return await ctx.send("Please provide a user to stop pinging")
	task = tasks.get(target.id)
	if task:
		if task["owner"] == ctx.author.id or (get(ctx.guild.roles, name="Administrators") in ctx.message.author.roles):
			task['task'].cancel()
			tasks.pop(target.id)
			await ctx.send(f"Stopped spamming target: {target.mention}.")
		else:
			await ctx.send("Who do you think you are? You cannot do this.")
	else:
		await ctx.send(f"Lol, I'm not spamming {target.mention}. He is in peace.")



@bot.command(help="List the users who are being spammed.", category="All Commands")
async def list(ctx):
	pinglist = ""
	count = 1
	for t in tasks:
		user = await bot.fetch_user(t)
		print(user)
		pinglist += f"{count}) {str(user)}\n"
		count += 1
	if pinglist != "":
		await ctx.send("```\n"+pinglist+"\n```")
	else:
		await ctx.send("No one is currently being pinged.")
		





def mass_ping(ctx, target:discord.User, message):
	async def ping(ctx, target:discord.User, message):
		while True:
			await asyncio.sleep(1)
			await ctx.send(f"{target.mention} "+str(message))
	loop = asyncio.create_task(ping(ctx, target, message))
	return loop
	

bot.run(os.getenv('TOKEN'))