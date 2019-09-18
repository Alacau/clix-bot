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
async def test():
    pass
#TESTING AREA

#Core to organize into cog: frame, nuke, tricap,
@client.command()
async def frame(ctx, *, frame):
    frame = frame.lower()

    with open('warframes.json', 'r') as h:
        warframes = json.load(h)

    for item in warframes:
        for key in item:
            if key == frame:
                build = item[frame][0].split('/')
                build_file = build[-1]
                build_name = build_file[:-4]

                embed = discord.Embed(
                description = '',
                color = discord.Color.teal()
                )
                embed.set_author(name = build_name.upper(), icon_url = item['thumbnail'])
                embed.set_image(url = f'{item[frame][0]}')
                embed.set_thumbnail(url = item['thumbnail'])
                embed.add_field(name = item['author'], value = item['link'])
                embed.set_footer(text = 'Success!', icon_url = 'https://cdn.discordapp.com/attachments/620077247516377100/623690064525787146/pug.jpg')

    if len(item[frame]) > 1:
        for value in range(len(item[frame])):
            build = item[frame][value].split('/')
            build_file = build[-1]
            build_name = build_file[:-4]
            embed.set_author(name = build_name.upper())
            embed.set_image(url = item[frame][value])
            embed.set_thumbnail(url = item['thumbnail'])
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
