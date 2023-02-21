import discord
from discord.ext import commands

discord.utils.setup_logging()

intents = discord.Intents.all()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
        print('We have sent a message to {0.author}'.format(message))

    await bot.process_commands(message)

@bot.command(name='sum', help='Sums two numbers')
async def sum_command(ctx):
    await ctx.send('Type the first number!')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    msg1 = await bot.wait_for('message', check=check)
    num1 = int(msg1.content)

    msg2 = await bot.wait_for('message', check=check)
    num2 = int(msg2.content)

    try:
        await ctx.send(f'The result is: {num1 + num2}')
    except ValueError:
        await ctx.send('You did not type a number!')

@bot.command(name='subtract', help='Subtracts two numbers')
async def subtract_command(ctx):
    await ctx.send('Type the first number!')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    msg1 = await bot.wait_for('message', check=check)
    num1 = int(msg1.content)

    msg2 = await bot.wait_for('message', check=check)
    num2 = int(msg2.content)

    try:
        await ctx.send(f'The result is: {num1 - num2}')
    except ValueError:
        await ctx.send('You did not type a number!')

@bot.command(name='multiply', help='Multiplies two numbers')
async def multiply_command(ctx):
    await ctx.send('Type the first number!')

    def check(msg): 
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    msg1 = await bot.wait_for('message', check=check)
    num1 = int(msg1.content)

    await ctx.send('Type the second number!')

    msg2 = await bot.wait_for('message', check=check)
    num2 = int(msg2.content)

    try: 
        await ctx.send(f'The result is: {num1 * num2}')
    except ValueError:
        await ctx.send('You did not type a number!')

bot.run('MTA3NzM2NjMyNTQwOTc0Mjg3OA.GEE7Gp.-BQKa5BnzWbJ5XoOOi8GJb4L4gqB5kdLC2HmWg')