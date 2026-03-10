import discord
from discord.ext import commands
import requests
import asyncio
from flask import Flask
import threading
from datetime import datetime, timedelta
import os

# =========================
# LẤY TOKEN TỪ RENDER ENV
# =========================
TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# WEB SERVER (PORT 8080)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_web).start()

# =========================
# BOT ONLINE
# =========================
@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

# =========================
# TEST COMMAND
# =========================
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 pong")

# =========================
# RESET COMMAND
# =========================
@bot.command()
async def reset(ctx, type1=None, token=None):

    if type1 != "token" or token is None:
        await ctx.send("❌ Sai cú pháp\n!reset token YOUR_TOKEN")
        return

    try:
        url = f"https://sghhjj.onrender.com/addbot?token={token}"
        r = requests.get(url)

        if r.status_code != 200:
            await ctx.send("❌ API lỗi")
            return

        end_time = datetime.now() + timedelta(hours=8)

        msg = await ctx.send("✅ Reset thành công\n⏳ Bắt đầu đếm ngược 8h")

        while True:

            remaining = end_time - datetime.now()

            if remaining.total_seconds() <= 0:
                await msg.edit(content="✅ Đã hết 8 giờ!")
                break

            hours, remainder = divmod(int(remaining.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)

            await msg.edit(
                content=f"✅ Reset thành công\n⏳ Còn lại: **{hours:02}:{minutes:02}:{seconds:02}**"
            )

            await asyncio.sleep(10)

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

# =========================

bot.run(TOKEN)