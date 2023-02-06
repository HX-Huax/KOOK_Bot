
from khl import *
from khl.card import CardMessage, Card, Module, Element, Types, Struct
import json
from datetime import datetime, timedelta
from random import randint
with open('./config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

bot = Bot(token=config['token'])
#roll点
@bot.command()
async def roll(msg: Message, t_min: int, t_max: int, n: int = 1):
    result = [randint(t_min, t_max) for i in range(n)]
    await msg.reply(f'你掷出了: {result}')
#bot_info
@bot.command(name = 'info')
async def info(msg:Message):
    # c=Card(INFO)
    # cm=khl.card.CardMessage(c)
    c = Card(Module.Header('提醒摸鱼小助手') , color='#e3b4b8')
    c.append(Module.Divider())
    c.append(Module.Context('var 0.0.1'))
    cm = CardMessage(c)  # Card can not be sent directly, need to wrapped with a CardMessage
    await msg.reply(cm)
# find the game you want to add in this list
@bot.command(name='list')
async def list_game(_: Message):
    ret = await bot.client.fetch_game_list()
    for g in ret:
        print(f"game_name: {g.name} -- game_id: {g.id}")
#set bot gaming status by random
@bot.command()
async def rgame(msg:Message):
    ret = await bot.client.fetch_game_list()
    size = len(ret)
    ga=randint(0, size)
    await bot.client.update_playing_game(ret[ga].id)
    await msg.reply(f'gaming!, {ret[ga].name}', is_temp=True)
# use game_id to set bot gaming status
@bot.command()
async def gaming(msg: Message, game_id: int):
    # game_id : int
    await bot.client.update_playing_game(game_id)
    await msg.reply('gaming!', is_temp=True)
# set bot music status
@bot.command()
async def music(msg: Message, music: str, singer: str):
    # music name : str
    # singer name : str
    # music_software : Enum ['cloudmusic'、'qqmusic'、'kugou'], 'cloudmusic' in default
    await bot.client.update_listening_music(music, singer, "cloudmusic")
    await msg.reply('listening to music!', is_temp=True)
# delete bot status
@bot.command()
async def stop(msg: Message, d: int):
    if d == 1:
        await bot.client.stop_playing_game()
    elif d == 2:
        await bot.client.stop_listening_music()
    await msg.reply('stop')

#fixing
# @bot.on_event(EventTypes.JOINED_CHANNEL)
# async def wellcome(b: Bot ,event: Event):
#     print(event.body)
#     channel=await b.client.fetch_public_channel(event.body['channel_id'])
#     await b.client.send('Wellcome')

bot.run()