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
    print('READY.')

#TESTING AREA
@client.command()
async def test(ctx, *, frame):
    with open('test.json', 'r') as h:
        warframes = json.load(h)
    for item in warframes:
        for key in item:
            if key == frame:
                print(item[frame][0])
#TESTING AREA

#Core to organize into cog: frame, nuke, tricap,
@client.command()
async def frame(ctx, *, frame):
    frame = frame.lower()
    with open('warframes.json', 'r') as f:
        warframe = json.load(f)

    with open('warframe_img.json', 'r') as g:
        img = json.load(g)

    build = warframe[frame][0].split('/')
    build_file = build[-1]
    build_name = build_file[:-4]

    embed = discord.Embed(
    description = '',
    color = discord.Color.teal()
    )
    embed.set_author(name = build_name.upper(), icon_url = img[frame])
    embed.set_image(url = f'{warframe[frame][0]}')
    embed.set_thumbnail(url = img[frame])
    embed.add_field(name = 'Warframe', value = frame.capitalize())
    embed.set_footer(text = 'Got build suggestions? Send them to: EXAMPLE EMAIL', icon_url = img['choobi'])

    if len(warframe[frame]) > 1:
        for value in range(len(warframe[frame])):
            build = warframe[frame][value].split('/')
            build_file = build[-1]
            build_name = build_file[:-4]
            embed.set_author(name = f'{build_name.upper()}', icon_url = f'{img[frame]}')
            embed.set_image(url = f'{warframe[frame][value]}')
            embed.set_thumbnail(url = img[frame])
            await ctx.send(embed = embed)
    else:
        await ctx.send(embed = embed)

#Prefixes to organize into cog
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

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
    embed = discord.Embed(
    title = ':white_check_mark: Success!',
    description = f'Your prefix has been changed to `{prefix}`',
    color = discord.Color.magenta()
    )

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

    await ctx.send(embed = embed)

client.run('TOKEN')
