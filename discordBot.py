import random
import string
import os
import discord
from discord.ext import commands
import time

client = commands.Bot(command_prefix='!')
toggle = False
global NAMES
NAMES = []
ref = ["j.moomoo.com", "share.firstrade.com", "act.webull.com", "dough.com/referrals?referral=", "join.robinhood.com"]

client.remove_command('help')


@client.event
async def on_ready():
    print('Bot is ready!')
    global channel


@client.event
async def on_message(message):
    await client.process_commands(message)
    if toggle == False:

        channel = os.environ['CHANNEL']
        channel = int(channel)

        channel = client.get_channel(channel)
        messageBackup = message
        for x in range(0, len(ref)):
            if ref[x] in message.content:
                await message.delete()
                print(message.author)
                await message.author.send(
                    "Hello! We've noticed you sent a referral link and while we appreciate you trying to help others, referal links are reserved for those who have earned the right. Reach out to us for our assistance with how to get referalls.  If you have any questions or would like to help, don\'t hesitate to message an Admin! Thank you for being a part of Learn and Earn!")
                await channel.send(
                    f"{message.author.mention} has tried to send a referral link.")


    donateChannel = os.environ['DONATE_CHANNEL']
    donateChannel = int(donateChannel)

    if message.channel.id == donateChannel:

        await client.process_commands(message)
        time.sleep(60)
        await message.delete()


@client.command()
async def enable(ctx):
    """ -- Enable referral auto delete."""

    role = discord.utils.get(ctx.guild.roles, name="RBAs")
    if role in ctx.author.roles:
        global toggle
        toggle = not toggle
        if toggle == False:
            await ctx.message.channel.send("Referral Deleter is now on.")
        else:
            await ctx.message.channel.send("Referral Deleter is now off.")


@client.command()
async def roll(ctx, max: int):
    """ -- Roll number between 1 and {input}"""



    # Get the server channel to send the "user rolled # out of #" message to
    channelID = os.environ['ROLL_CHHANNEL']
    channelID = int(channelID)
    roll_channel = client.get_channel(channelID)
    # Get the random roll number from 1 to the number that was inputed
    rolled = random.randint(1, max)

    # If the user that is rolling does not have their name in the list
    if ctx.message.author.name not in NAMES:

        # Send the "User rolled # out of #" message to the admin channel
        await roll_channel.send(f"{ctx.message.author.mention} has rolled a " + str(rolled) + " out of " + str(max))

        # Add the user's name to the list so they can not reroll
        NAMES.append(ctx.message.author.name)

    else:

        # If the name already exists in the list, send this message to the user
        await ctx.message.author.send(
            "Sorry, but you've already rolled in the Togethearn raffle. If there has been a mistake, please contact the Togethearn staff.")


@client.command()
async def rem(ctx, name: str):
    """ -- Remove user from rolled users."""
    # This will give us the User ID without "<", ">", and "@"
    name = name.replace("<", "")
    name = name.replace(">", "")
    name = name.replace("@", "")

    # This gets the role from the server
    role = discord.utils.get(ctx.guild.roles, name="RBAs")

    # This returns the user's name
    user = client.get_user(int(name))
    username = user.name

    # If the role of the user matches the required role
    if role in ctx.author.roles:

        # If the username exists in the list
        if username in NAMES:

            # Remove the name from the list
            NAMES.remove(username)

            # For debugging purposes
            print(NAMES)

        else:

            # If the user does not exist on the list, send this message
            await ctx.author.send("The user " + username + " has not yet rolled.")






@client.command()
async def list(ctx):
    """ -- Get list of all users that have rolled."""

    role = discord.utils.get(ctx.guild.roles, name="RBAs")

    if role in ctx.author.roles:
        await ctx.send(NAMES)

@client.command()
async def invite(ctx):
	await ctx.message.channel.send("https://discord.gg/XGzyksp")

@client.command()
async def clear(ctx):
    """ -- Clear list of users that have rolled."""

    role = discord.utils.get(ctx.guild.roles, name="RBAs")

    if role in ctx.author.roles:
        NAMES.clear()
        await ctx.author.send("The list has been cleared.")

client.run(os.environ['TOKEN'])
