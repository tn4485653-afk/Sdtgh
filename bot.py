import discord
from discord.ext import commands
import requests
import asyncio
from flask import Flask
import threading
from datetime import datetime, timedelta
import os
import sys

# =========================
# TOKEN FROM ENV
# =========================
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    print("ERROR: DISCORD_TOKEN not found")
    sys.exit()

# =========================
# INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# WEB SERVER
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_web, daemon=True).start()

# =========================
# BOT READY
# =========================
@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")

# =========================
# TEST
# =========================
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 pong")

# =========================
# RESET
# =========================
@bot.command()
async def reset(ctx, mode=None, token=None):

    if mode != "token" or token is None:
        await ctx.send("❌ Sai cú pháp\n!reset token YOUR_TOKEN")
        return

    try:
        url = f"https://sghhjj.onrender.com/addbot?token={token}"
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            await ctx.send("❌ API lỗi")
            return

        end_time = datetime.utcnow() + timedelta(hours=8)

        msg = await ctx.send("✅ Reset thành công\n⏳ Countdown 8h")

        while True:

            remaining = end_time - datetime.utcnow()

            if remaining.total_seconds() <= 0:
                await msg.edit(content="✅ Đã hết 8 giờ!")
                break

            hours, remainder = divmod(int(remaining.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)

            await msg.edit(
                content=f"⏳ Còn: **{hours:02}:{minutes:02}:{seconds:02}**"
            )

            await asyncio.sleep(10)

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

bot.run(TOKEN)