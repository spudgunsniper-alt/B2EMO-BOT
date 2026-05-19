import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages

bot = commands.Bot(command_prefix="!", intents=intents)

# Store messages per channel
pending = {}

@bot.command()
async def commit(ctx, *, message):
    await ctx.message.delete()  # Delete the user's original message

    channel_id = ctx.channel.id
    user_id = ctx.author.id

    # Create storage for this channel if needed
    if channel_id not in pending:
        pending[channel_id] = {}

    # Save the user's message
    pending[channel_id][user_id] = message
    await ctx.send(f"{ctx.author.mention} your message is locked in.")

    # If two users have submitted, reveal both
    if len(pending[channel_id]) == 2:
        reveal = "🔓 **Simultaneous Reveal** 🔓\n\n"
        for uid, msg in pending[channel_id].items():
            user = await bot.fetch_user(uid)
            reveal += f"**{user.name}:** {msg}\n"

        await ctx.send(reveal)

        # Reset for next round
        pending[channel_id].clear()

import os

print("TOKEN:", os.getenv("DISCORD_TOKEN"))

bot.run(os.getenv("DISCORD_TOKEN"))




