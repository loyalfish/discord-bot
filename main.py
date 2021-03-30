import conf
import discord.ext
from discord.ext import commands
from discord.utils import get
from random import randint
import time
import json

intents = discord.Intents.all()
client = commands.Bot(command_prefix='#', intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    print('бот включен')


@client.event
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

    await add_lvl(users, str(message.author.id))
    await add_exp(users, str(message.author.id), 1)
    await ziro_exp(users, str(message.author.id))
    await update_data(users, str(message.author.id))
    with open('lvl.json', 'w') as f:
        json.dump(users, f)
    await client.process_commands(message)



@client.command()
async def help(ctx):
    msg = f"**#hello** - привествие\n" \
          f"**#repeat (текст)** - повторить текст\n" \
          f"**#loop (текст) (кол-во раз)** - повторить текст некоторое кол-во раз\n" \
          f"**#about_me** - информация о написавшем команду\n" \
          f"**#about @id** - информация о человеке, id которого указано\n" \
          f"**#ruletka** - игра 'Русская рулетка': если повезет, то пули не окажется в ячейке, а если нет, то ты умрешь и будешь кикнут с сервера!\n"
    emb = discord.Embed(title=f"Памятка по командам:\n", description=msg, colour=discord.Color.red())
    await ctx.send(embed=emb)


@client.command()
async def repeat(ctx):
    if ctx.message.content == "#repeat":
        await ctx.send(f'Мне нечего повторять :/')
    else:
        await ctx.send(f'{ctx.message.content[7:]}')


@client.command()
async def loop(ctx):
    print(int(ctx.message.content.split()[-1]))
    if int(ctx.message.content.split()[-1]) <= 14:
        for i in range(int(ctx.message.content.split()[-1])):
            await ctx.send(ctx.message.content[5:-2])
    elif int(ctx.message.content.split()[-1]) >= 14:
        await ctx.send("Ограничение - 14 символов")
    elif int(ctx.message.content.split()[-1]) != 0:
        for i in range(int(ctx.message.content.split()[-1])):
            await ctx.send(ctx.message.content[5:-2])


@client.command()
async def hello(ctx):
    await ctx.send(f"Привет, {ctx.author.name}")


@client.command()
async def about_me(ctx):
    if ctx.author.nick != None:
        msg = f"**Имя** - {client.get_user(ctx.author.id)}\n" \
              f"**id** - {ctx.author.id}\n" \
              f"**exp** - {users[str(ctx.message.author.id)]['exp']}/1000\n" \
              f"**lvl** - {users[str(ctx.message.author.id)]['lvl']}\n" \
              f"**Ник** - {ctx.author.nick}\n"
    else:
        msg = f"**Имя** - {client.get_user(ctx.author.id)}\n" \
              f"**id** - {ctx.author.id}\n" \
              f"**exp** - {users[str(ctx.message.author.id)]['exp']}/1000\n" \
              f"**lvl** - {users[str(ctx.message.author.id)]['lvl']}\n"

    emb = discord.Embed(title=f"Информация о {ctx.author.name}\n", description=msg, colour=discord.Color.red())
    emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


@client.command()
async def about(ctx, member: discord.Member):
    if member.nick != None:
        msg = f"**Имя** - {client.get_user(member.id)}\n" \
              f"**id** - {member.id}\n" \
              f"**exp** - {users[str(member.id)]['exp']}/100\n" \
              f"**Ник** - {member.nick}\n"
    else:
        msg = f"**Имя** - {client.get_user(member.id)}\n" \
              f"**id** - {member.id}\n" \
              f"**exp** - {users[str(member.id)]['exp']}/100"

    emb = discord.Embed(title=f"Информация о {member.name}\n", description=msg, colour=discord.Color.red())
    emb.set_footer(text=member.name, icon_url=member.avatar_url)
    await ctx.send(embed=emb)


@client.command()
async def ruletka(ctx):
    shoot = randint(1, 6)
    bully = randint(1, 6)
    for member in ctx.guild.members:
        if member.id == client.user.id:
            bot_role = member.top_role
    if ctx.author.top_role >= bot_role:
        await ctx.send(f"Ты не можешь учавствовать в рулетке, так как ты выше меня по роли, я не могу кикнуть тебя!")
    else:
        if shoot == bully:
            await ctx.author.kick(reason="Получил(a) пулю в бошку!")
            await ctx.send(f"{ctx.author.name} умер и был кикнут, земля ему пухом! :worried:")
        else:
            await ctx.send(f"Везунчик! Но лучше положи револьвер на место, а то мало ли! :wink:")


client.run(conf.bot_token)