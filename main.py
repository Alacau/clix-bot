import discord
from discord.ext import commands
import glob

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def test(ctx, *, kwarg):
    for image_file in glob.glob('png/*'):
        file_name = image_file.split('/')[-1]
        if file_name.startswith(f'{kwarg.lower()}'):
            await ctx.send(embed = discord.Embed(title = 'Title'))

@client.command()
async def pug(ctx, *, kwarg):
    for image_file in glob.glob('png/*'):
        file_name = image_file.split('/')[-1]
        if file_name.startswith(f'{kwarg.lower()}'):
            await ctx.send(file = discord.File(f'{image_file}'))

client.run('TOKEN')
