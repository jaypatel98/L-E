import asyncio
import json
import random
import re
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
#     client.loop.create_task(clearUsers())




@client.event
async def on_message(message):

    await client.process_commands(message)

    if toggle == False:

        refWarningChannel = os.environ['REF_CHANNEL']
        refWarningChannel = int(refWarningChannel)

        refWarningChannel = client.get_channel(refWarningChannel)
        for x in range(0, len(ref)):
            if ref[x] in message.content:
                await message.delete()
                print(message.author)
                await message.author.send(
                    "Hello! We've noticed you sent a referral link and while we appreciate you trying to help others, referal links are reserved for those who have earned the right. Reach out to us for our assistance with how to get referalls.  If you have any questions or would like to help, don\'t hesitate to message an Admin! Thank you for being a part of Learn & Earn!")
                await refWarningChannel.send(
                    f"{message.author.mention} has tried to send a referral link.")

    donateChannel = os.environ['DONATE_CHANNEL']
    donateChannel = int(donateChannel)

    if message.channel.id == donateChannel:
        await client.process_commands(message)
        await asyncio.sleep(60)
        await message.delete()

@client.event
async def on_member_join(member):

    starthere = client.get_channel(os.environ['START_HERE'])
    userAgreementchannel = client.get_channel(os.environ['USER_AGREEMENT'])

    server = starthere.guild
    role = discord.utils.find(lambda r: r.name == 'New User', server.roles)
    await member.add_roles(role)

    await starthere.send(
        f"Welcome to Learn and Earn {member.mention}! Press the green checkbox in the {userAgreementchannel.mention} channel to get access to the full server.")

@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == os.environ['MESSAGE_ID']:
        print(payload.emoji.name)
        # Find a role corresponding to the Emoji name.
        guild_id = payload.guild_id

        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        roleAdd = discord.utils.find(lambda r: r.name == 'Community Members', guild.roles)
        roleRemove = discord.utils.find(lambda r: r.name == 'New User', guild.roles)

        print(payload.emoji.name)
        if(payload.emoji.name == '✅'):
            print("inhere")

            role = discord.utils.get(guild.roles, name="Community Members")

        if role is not None:
            print(role.name + " was found!")
            print(role.id)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(roleAdd)
            await member.remove_roles(roleRemove)
            print("done")




# @client.event
# async def clearUsers():
#     await client.wait_until_ready()
#     while True:
#         counter = 0
#         startchannel = client.get_channel(os.environ['START_HERE'])

#         server = startchannel.guild
#         # role = discord.utils.find(lambda r: r.name == 'New User', client.roles)

#         for member in server.members:

#             for role in member.roles:
#                 if role.name == "New User":
#                     counter+=1
#                     print(f"Removed: {member}")
#                     members = str(member)
#                     memberNameTemp = re.match(r"[^#]+", members)
#                     memberName = memberNameTemp.group()
#                     # await member.send(
#                     #     f"Hi, {memberName} we noticed you joined our group but have not gotten full access to all of our channels. To get full access please go to the user agreement channel and click the green check mark one time to have full access. To make this process easier for you I have removed you and you can use the attached invite to rejoin the group and get properly verified. Hope to see you soon, {memberName}.\n Invite link: https://discord.gg/XGzyksp")
#                     # await server.kick(member, reason="User did not verify")
#         print(counter)
#         await asyncio.sleep(3600)






@client.command()
async def enable(ctx):
    """ -- Enable referral auto delete."""

    role = discord.utils.get(ctx.guild.roles, name="Admins")
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
    role = discord.utils.get(ctx.guild.roles, name="Admins")
    if role in ctx.author.roles:
        rolled = random.randint(1, max)
        await ctx.channel.send(f"You have rolled a " + str(rolled) + " out of " + str(max))


@client.command()
async def invite(ctx):
    await ctx.message.channel.send("https://discord.gg/4EdCTGh")

client.run(os.environ['TOKEN'])
