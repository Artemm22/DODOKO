# -*- coding: utf-8 -*-
import time

import discord
from discord.ext import commands
from discord.utils import get
import sys
from discord_components import DiscordComponents, Button, ButtonStyle
import datetime
import humanfriendly

import asyncio

import json

import requests
from PIL import Image, ImageFont, ImageDraw
import io
import random

from lop import token

bot = commands.Bot(command_prefix='q', intents=discord.Intents().all())

bot.remove_command('help')

@bot.command()
async def help(ctx):
    await ctx.message.add_reaction('✅')
    emb = discord.Embed(title='Привет, я бот DODOKO!', colour=discord.Colour.random())
    emb.add_field(name='help'.format(bot), value='Показывает это окно.')
    emb.add_field(name='bye'.format(bot), value='Выключает меня.')
    emb.add_field(name='send_hi'.format(bot), value='Я пришлю кому укажите привет.')
    emb.add_field(name='clear'.format(bot), value='Удаляю 10 сообщениий включая команду.')
    emb.add_field(name='hello'.format(bot), value='Я скажу вам привет!')
    emb.add_field(name="card_user(я, карта)".format(bot), value='Отправляю вашу карточку discord.')
    emb.add_field(name="tt".format(bot), value='Ссылки для поддержки автора!')
    emb.add_field(name="mute @кого-то ^m *причина*".format(bot), value='Мут кому-то. !Работает только у администратаров!')
    emb.add_field(name="unmute @кого-то *причина*".format(bot), value='Размут кому-то. !Работает только у администратаров!')
    await ctx.send(embed = emb )

@bot.event
async def on_ready():
    print('Bot online!')
    DiscordComponents(bot)
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('zxc girl'))
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if str(channel) == "〰▪test🛠":
                await channel.send('Я тут!! :heart:  qhelp чтобы узнать команды.')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass
    else:
        with open('rmoji.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(bot.get_guild(payload.guild_id).roles, id=x['role_id'])
                    await payload.member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.member.bot:
        pass
    else:
        with open('rmoji.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(bot.get_guild(payload.guild_id).roles, id=x['role_id'])
                    await payload.member.add_roles(role)

@bot.command(pass_context=True)
async def clear(ctx, amount=10):
    await ctx.message.add_reaction('✅')
    await ctx.channel.purge(limit=amount)

@bot.command(pass_context=True)
async def clearall(ctx):
    await ctx.message.add_reaction('✅')
    await ctx.channel.purge()


@bot.command()
async def bye(ctx):
    await ctx.message.add_reaction('✅')
    await ctx.send('Я побежала! Пока!')
    sys.exit(0)
    pass

@bot.command()
async def rrole(ctx, emoji, role: discord.Role, *, message):
    await ctx.message.add_reaction('✅')
    emb = discord.Embed(title=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)
    with open('rmoji.json') as json_file:
        data = json.load(json_file)
        new_react_role = {
            'role_name':role.name,
            'role_id':role.id,
            'emoji':emoji,
            'message_id':msg.id
        }
        data.append(new_react_role)
    with open('rmoji.json', 'w') as j:
        json.dump(data, j, indent=4)


@bot.command()
async def send_hi(ctx, member: discord.Member):
    await ctx.message.add_reaction('✅')
    await member.send(f'{member.mention}, вам привет от {ctx.author.mention}! :heart:')

@bot.command()
async def hello(ctx):
    await ctx.message.add_reaction('✅')
    author = ctx.message.author
    await ctx.send(f'Hello {author.mention}!')

@bot.command()
async def ping(ctx):
    await ctx.message.add_reaction('✅')
    await ctx.channel.send(f'Pong {round(bot.latency*1000)}ms')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member=None, time=None, *, reason=None):
    await ctx.message.add_reaction('✅')
    time=humanfriendly.parse_timespan(time)
    await member.timeout(until=discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)
    emb = discord.Embed(title="Мут на {}sec".format(time), colour=discord.Colour.random())
    await ctx.channel.purge(limit=1)
    emb.set_author(name=member.name, icon_url=member.avatar)
    emb.add_field(name="Замуюченый пользователь: {}".format(member.name), value="Причина: {}".format(reason))
    await ctx.send(embed=emb)

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member=None, *, reason=None):
    await ctx.message.add_reaction('✅')
    await member.timeout(until=None, reason=reason)
    emb = discord.Embed(title="Размут", colour=discord.Colour.random())
    await ctx.channel.purge(limit=1)
    emb.set_author(name=member.name, icon_url=member.avatar)
    emb.add_field(name="Размученый пользователь: {}".format(member.name), value="Причина: {}".format(reason))
    await ctx.send(embed = emb)

@bot.command()
async def join(ctx):
    await ctx.message.add_reaction('✅')
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Я у вас! ({channel})')

@bot.command()
async def leave(ctx):
    await ctx.message.add_reaction('✅')
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
    await ctx.send(f'Всё! Я побежала! ({channel})')

@bot.command(aliases = ['я', 'карта'])
async def card_user(ctx):
    await ctx.message.add_reaction('✅')
    img = Image.open('003.png')
    url = str(ctx.author.avatar)
    response = requests.get(url, stream=True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)
    img.paste(response, (15, 15, 115, 115))
    idraw = ImageDraw.Draw(img)
    name = ctx.author.name
    tag = ctx.author.discriminator
    headline = ImageFont.truetype('comic.ttf', size=20)
    undertext = ImageFont.truetype('comic.ttf', size=12)
    idraw.text((145, 15), f'{name}#{tag}', font=headline)
    idraw.text((145, 50), f'ID: {ctx.author.id}', font=undertext)
    img.save('user_card.png')
    await ctx.send(file = discord.File(fp='user_card.png'))

@bot.command()
async def tt(ctx):
    await ctx.message.add_reaction('✅')
    await ctx.send(
        embed=discord.Embed(title="Ссылки на создателя:"),
        components=[
            Button(style=ButtonStyle.URL, label="YouTube", url='https://www.youtube.com/channel/UCQbovJUdaHxkIuNHJDuT25A', emoji='❤'),
            Button(style=ButtonStyle.URL, label="DonationAlerts", url='https://www.donationalerts.com/r/orgctrl5', emoji='🧡'),
            Button(style=ButtonStyle.URL, label="Twitch", url='https://www.twitch.tv/orgctrl5', emoji='💜'),
            Button(style=ButtonStyle.URL, label="VK", url='https://vk.com/go_outme', emoji='💙'),
        ]
    )


bot.run(token)