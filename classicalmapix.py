import datetime
import json
import discord
from discord.ext import commands

intents = discord.intents.all()
intents.members = True
intents.guild_messages = True

client = commands.Bot(command_prefix='!', intents=intents, self_bot=False, case_sensitive=True) 

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="Random GitHub Repo"))
    print(f'{client.user} has connected to Discord!')

    # Load configuration
    global welcome_messages
    try:
        with open('welcome_messages.json', 'r') as f:
            welcome_messages = json.load(f)
    except FileNotFoundError:
        welcome_messages = {}
    # Load configuration
    with open('welcome_messages.json', 'r') as f:
        welcome_messages = json.load(f)



@client.event
async def on_member_join(member):
    guild = member.guild
    channel = await guild.fetch_channel()  # Replace with your channel ID
    #role = discord.utils.get(guild.roles, name='Newcomer')  # Example role assignment



    message = welcome_messages.get(str(guild.id), 'hey there, welcome')

    # Replace the placeholder with the member's mention
    message = message.replace('{member}', member.mention)
    message = message.replace('{guild}', guild.name)

    await channel.send(message)

@client.event
async def on_member_remove(member):
    channel_id = () #put your channel id in the lil brackets alr?
    channel = client.get_channel(channel_id)
    message = f'{member.mention} has left the server.'
    await channel.send(message)





    @client.command()
    @commands.has_premissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for reason: {reason}')

    @client.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for reason: {reason}')

@client.command()
async def poll(ctx, question, *options):
    if len(options) < 2:
        await ctx.send('You need to provide at least two options for the poll.')
        return
    if len(options) > 10:
        await ctx.send('You can provide a maximum of 10 options for the poll.')
        return

    description = []
    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    for i, option in enumerate(options):
        description.append(f'{emojis[i]} {option}')

    embed = discord.Embed(title=question, description='\n'.join(description), color=0x00ff00)
    poll_message = await ctx.send(embed=embed)

    for i in range(len(options)):
        await poll_message.add_reaction(emojis[i])

@client.command()
async def message_count(ctx, member: discord.Member, start_date: str, end_date: str):
    message_count = 0

    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    for channel in ctx.guild.text_channels:
        try:
            async for message in channel.history(limit=None, after=start, before=end_date):
                if message.author == member:
                    message_count += 1
        except discord.Forbidden:
            continue  # Skip channels where the bot doesn't have access

    await ctx.send(f'{member.mention} sent {message_count} messages between {start_date} and {end_date.strftime("%Y-%m-%d")}.')

@client.command()
@commands.has_premissions(manage_roles=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.addroles(role, reason=reason)
    await ctx.send(f'{member.mention} has been muted for reason: {reason}')  


@client.command()
@commands.has_premissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    # Add a code to store warnings and all
    await ctx.send(f'{member.mention} has been warned. Reason {reason}')

@client.command()
async def commands(ctx):
    embed = discord.Embed(title="Bot Commands", description="Here are all the commands")
    for command in client.commands:
        embed.add_field(name=f"{command.name} {command.signature}", value=command.help, inline=False)
    await ctx.sent(embed=embed)


client.run('') #add your bot token :D                