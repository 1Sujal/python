import discord
from discord.ext import commands
from facebook_scraper import get_posts
from datetime import date
from facebook_scraper import *
import requests
import base64
import io

TOKEN = 'Your discord bot token'

# Define the intents you need
intents = discord.Intents.default()
intents.typing = False  # Disable typing event
intents.presences = False
intents.messages = True
intents.message_content = True  # v2

# Create a bot instance with a command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Store uploaded video information
uploaded_videos = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='check_videos')
async def check_videos(ctx):
    id = '678521690028942'

    for post in get_posts(id, pages=3):
        set_user_agent(
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
        link = (post['video'])
        clock = post['time'].date()
        date2 = date(2023, 11, 21)
        
        if clock > date2:
            # Check if the video has been uploaded before
            if link not in uploaded_videos:
                # Download video from the direct link
                response = requests.get(link)
                while True:
                # Check if the request was successful (status code 200)
                    if response.status_code == 200:
                        # Save the video to a file
                        with open('downloaded_video.mp4', 'wb') as video_file:
                            video_file.write(response.content)

                        with open('downloaded_video.mp4', 'rb') as video_file:
                            await ctx.send(post['post_text'])
                            await ctx.send(file=discord.File(video_file, filename='downloaded_video.mp4'))

                        # Add the video link to the list of uploaded videos
                        uploaded_videos.append(link)
                    else:
                        print(f"Failed to download the video. Status code: {response.status_code}")
            else:
                print(f"Video already uploaded: {link}")
        else:
            print('Error 404')

@bot.command(name='mention')
async def mention(ctx):
    while True:
        await ctx.send("<@1102148901559095308> welcome")

bot.run(TOKEN)
