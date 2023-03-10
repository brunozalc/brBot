import os
import requests
import discord
from discord import app_commands
from discord.ext import commands
from credentials import token, WEATHER_API_KEY

discord.utils.setup_logging()

intents = discord.Intents.all()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try: 
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')

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

@bot.tree.command(name='weather', description='Checks the weather in a city')
async def weather_command(ctx, city: str):
    weather_suggestions = {
    "Clouds": "You should bring an umbrella if things look overcast!",
    "Rain": "You might want to take an umbrella with you!",
    "Drizzle": "You might want to take an umbrella with you!",
    "Clear": "It looks like a good day to go outside!",
    "Snow": "You should bring a jacket and a hat!",
    "Thunderstorm": "You should stay inside!",
    "Tornado": "You should stay inside! Please be safe!",
    "Mist": "Be careful when driving!",
    "Fog": "Be careful when driving!",
    "Smoke": "Be careful when driving! Maybe use a mask if you are going outside!",
    "Haze": "Be careful when driving! Maybe use a mask if you are going outside!"
    }
    
    api_key = WEATHER_API_KEY
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    response = requests.get(base_url)
    weather = response.json()

    if response.status_code != 200:
        print(f'Process exited with error: {response.status_code}')
        await ctx.response.send_message('Sorry, there was an error. Either the city does not exist or you did not type it correctly.')

    else:
        sent = False
        for key in weather_suggestions.keys():
            if key in weather["weather"][0]["main"]:
                await ctx.response.send_message(f'Weather in {city} is {weather["weather"][0]["description"]}. The temperature is {round(weather["main"]["temp"])}??C and the humidity is {weather["main"]["humidity"]}%. {weather_suggestions[weather["weather"][0]["main"]]}')
                sent = True
                break
        if not sent:
            await ctx.response.send_message(f'Weather in {city} is {weather["weather"][0]["description"]}. The temperature is {round(weather["main"]["temp"])}??C and the humidity is {weather["main"]["humidity"]}%.')
            sent = True
    
bot.run(token)