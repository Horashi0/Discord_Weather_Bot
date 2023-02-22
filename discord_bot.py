#import section
import discord
import requests
import datetime as dt
import os
from dotenv import load_dotenv
# start procedure
client = discord.Client()

@client.event
async def on_ready():
    print(
        'I have hacked into ze mainframe, I am now online {0.user}'.format(client))

bot_sent_message = False

@client.event
async def on_message(message):
    if "!weather" in message.content.lower():
        await message.channel.send("Hello. I am weather bot. Please enter the nearest city/town")

        def check(msg):
            return msg.author != client.user and msg.channel == message.channel

        city_msg = await client.wait_for("message", check=check)
        city = city_msg.content

        if city:
            API_key = ""
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric"

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
            await message.channel.send(f"Temperature in {city}: {temp_celsius}°C")
            await message.channel.send(f"Temperature in {city} feels like: {temp_celsius_feels_like}°C")
            await message.channel.send(f"Humidity in {city}: {humidity}%")
            await message.channel.send(f"Wind speed in {city}: {wind_speed}m/s")
            await message.channel.send(f"Wind direction in {city}: {wind_degrees}°")
            await message.channel.send(f"General Weather in {city}: {clouds}")
            await message.channel.send(f"Sun rises in {city} at {sunrise_time} local time")
            await message.channel.send(f"Sun sets in {city} at {sunset_time} local time")
            await message.channel.send(f"The time in {city} is: {time_id}")
            bot_sent_message = True

        else:
            await message.channel.send("I'm sorry, I couldn't find the weather information for the city you entered.")

        if not bot_sent_message:
            await message.channel.send("Hello. I am weather bot. Please enter the nearest city/town ")

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)