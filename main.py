import discord
from discord.ext import commands
import json

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')

@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(status = discord.Status.online, activity = discord.Game('.help'))

#Core frame, modset
@client.command()
async def frame(ctx, *, frame):
    frame = frame.lower()

    with open('warframes.json', 'r') as f:
        warframes = json.load(f)

    for item in warframes:
        for key in item:
            if key == frame and len(item[frame]) == 1:
                build = item[frame][0].split('/')
                build_file = build[-1]
                build_name = build_file[:-4]
                build_name = build_name.replace('_', ' ')

                embed = discord.Embed(color = discord.Color.gold())
                embed.set_author(name = build_name.upper(), icon_url = item['thumbnail'])
                embed.set_image(url = item[frame][0])
                embed.set_thumbnail(url = item['thumbnail'])
                embed.add_field(name = item['author'][0], value = item['link'][0])
                embed.set_footer(text ='Suggestions at warframeclixbot@gmail.com!', icon_url = 'https://cdn.discordapp.com/attachments/620077247516377100/623690064525787146/pug.jpg')
                await ctx.send(embed = embed)

            elif key == frame and len(item[frame]) > 1:
                for value in range(len(item[frame])):
                    build = item[frame][value].split('/')
                    build_file = build[-1]
                    build_name = build_file[:-4]
                    build_name = build_name.replace('_', ' ')

                    embed = discord.Embed(color = discord.Color.gold())
                    embed.set_author(name = build_name.upper(), icon_url = item['thumbnail'])
                    embed.set_image(url = item[frame][value])
                    embed.add_field(name = item['author'][value], value = item['link'][value])
                    embed.set_thumbnail(url = item['thumbnail'])
                    embed.set_footer(text = 'Suggestions at warframeclixbot@gmail.com!', icon_url = 'https://cdn.discordapp.com/attachments/620077247516377100/623690064525787146/pug.jpg')
                    await ctx.send(embed = embed)

@client.command()
async def modset(ctx, *, set_name):
    set_name = set_name.lower()

    with open ('modset.json', 'r') as f:
        modsets = json.load(f)

    for item in modsets:
        for set in item:
            if set == set_name:
                build = item[set_name].split('/')
                build_file = build[-1]
                build_name = build_file[:-4]
                build_name = build_name.replace('_', ' ')

                embed = discord.Embed(color = discord.Color.greyple())
                embed.set_author(name = build_name.upper(), icon_url = 'https://cdn.discordapp.com/attachments/620077247516377100/623690064525787146/pug.jpg')
                embed.set_image(url = item[set_name])
                embed.add_field(name = 'Set Bonus:', value = item['bonus'])
                embed.set_footer(text = 'Suggestions at warframeclixbot@gmail.com!', icon_url = 'https://cdn.discordapp.com/attachments/620077247516377100/623690064525787146/pug.jpg')
                await ctx.send(embed = embed)

@frame.error
async def frame_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title = ':x: Unsuccessful!', description = 'Please specify a warframe.', color = discord.Color.blurple())
        await ctx.send(embed = embed)

@modset.error
async def modset_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title = ':x: Unsuccessful!', description = 'Please specify a modset.', color = discord.Color.blurple())
        await ctx.send(embed = embed)

@client.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(color = discord.Color.magenta())
    embed.set_author(name = 'Help Commands!\nWeapon commands coming soon!')
    embed.add_field(name = '.frame <warframe>', value = 'Shows warframe builds', inline = False)
    embed.add_field(name = '.help', value = 'Shows this command', inline = False)
    await ctx.send(embed = embed)

#PREFIX COMMANDS
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
    title = ':white_check_mark: Successful!',
    description = f'Your prefix has been changed to `{prefix}`',
    color = discord.Color.magenta()
    )

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

    await ctx.send(embed = embed)

client.run('TOKEN')
