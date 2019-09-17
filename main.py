import discord
from discord.ext import commands
import json

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def test(ctx, *, kwarg):
    pass

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "."

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json' , 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.command()
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

    await ctx.send(f'Your prefix has been changed to {prefix}')

@client.command()
async def frame(ctx, *, frame):
    embed = discord.Embed(
    title = f'{frame.upper()}',
    description = f'A basic {frame.capitalize()} build!',
    color = discord.Color.teal()
    )

    embed.set_image(url = f'https://cutt.ly/{frame}')
    embed.set_footer(text = f'{prefix}umbral <frame> for a stronger warframe build!')
    await ctx.send(embed = embed)

@client.command()
async def nuke(ctx, *, frame):
    embed = discord.Embed(
    title = 'Title',
    description = 'Description',
    color = discord.Color.blue()
    )

    embed.set_image(url = f'https://cutt.ly/nuke_{frame}')

@client.command()
async def pug(ctx, *, kwarg):
    for image_file in glob.glob('png/*'):
        file_name = image_file.split('/')[-1]
        if file_name.startswith(f'{kwarg.lower()}'):
            await ctx.send(file = discord.File(f'{image_file}'))


client.run('TOKEN')
