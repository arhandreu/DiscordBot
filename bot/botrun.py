import discord
import os, sqlite3, string, json
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready(): # Действия при включении бота
    print('Я подключился!!!')

    global base, cur
    base = sqlite3.connect('Bot.db')
    cur = base.cursor()
    if base:
        print('DB connect!')

@bot.event
async def on_member_join(member):
    await member.send('Привет! Я Ботя, просмотр доступных команд !инфо') # личное сообщение
    #for chan in bot.get_guild(member.guild.id).channels: # сообщение в канал сервера(guild)
    #    if chan.name == 'general':
    #        await chan.send(f'{member}, добро пожаловать, проверь личку.')


@bot.event
async def on_member_remove(member):
    for chan in bot.get_guild(member.guild.id).channels:
        if chan.name == 'general':
            await chan.send(f'{member}, покинул сервер')


@bot.event
async def on_message(message): # Действия над сообщениями
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) 
        for i in message.content.split(' ')}.intersection(set(json.load(open(r'..\to_json\cenzor.json')))) != set():
            await message.channel.send(f'{message.author.mention}, Не использовать запрещенку')
            # await message.author.send('eeeee')
            await message.delete()

            name = message.guild.name

            base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(name))
            base.commit()

            warning = cur.execute('SELECT * FROM {} WHERE userid == ?'.format(name),(message.author.id,)).fetchone()
            
            if warning is None:
                cur.execute('INSERT INTO {} VALUES(?, ?)'.format(name),(message.author.id, 1))
                base.commit()
                await message.channel.send(f'{message.author.mention}, 1 предупреждение за 3 - бан!')

            elif warning[1] == 1:
                cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name),(2, message.author.id))
                base.commit()
                await message.channel.send(f'{message.author.mention}, 2-е предупреждение, еще одно и бан!')

            elif warning[2] == 2:
                cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name),(3, message.author.id))    
                base.commit()
                await message.channel.send(f'{message.author.mention}, забанен в чате!')
                await message.author.ban(reason='Мат!')
    
    
    
    await bot.process_commands(message) # для передачи на проверку команда ли это 

@bot.command()
async def статус(ctx):
    base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(ctx.message.guild.name))
    base.commit()
    warning = cur.execute('SELECT * FROM {} WHERE userid== ?'.format(ctx.message.guild.name),
    (ctx.message.author.id,)).fetchone()
    if warning is None:
        await ctx.send(f'{ctx.message.author.mention}, у Вас нет предупреждений')
    else:
        await ctx.send(f'{ctx.message.author.mention}, у Вас {warning[1]} предупреждений')

@bot.command()
async def test(ctx):
    await ctx.send('Я онлайн!')
    
@bot.command()   
async def инфо(ctx, arg=None):     # arg1, arg2 - несколько переменных // *, arg - предложение
    author = ctx.message.author
    if arg is None:
        await ctx.send(f'{author.mention}\nВведите:\n!инфо общая\n!инфо команды')
    elif arg == 'общая':
        await ctx.send(f'{author.mention}\nЯ Ботя слежу за порядком в чате')
    elif arg == 'команды':
        await ctx.send(f'{author.mention}\n!test - Доступен ли бот\n!статус - Мои штрафы')
    else:
        await ctx.send(f'{author.mention}\nНезнакомая команда((')   
      


bot.run(os.getenv('TOKEN'))
