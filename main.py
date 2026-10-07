import os
import discord
from discord.ext import commands
from discord import app_commands

from server import server_on

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())




# //////////////////// Bot Event /////////////////////////
@bot.event
async def on_ready():
    print("Bot Online!")
    print("555")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s)")


# แจ้งคนเข้า -ออกเซิฟเวอร์
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(963602209365450806)
    if channel:
        text = f"Welcome to the server, {member.mention}!"
        await channel.send(text)
    await member.send(f"Welcome to the server, {member.mention}!")


# คำสั่ง chatbot
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    mes = message.content
    if mes == 'hello':
        await message.channel.send("Hello It's me")
    elif mes == 'hi bot':
        await message.channel.send("Hello, " + str(message.author.name))

    await bot.process_commands(message)


# ///////////////////// Commands /////////////////////

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.name}!")


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


# --- คำสั่งเข้า-ออกจากห้องเสียง (Prefix Commands) ---

@bot.command(name='join', help='ให้บอทเข้ามาในห้องเสียงที่คุณอยู่')
async def join_voice(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"เชื่อมต่อเข้าห้องเสียง **{channel.name}** เรียบร้อยแล้ว!")
    else:
        await ctx.send("คุณต้องเข้าห้องเสียงก่อนใช้คำสั่งนี้ครับ!")


@bot.command(name='leave', help='สั่งให้บอทออกจากห้องเสียง')
async def leave_voice(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("ออกจากห้องเสียงเรียบร้อยแล้ว!")
    else:
        await ctx.send("บอทไม่ได้อยู่ในห้องเสียงครับ!")


# --- Slash Commands ---

@bot.tree.command(name='hellobot', description='Replies with Hello')
async def hellocommand(interaction: discord.Interaction):
    await interaction.response.send_message("Hello It's me BOT DISCORD")


@bot.tree.command(name='name')
@app_commands.describe(name="What's your name?")
async def namecommand(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}")


# Slash Commands สำหรับเข้า/ออกจากห้องเสียง
@bot.tree.command(name='join', description='ให้บอทเข้ามาในห้องเสียงที่คุณอยู่')
async def slash_join(interaction: discord.Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.move_to(channel)
        else:
            await channel.connect()
        await interaction.response.send_message(f"เชื่อมต่อเข้าห้องเสียง **{channel.name}** เรียบร้อยแล้ว!")
    else:
        await interaction.response.send_message("คุณต้องเข้าห้องเสียงก่อนใช้คำสั่งนี้ครับ!", ephemeral=True)


@bot.tree.command(name='leave', description='สั่งให้บอทออกจากห้องเสียง')
async def slash_leave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("ออกจากห้องเสียงเรียบร้อยแล้ว!")
    else:
        await interaction.response.send_message("บอทไม่ได้อยู่ในห้องเสียงครับ!", ephemeral=True)


# คำสั่ง Help (ส่งเป็นข้อความธรรมดาแทน Embed)
@bot.tree.command(name='help', description='Bot Commands')
async def helpcommand(interaction: discord.Interaction):
    text = (
        "**Help Me! - Bot Commands**\n"
        "- `/hello1`: Hello Command\n"
        "- `/hello2`: Hello Command\n"
        "- `/hello3`: Hello Command"
    )
    await interaction.response.send_message(text)


server_on()

bot.run(os.getenv('TOKEN'))
