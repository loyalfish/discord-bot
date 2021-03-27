import conf
import discord


client = discord.Client()
@client.event
async def on_message(message):
    msg = None
    if message.author == client.user:
        return

    if message.author.bot:
        return
    
    if message.channel.id == 825347231271354391:
        msg = f'Your message is {message.content}'
        if message.content == "/hello":
            msg = f'Hello, {message.author.name}!'
        elif message.content.find('/repeat') != -1:
            msg = message.content.split('/repeat')[1]
        elif message.content == "/about_me":
            if message.author.nick != None:
                msg = f'Вы - {message.author.name}, ваш ник - {message.author.nick}'
            else:
                msg = f'Вы - {message.author.name}'
        if msg != None:
            await message.channel.send(msg)
client.run(conf.bot_token)