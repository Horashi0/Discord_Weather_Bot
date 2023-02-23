#import section
import discord
import requests
import datetime as dt
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand

# start procedure
client = discord.Client()


@client.event
async def on_ready():
    print(
        'I have hacked into ze mainframe, I am now online {0.user}'.format(client))

bot_sent_message = False

slash = SlashCommand(client, sync_commands=True)

@slash.slash(name="weather", description="Get weather information for city",
             options=[
                {
    "name":"city",
    "description": "City name",
    "type": 3,
    "required": True
                }
             ])

@client.event
async def on_message(message):
    if "!weather" in message.content.lower():
        await message.channel.send("Hello. I am weather bot. Please enter the nearest city/town")

        def check(msg):
            return msg.author != client.user and msg.channel == message.channel

        city_msg = await client.wait_for("message", check=check)
        city = city_msg.content

        try:
            if city:
                API_KEY = os.getenv("API_KEY")
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

                weather_data = requests.get(url).json()
                temp_celsius = weather_data["main"]["temp"]
                temp_celsius_feels_like = weather_data["main"]["feels_like"]
                sunrise_time = dt.datetime.utcfromtimestamp(
                    weather_data["sys"]["sunrise"] + weather_data["timezone"])
                sunset_time = dt.datetime.utcfromtimestamp(
                    weather_data["sys"]["sunset"] + weather_data["timezone"])
                clouds = weather_data["weather"][0]["description"]
                wind_speed = weather_data["wind"]["speed"]
                wind_degrees = weather_data["wind"]["deg"]
                place = weather_data["name"]
                identification = weather_data["id"]
                timezone = weather_data["timezone"]
                humidity = weather_data["main"]["humidity"]
                time_id = dt.datetime.utcfromtimestamp(
                    weather_data["dt"] + weather_data["timezone"])
                embed = discord.Embed(
                    title=f"Weather in {city}",
                    description=f"Temperature: {temp_celsius}°C\nFeels like: {temp_celsius_feels_like}°C\nHumidity: {humidity}%\nWind speed: {wind_speed}m/s\nWind direction: {wind_degrees}°\nGeneral weather: {clouds}\nSunrise time: {sunrise_time}\nSunset time: {sunset_time}\nFor more information: https://openweathermap.org/city/{identification}",
                    color=discord.Color.blue())

                await message.channel.send(embed=embed)
                bot_sent_message = True

            else:
                await message.channel.send("I'm sorry, I couldn't find the weather information for the city you entered.")

            if not bot_sent_message:
                await message.channel.send("Hello. I am weather bot. Please enter the nearest city/town ")
        except:
            await message.channel.send("I'm sorry someting went wrong, I couldn't find the weather information for the city you entered. Please try again")

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)