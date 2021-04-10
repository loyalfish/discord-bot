import discord.ext
from discord.utils import get
from random import randint
import time
import json
import os
import asyncio
import functools
import itertools
import math
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl
from discord.ext import commands

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands

from discord.ext import commands

# Read the Data files and store them in a variable
TokenFile = open("./data/Token.txt", "r") # Make sure to paste the token in the txt file
TOKEN = TokenFile.read()


OWNERID = 505750675758514197

# Define "bot"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", case_insensitive=True, intents=intents)
bot.remove_command('help')

# Let us Know when the bot is ready and has started
@bot.event
async def on_ready():
    print("Bot is ready")


@bot.event 
async def on_command_error(ctx, error):
    embed = discord.Embed(
    title='',
    color=discord.Color.red())
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.MissingPermissions):
        embed.add_field(name=f'Invalid Permissions', value=f'You dont have {error.missing_perms} permissions.')
        await ctx.send(embed=embed)
    else:
        embed.add_field(name = f':x: Terminal Error', value = f"```{error}```")
        await ctx.send(embed = embed)
        raise error


@bot.event
async def on_message(message):
    with open('lvl.json', 'r') as f:
        global users
        users = json.load(f)

    async def ziro_exp(users, user):
        if users[user]['exp'] == 1000:
            users[user]['exp'] = 0
            users[user]['lvl'] += 1

    async def update_data(users, user):
        if not user in users:
            users[user] = {}
            users[user]['exp'] = 0
            users[user]['lvl'] = 1

    async def add_exp(users, user, exp):
        if message.author.bot:
            pass
        else:
            if expp == 0:
                users[user]['exp'] = 1
            elif expp > 0:
                users[user]['exp'] += exp


    async def add_lvl(users, user):
        global expp
        lvl = users[user]['lvl']
        expp = users[user]['exp']
        if expp == 999:
            expp = 1
            await message.channel.send(f'{message.author.mention} повысил свой уровень!')
            users[user]['exp'] = 1

    await update_data(users, str(message.author.id))
    await add_lvl(users, str(message.author.id))
    await add_exp(users, str(message.author.id), 1)
    await ziro_exp(users, str(message.author.id))
    with open('lvl.json', 'w') as f:
        json.dump(users, f)
    await bot.process_commands(message)


@bot.command(name='help', aliases=['commands', '', 'command'])
async def help(ctx):
    msg = f"**`#repeat (текст)`** - повторить текст\n" \
          f"**`#loop *(текст) (кол-во раз)`** - повторить текст некоторое кол-во раз\n" \
          f"**`#about @id`** - информация о человеке, @id которого указано. Если @id человека не указано, выведется информация о человеке,написавшем команду\n" \
          f"**`#kick @id (причина)`** - кикнуть участника, @id которого указано. Также можно объявить причину, по которой происходит кик\n" \
          f"**`#ban @id (причина)`** - забанить участника, @id которого указано. Также можно объявить причину, по которой происходит бан\n" \
          f"**`#mute @id (причина)`** - замутить участника, @id которого указано. Также можно объявить причину, по которой происходит мут (здесь обязательно стоит создать роль на сервере 'muted', которая отбирает полное право на сообщение у участника)\n"\
          f"**`#code/#decode (текст)`** - зашифровать/расшифровать текст, имеется русский и английский язык, а также основные знаки пунктуации.\n" \
          f"**`#ruletka`** - игра 'Русская рулетка': если повезет, то пули не окажется в ячейке, а если нет, то ты умрешь и будешь кикнут с сервера!\n" \
          f"**`#bump`** - ударить бота\n" \
          f"**`#play/sing (url/слово/фраза)`** - сыграть аудио дорожку из видео по url или по названию\n" \
          f"**`#join/connect`** - подсоединиться к voice-каналу, в котором находится написавший\n"\
          f"**`#pause`** - приостановить аудиодорожку\n"\
          f"**`#resume`** - возобновить аудиодорожку\n"\
          f"**`#leave/stop`** - выйти из voice-канала\n"\
          f"**`#queue/playlist/q`** - показать плейслист из аудиодорожек\n"\
          f"**`#skip`** - включить следующую аудиодорожку\n"\
          f"**`#now_playing`** - показать ту аудидорожку, которая сейчас играет\n"\
          f"**`#volume 1-100`** - установить громкость от 1 до 100\n"
    emb = discord.Embed(title=f"Памятка по командам:\n", description=msg, colour=discord.Color.red())
    await ctx.send(embed=emb)


@bot.command()
async def repeat(ctx):
    if ctx.message.content == "#repeat":
        await ctx.send(f'Мне нечего повторять :/')
    else:
        await ctx.send(f'{ctx.message.content[7:]}')


@bot.command()
async def ruletka(ctx):
    shoot = randint(1, 6)
    bully = randint(1, 6)
    for member in ctx.guild.members:
        if member.id == bot.user.id:
            bot_role = member.top_role
    if ctx.author.top_role >= bot_role:
        await ctx.send(f"Ты не можешь учавствовать в рулетке, так как ты выше меня по роли, я не могу кикнуть тебя!")
    else:
        if shoot == bully:
            await ctx.author.kick(reason="Получил(a) пулю в бошку!")
            await ctx.author.send(f'Вы были кикнуты с сервера "{ctx.message.guild.name}", по причине проигрыша в русской рулетке')
            await ctx.send(f"{ctx.author.mention} умер и был кикнут, земля ему пухом! :worried:")
        else:
            await ctx.send(f"Везунчик! Но лучше положи револьвер на место, а то мало ли! :wink:")


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    for member in ctx.guild.members:
        if member.id == bot.user.id:
            bot_role = member.top_role
    if member.top_role >= bot_role:
        await ctx.send("Я не могу кикнуть этого пользователя, так как он равен или выше меня по роли!")
    else:
        if reason == None:
            await ctx.send(f'{member.mention} был кикнут с сервера!')
            await member.send(f'Вы были кикнуты с сервера "{ctx.message.guild.name}"')
        else:
            await ctx.send(f'{member.mention} был кикнут с сервера, по причине: {reason}!')
            await member.send(f'Вы были кикнуты с сервера "{ctx.message.guild.name}", по причине: {reason}')
        await member.kick(reason=reason)


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    for member in ctx.guild.members:
        if member.id == bot.user.id:
            bot_role = member.top_role
    if member.top_role >= bot_role:
        await ctx.send("Я не могу забанить этого пользователя, так как он равен или выше меня по роли!")
    else:
        await member.ban(reason=reason)
        if reason == None:
            await ctx.send(f'{member.mention} был забанен на сервере!')
            await member.send(f'Вы были забанены на сервере "{ctx.message.guild.name}"')
        else:
            await ctx.send(f'{member.mention} был забанен на сервере, по причине: {reason}!')
            await member.send(f'Вы были забанены на сервере "{ctx.message.guild.name}", по причине: {reason}')


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    mute_role = discord.utils.get(ctx.message.guild.roles, name='muted')
    if reason == None:
        await ctx.send(f'{member.mention} был замучен на сервере!')
    else:
        await ctx.send(f'{member.mention} был замучен на сервере, по причине: {reason}!')
    await member.add_roles(mute_role)


@bot.command()
async def about(ctx, member: discord.Member = None, guild: discord.Guild = None):
    if member == None:
            if ctx.message.author.activity == None:
                status = "Нету"
            else:
                status = ctx.message.author.activity
            emb = discord.Embed(title="Информация о пользователе", color=ctx.message.author.color)
            emb.add_field(name="Отображаемое имя:", value=ctx.message.author.display_name, inline=False)
            emb.add_field(name="Имя аккаунта:", value=ctx.message.author, inline=False)
            emb.add_field(name="id пользователя:", value=ctx.message.author.id, inline=False)
            t = ctx.message.author.status
            if t == discord.Status.online:
                d = " В сети"

            t = ctx.message.author.status
            if t == discord.Status.offline:
                d = "⚪ Не в сети"

            t = ctx.message.author.status
            if t == discord.Status.idle:
                d = " Не активен"

            t = ctx.message.author.status
            if t == discord.Status.dnd:
                d = " Не беспокоить"

            emb.add_field(name="Активность:", value=d, inline=False)
            emb.add_field(name="Статус:", value=status, inline=False)
            emb.add_field(name="Роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
            emb.add_field(name="Акаунт был создан:", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
            emb.set_thumbnail(url=ctx.message.author.avatar_url)
            if str(ctx.message.author.id) in users:
                emb.add_field(name="XP:", value=f"{users[str(ctx.message.author.id)]['exp']}/1000", inline=False)
                emb.add_field(name="LVL:", value=f"{users[str(ctx.message.author.id)]['lvl']} уровень", inline=False)
            else:
                emb.add_field(name="XP:", value=f"0/1000", inline=False)
                emb.add_field(name="LVL:", value=f"1 уровень", inline=False)
            await ctx.send(embed=emb)
    else:
        if member.bot == True:
            await ctx.send("Я не могу иметь в себе информацию бота :/")
        else:
            if member.activity == None:
                status = "Нету"
            else:
                status = member.activity
            emb = discord.Embed(title="Информация о пользователе", color=member.color)
            emb.add_field(name="Отображаемое имя:", value=member.display_name, inline=False)
            emb.add_field(name="Имя аккаунта:", value=member, inline=False)
            emb.add_field(name="id пользователя:", value=member.id, inline=False)
            t = member.status
            if t == discord.Status.online:
                d = " В сети"

            t = member.status
            if t == discord.Status.offline:
                d = "⚪ Не в сети"

            t = member.status
            if t == discord.Status.idle:
                d = " Не активен"

            t = member.status
            if t == discord.Status.dnd:
                d = " Не беспокоить"
            emb.add_field(name="Активность:", value=d,inline=False)
            emb.add_field(name="Статус:", value=status, inline=False)
            emb.add_field(name="Роль на сервере:", value=f"{member.top_role.mention}",inline=False)
            emb.add_field(name="Акаунт был создан:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p"),inline=False)
            emb.set_thumbnail(url=member.avatar_url)
            if str(member.id) in users:
                emb.add_field(name="XP:", value=f"{users[str(member.id)]['exp']}/1000", inline=False)
                emb.add_field(name="LVL:", value=f"{users[str(member.id)]['lvl']} уровень", inline=False)
            else:
                emb.add_field(name="XP:", value=f"0/1000", inline=False)
                emb.add_field(name="LVL:", value=f"1 уровень", inline=False)
            await ctx.send(embed=emb)


@bot.command()
async def loop(ctx):
    msg = ""
    a = ctx.message.content.split()[-1]
    if a.isdigit() == True:
        print(int(ctx.message.content.split()[-1]))
        if int(ctx.message.content.split()[-1]) <= 20:
            for i in range(int(ctx.message.content.split()[-1])):
                msg += f"{ctx.message.content[6:-2]}\n"
        elif int(ctx.message.content.split()[-1]) >= 20:
            msg = "Ограничение - 20 символов"
        elif int(ctx.message.content.split()[-1]) != 0:
            for i in range(int(ctx.message.content.split()[-1])):
                msg += f"{ctx.message.content[6:-2]}\n"
        await ctx.send(msg)
    else:
        await ctx.send(f"{ctx.message.content[6:]}\n")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Привет, {ctx.author.name}")


@bot.command()
async def code(ctx):
    m = ""
    for char in ctx.message.content[6:].lower():
        if char == "a":
            m += "881"
        if char == "b":
            m += "312"
        if char == "c":
            m += "841"
        if char == "d":
            m += "541"
        if char == "e":
            m += "632"
        if char == "f":
            m += "463"
        if char == "g":
            m += "346"
        if char == "h":
            m += "436"
        if char == "j":
            m += "768"
        if char == "i":
            m += "111"
        if char == "k":
            m += "123"
        if char == "l":
            m += "985"
        if char == "m":
            m += "234"
        if char == "n":
            m += "652"
        if char == "o":
            m += "335"
        if char == "p":
            m += "665"
        if char == "q":
            m += "222"
        if char == "r":
            m += "435"
        if char == "s":
            m += "153"
        if char == "t":
            m += "980"
        if char == "u":
            m += "901"
        if char == "v":
            m += "990"
        if char == "w":
            m += "001"
        if char == "x":
            m += "219"
        if char == "y":
            m += "128"
        if char == "z":
            m += "098"
        if char == " ":
            m += "090"
        if char == ",":
            m += "494"
        if char == ".":
            m += "199"
        if char == ":":
            m += "393"
        if char == "/":
            m += "666"
        if char == "'":
            m += "228"
        if char == '"':
            m += "672"
        if char == '|':
            m += "563"
        if char == '(':
            m += "565"
        if char == ')':
            m += "571"
        if char == '-':
            m += "972"
        if char == '=':
            m += "867"
        if char == "а":
            m += "010"
        if char == "б":
            m += "020"
        if char == "в":
            m += "088"
        if char == "г":
            m += "019"
        if char == "д":
            m += "880"
        if char == "е":
            m += "771"
        if char == "ё":
            m += "810"
        if char == "ж":
            m += "911"
        if char == "з":
            m += "212"
        if char == "и":
            m += "653"
        if char == "й":
            m += "325"
        if char == "к":
            m += "050"
        if char == "л":
            m += "070"
        if char == "м":
            m += "007"
        if char == "н":
            m += "112"
        if char == "о":
            m += "856"
        if char == "п":
            m += "223"
        if char == "р":
            m += "900"
        if char == "с":
            m += "800"
        if char == "т":
            m += "100"
        if char == "у":
            m += "700"
        if char == "ф":
            m += "500"
        if char == "х":
            m += "200"
        if char == "ц":
            m += "300"
        if char == "ч":
            m += "400"
        if char == "ш":
            m += "009"
        if char == "щ":
            m += "004"
        if char == "ъ":
            m += "812"
        if char == "ы":
            m += "341"
        if char == "ь":
            m += "987"
        if char == "э":
            m += "413"
        if char == "ю":
            m += "236"
        if char == "я":
            m += "109"
    if m == "":
        await ctx.send("А где :/")
    else:
        emb = discord.Embed(title="Зашифрованное сообщение:", description=m, color=discord.Color.red())
        await ctx.send(embed=emb)


@bot.command()
async def decode(ctx):
    m = ""
    s = ([ctx.message.content[8:][i:i + 3] for i in range(0, len(ctx.message.content), 3)])
    print(s)
    for i in s:
        if i == "881":
            m += "a"
        if i == "312":
            m += "b"
        if i == "841":
            m += "c"
        if i == "541":
            m += "d"
        if i == "632":
            m += "e"
        if i == "463":
            m += "f"
        if i == "346":
            m += "g"
        if i == "436":
            m += "h"
        if i == "768":
            m += "j"
        if i == "111":
            m += "i"
        if i == "123":
            m += "k"
        if i == "985":
            m += "l"
        if i == "234":
            m += "m"
        if i == "652":
            m += "n"
        if i == "335":
            m += "o"
        if i == "665":
            m += "p"
        if i == "222":
            m += "q"
        if i == "435":
            m += "r"
        if i == "153":
            m += "s"
        if i == "980":
            m += "t"
        if i == "901":
            m += "u"
        if i == "990":
            m += "v"
        if i == "001":
            m += "w"
        if i == "219":
            m += "x"
        if i == "128":
            m += "y"
        if i == "098":
            m += "z"
        if i == "090":
            m += " "
        if i == "494":
            m += ","
        if i == "199":
            m += "."
        if i == "393":
            m += ":"
        if i == "666":
            m += "/"
        if i == "228":
            m += "'"
        if i == '672':
            m += '"'
        if i == '563':
            m += "|"
        if i == '565':
            m += "("
        if i == '571':
            m += ")"
        if i == '972':
            m += "-"
        if i == '867':
            m += "="
        if i == "010":
            m += "а"
        if i == "020":
            m += "б"
        if i == "088":
            m += "в"
        if i == "019":
            m += "г"
        if i == "880":
            m += "д"
        if i == "771":
            m += "е"
        if i == "810":
            m += "ё"
        if i == "911":
            m += "ж"
        if i == "212":
            m += "з"
        if i == "653":
            m += "и"
        if i == "325":
            m += "й"
        if i == "050":
            m += "к"
        if i == "070":
            m += "л"
        if i == "007":
            m += "м"
        if i == "112":
            m += "н"
        if i == "856":
            m += "о"
        if i == "223":
            m += "п"
        if i == "900":
            m += "р"
        if i == "800":
            m += "с"
        if i == "100":
            m += "т"
        if i == "700":
            m += "у"
        if i == "500":
            m += "ф"
        if i == "200":
            m += "х"
        if i == "300":
            m += "ц"
        if i == "400":
            m += "ч"
        if i == "009":
            m += "ш"
        if i == "004":
            m += "щ"
        if i == "812":
            m += "ъ"
        if i == "341":
            m += "ы"
        if i == "987":
            m += "ь"
        if i == "413":
            m += "э"
        if i == "236":
            m += "ю"
        if i == "109":
            m += "я"
    if m == "":
        await ctx.send("А где :/")
    else:
        emb = discord.Embed(title="Расшифрованное сообщение:", description=m, color=discord.Color.red())
        await ctx.send(embed=emb)


@bot.command()
async def load(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Enabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")


@bot.command()
async def unload(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.unload_extension(f'Cogs.{extension}')
        await ctx.send(f"Disabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")


@bot.command(name="reload")
async def reload_(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.reload_extension(f'Cogs.{extension}')
        await ctx.send(f"Reloaded the Cog!") 
    else:
        await ctx.send(f"You are not cool enough to use this command")


@bot.command()
async def get_channels(ctx):
    n = 1
    msgg = ""
    for i in ctx.guild.channels:
        msgg += f"**`{n}`**: **{i}**  -  *{i.id}*\n"
        n += 1
    emb = discord.Embed(title=f"Каналы этого сервера:\n", description=msgg, colour=discord.Color.red())
    await ctx.send(embed=emb)


@bot.command()
async def get_members(ctx):
    n = 1
    msgg = ""
    for i in ctx.guild.members:
        msgg += f"**`{n}`**: **{i}**  -  *{i.id}*\n"
        n += 1
    emb = discord.Embed(title=f"Участники этого сервера:\n", description=msgg, colour=discord.Color.red())
    await ctx.send(embed=emb)


@bot.command()
async def bump(ctx, member: discord.Member = None):
    if member == None:
        await ctx.send(f"{ctx.message.author.mention} жёстко вдарил по {ctx.message.author.mention} :punch: :head_bandage: ")
    else:
        await ctx.send(f"{ctx.message.author.mention} жёстко вдарил по {member.mention} :punch: :head_bandage: ")


@bot.command()
async def fuck(ctx, member: discord.Member = None):
    if member == None:
        await ctx.send(f"{ctx.message.author.mention} дико трахнул {ctx.message.author.mention} :hot_face: :underage: ")
    else:
        await ctx.send(f"{ctx.message.author.mention} дико трахнул {member.mention} :hot_face: :underage: ")


@bot.command()
async def piss(ctx, member: discord.Member = None):
    if member == None:
        await ctx.send(f"{ctx.message.author.mention} дико трахнул {ctx.message.author.mention} :hot_face: :underage: ")
    else:
        await ctx.send(f"{ctx.message.author.mention} обоссал {member.mention} :banana: :tropical_drink:  ")
    await ctx.send()


@bot.command()
async def rape(ctx, member: discord.Member = None):
    await ctx.send(f"{ctx.message.author.mention} обоссал {member.mention} :banana: :tropical_drink:  ")


for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'Cogs.{filename[:-3]}')
        except Exception:
            raise Exception
        

bot.run(str(TOKEN))