import nextcord
import asyncio
import time
import random
import requests
import json
import re
from nextcord.ext import commands, tasks
from nextcord.ui import View, Select
from datetime import datetime, timedelta, timezone
from constants import botToken

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='?', intents=intents)

"""
big info section cause tee hee i love information so much!
"""

message_ids = {}
STAFF_CHANNEL_ID = 1479282567558598848
LOG_CHANNEL_ID = 1479282492149203159
ROLE_NAME = "*"
VerifyName = "Raver"
VerifyRole = "✅"
dripMention = "<@639904427624628224>" # can use this in (f'x') text to @ myself in discord
dripID = "639904427624628224"

def is_owner(ctx):
    role = nextcord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    return role in ctx.author.roles or ctx.author.id == 542882947183673344

def is_drip(ctx):
    return ctx.author.id == 639904427624628224

async def log_to_channel(message):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        utc_now = time.time()
        pacific_offset = -8 * 3600  # Standard PST offset
        if time.localtime(utc_now).tm_isdst == 0:  # Adjust for DST
            pacific_offset = -9 * 3600

        # Add 1 hour to the offset if required (testing or adjustments)
        pacific_offset += 1 * 3600

        # Convert UTC time to Pacific Time
        pacific_time = utc_now + pacific_offset
        timestamp = datetime.fromtimestamp(pacific_time).strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"**[{timestamp}]** {message}"
        await log_channel.send(log_message)

@bot.command()
@commands.check(is_owner)
async def ping(ctx):
    latency_message = f'Pong! {round(bot.latency * 1000)} ms <#1479270319431876768>'
    await ctx.send(latency_message)

@bot.event
async def on_member_join(member):
    if welcomeChannel is not None:
        message_type = random.randint(1, 11)
        messages = {
            1: f"DAMN {str(member.mention)} look at you...",
            2: f"{str(member.mention)} just joined! Hows it goin' cutie :3",
            3: f"{str(member.mention)} just fell from heaven. Oh how lucky we are",
            4: f"{str(member.mention)} looks absolutely stunning. Welcome!",
            5: f"{str(member.mention)} looks just like a dream, prettiest person we've ever seen",
            6: f"{str(member.mention)} has got to be the best looking person here :O",
            7: f"Hey {str(member.mention)}, whats cookin good lookin ; )",
            8: f"The way {str(member.mention)} joined the server. Very Demure. Very Mindful",
            9: f"{str(member.mention)} may look good, I am gonna make them my play toy.",
            10: f"{str(member.mention)} are you https? Because without you, im ://",
            11: f"Hey {str(member.mention)} if you were a vegetable, you'd be a cute-cumber."
        }
        welcome_message = messages[message_type]
        await welcomeChannel.send(welcome_message)
@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if member is None or guild is None:
        return
    if payload.user_id == 1280817864357445663: #checks if bot
        return

    if payload.message_id == message_ids.get('verify_message_id') and str(payload.emoji) == VerifyRole:
        role = nextcord.utils.get(guild.roles, name=VerifyName)
        if role is not None:
            await member.add_roles(role)
            await log_to_channel(f'Assigned {VerifyName} to {member.display_name}')

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if member is None or guild is None:
        return
    if payload.user_id == 1280817864357445663: # checks if bot
        return

    if payload.message_id == message_ids.get('verify_message_id') and str(payload.emoji) == VerifyRole:
        role = nextcord.utils.get(guild.roles, name=VerifyName)
        if role is not None:
            await member.remove_roles(role)
            await log_to_channel(f'Removed {VerifyName} from {member.display_name}')

@bot.command()
@commands.check(is_owner)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Please specify a positive number of messages to delete.", delete_after=5)
        return

    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        confirmation = await ctx.send(f"✅ Deleted {len(deleted)} messages.", delete_after=5)
    except nextcord.Forbidden:
        await ctx.send("❌ I don't have permission to delete messages in this channel.", delete_after=5)
    except nextcord.HTTPException as e:
        await ctx.send(f"❌ An error occurred: {e}", delete_after=5)

@bot.command()
@commands.check(is_owner)
async def restart(ctx):
    if str(ctx.author.id) != dripID:
        for i in range(1, 6):
            await ctx.send(f'{dripMention}!!! <@{ctx.author.id}> IS TRYING TO RESTART THE BOT WITHOUT YOUR PERMISSION!!! GET THEM!!!')
            time.sleep(0.1)
        return
        
    close_message = await ctx.send("Restarting Bot, Please wait")
    for i in range(1, 4):
        await close_message.edit(content=f"Restarting Bot, Please wait{'.' * i}")
        time.sleep(0.5)
    await bot.close()

@bot.command()
async def kill(ctx, user: nextcord.Member = None):
    if user == None:
        await ctx.send("Please enter a user!")
        return
    await ctx.send(f"<@{user.id}> u been died by <@{ctx.author.id}>")

@bot.command()
@commands.check(is_owner)
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: nextcord.Member = None, *, reason=None):
    if user == None:
        await ctx.send("Please enter a user!")
        return

    await user.kick(reason=reason)
    await ctx.send(f'Kicked {user.name} for reason: {reason}')

@bot.command()
@commands.check(is_owner)
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: nextcord.Member = None, *, reason=None):
    if user == None:
        await ctx.send("Please enter a user!")
        return

    await user.ban(reason=reason)
    await ctx.send(f'Banned {user.name} for reason: {reason}')

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    
    staff_channel = bot.get_channel(STAFF_CHANNEL_ID)
    if staff_channel:
        embed = nextcord.Embed(title="Message Deleted", color=nextcord.Color.red())
        embed.add_field(name="User", value=message.author.name, inline=True)
        embed.add_field(name="Channel", value=message.channel.name, inline=True)
        embed.add_field(name="Content", value=message.content or "No content", inline=False)
        await staff_channel.send(embed=embed)

"""
down below is on_ready + bot.run
"""

@bot.event
async def on_ready():
    global welcomeChannel
    welcomeChannel = bot.get_channel(1479274318923042931)
    if welcomeChannel is None:
        await log_to_channel("Could not find the welcome channel.")
    else:
        await log_to_channel(f'Logged in as {bot.user.name}. Now commencing all startup processes.')
        time.sleep(5)

    # Verify Roles Message
    channel1 = bot.get_channel(1479270319431876768)
    if channel1 is not None:
        try:
            await channel1.purge(limit=100)  # Limit the number of messages to purge
            verify_message = await channel1.send("dont be a bitch, spread PLUR, and click to ✅ verify")
            await verify_message.add_reaction("✅")
            message_ids["verify_message_id"] = verify_message.id
            await log_to_channel("Verify role setup complete.")
            time.sleep(5)
        except Exception as e:
            await log_to_channel(f"Error setting up verify role: {e}")
        await log_to_channel(f'{dripMention} BOT IS SET UP AND READY TO GO!')

bot.run(botToken)
