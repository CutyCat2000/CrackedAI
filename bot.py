import discord 
from discord.ext import commands
import httpx
import asyncio
import websockets
import random
import json
import base64
from PIL import Image
from io import BytesIO
import perplexity
import re
import asyncio
from discord import app_commands, ui
from datetime import datetime, timedelta
import string
import ai_dm
from fake_useragent import UserAgent
from sing import sing
import os
from describe import describe
import discord
import os
import src.log
import sys
import pkg_resources
import json
from discord.ext import commands
import flask
from textgen import textgen
from threading import Thread
from tts import tts
from remake import remake
from shazamio import Shazam

app = flask.Flask("app")

@app.route("/")
def isRunning():
    return "Bots are online."

def run():
  app.run(host="0.0.0.0", port=4061)

server = Thread(target=run)
server.start()

TOKEN = <TOKEN>
TOKEN2 = <TOKEN2>
TOKEN3 = <TOKEN3>

bot = commands.Bot(command_prefix='!', intents = discord.Intents.default())
splmod = commands.Bot(command_prefix='-', intents=discord.Intents.all())
logger = src.log.setup_logger(__name__)
    
ua = UserAgent()

chatbot_chats = {}

AsyncClient = httpx.AsyncClient()

userDailyLimits = {}
serverDailyLimits = {}

image_sessions = []

current_session_index = 0

image_sessions_user_agents = {}
current_sing_pos = {1:0,2:0,3:0,4:0,5:0}

def generate_user_agent():
    # Define the range for the random length of the string
    min_length = 5
    max_length = 65

    # Generate a random length for the string
    length = random.randint(min_length, max_length)

    # Define the characters from which the random string will be composed
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate the random string using the chosen length and characters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string + " playgroundai.com"

def generate_user_agent2():
    # List of possible values for each part of the user-agent
    windows_versions = ['Windows NT 10.0', 'Windows NT 6.1', 'Windows NT 6.2', 'Windows NT 6.3', 'Windows NT 6.4', 'Windows NT 6.0']
    architectures = ['Win64; x64', 'Win32; x86']
    webkit_versions = ['537.36', '537.38', '537.41', '537.42']
    chrome_versions = ['114.0.0.0', '115.0.0.0', '116.0.0.0', '117.0.0.0']
    safari_versions = ['537.36', '537.38', '537.40', '537.42']
    edge_versions = ['114.0.1823.86', '115.0.1823.89', '116.0.1823.92', '117.0.1823.95']

    # Randomly select values for each part
    windows_version = random.choice(windows_versions)
    architecture = random.choice(architectures)
    webkit_version = random.choice(webkit_versions)
    chrome_version = random.choice(chrome_versions)
    safari_version = random.choice(safari_versions)
    edge_version = random.choice(edge_versions)

    # Format the user-agent string
    user_agent = f"Mozilla/5.0 ({windows_version}; {architecture}) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{chrome_version} Safari/{safari_version} Edg/{edge_version}"
    
    return user_agent

for x in image_sessions:
    image_sessions_user_agents[x] = generate_user_agent2()
    

splai_image_sessions = image_sessions

cookies = {}


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
perplexity_cookies = {
    'cf_clearance': 'Gu9Jtw4rC0pRAS5HuP1phemXA8F14bh11qLrN_qvU5k-1694265713-0-1-5bb078a8.84199131.cb12748-160.0.0',
    'trackingAllowed': 'false',
    '_ga': 'GA1.1.129096313.1694265734',
    'next-auth.csrf-token': '205dd62314f0bb343da28074854f80587325bb618eb92994fd9a8b8ed8b657a4%7Ce9c80a9f9a0a20f1c50831cf71d22640d8efcefc552d7db2ca3f890ac9ede391',
    'g_state': '{"i_l":0}',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fwww.perplexity.ai%2Fapi%2Fauth%2Fsignin-callback%3Fredirect%3Dhttps%253A%252F%252Fwww.perplexity.ai%252Fsearch%252F0f81b88e-5184-4f40-91fc-e2a75e3d71bb%253Fs%253Du',
    '_ga_SH9PRBQG23': 'GS1.1.1694961899.4.1.1694962346.0.0.0',
    '__cflb': '02DiuDyvFMmK5p9jVbWbam6CcSLCt41hZgmZLbF2UKFic',
    'AWSALB': 'GzHK2ezvxBtPIyMBaGKTQo8RIDb3kwHfK7gGLxCxurNGKNM3TSID4ek6as9gzXAXyvDuZnl/o/fk/SofDN4Le/Z0lttFHybFHzYU396+3W5TgrEf1DNPRn1naU7l',
    'AWSALBCORS': 'GzHK2ezvxBtPIyMBaGKTQo8RIDb3kwHfK7gGLxCxurNGKNM3TSID4ek6as9gzXAXyvDuZnl/o/fk/SofDN4Le/Z0lttFHybFHzYU396+3W5TgrEf1DNPRn1naU7l',
    '__Secure-next-auth.session-token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..aITmyUlDDDY6rT0Q.DKkU8kTZWGK0_wcKGrSWhPnr75sAJ014cHAcMa5QJ3JPnVThann2rYNT2sX50YEJcW0WYhmtd_DPXq3RSnON0q2WdtD4YqAEob3SwRrQz-hMH4HM6ILchhTHPpVcD0zZGFKo8MMkNWUgQ-BP4YXXdYh9fweMGk1J3XiMDCdAYSPB_PN5Jik7VStM9slro-HT1xGS8z4a52NbiGuZjo65MM48boxclrmPTriHOLFzvTvtuobi_hnc6wyX3QDHsyk-lNSGmw-t8JVDcJN5iG-U6bXXodBUrGBGtgJQ9tsASTaenD7QHnVM2fygWxp1XZjlSBu_mZC5cgWdiyq1ZuJkcQVGQB6VlidsTtqjghogD7mKWD8h43Xwftq_nJDg9o5Cjg.caSOx_I1ZLp_oY-Ymtr9zw',
}

perplexity_headers = {
    'authority': 'www.perplexity.ai',
    'accept': '*/*',
    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    'baggage': 'sentry-environment=production,sentry-release=J9TUHbuF40Xu0qG6einWJ,sentry-public_key=bb45aa7ca2dc43b6a7b6518e7c91e13d,sentry-trace_id=2def8bc4372344698f5440c3e7ea680a',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': 'cf_clearance=Gu9Jtw4rC0pRAS5HuP1phemXA8F14bh11qLrN_qvU5k-1694265713-0-1-5bb078a8.84199131.cb12748-160.0.0; trackingAllowed=true; _ga=GA1.1.129096313.1694265734; next-auth.csrf-token=205dd62314f0bb343da28074854f80587325bb618eb92994fd9a8b8ed8b657a4%7Ce9c80a9f9a0a20f1c50831cf71d22640d8efcefc552d7db2ca3f890ac9ede391; g_state={"i_l":0}; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.perplexity.ai%2Fapi%2Fauth%2Fsignin-callback%3Fredirect%3Dhttps%253A%252F%252Fwww.perplexity.ai%252Fsearch%252F942fa0c1-7a49-4b52-8e44-d2ba4fd3e261%253Fs%253Du; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..WlRyPIa0sny-lynb.6rR2Ua3nhgzAPypGNCgqNPKKqM-76RZQCzvrYuLt4xuK3_BIycOnUDEfWhUI_Dt_Arwov2Z-TRDfT_WBXYGBIsnt0Wlpyvt-fMQlciGGvIbqyDnwU5tagmEhG98BE0nZRYyKL6nQTg7tLl6qc_HyVeDrTHJsHJiY5ViLXJTgRyKsnvMnl0UGIHws7jNtGLunmHBELTH670kw8KwI_sKxQs9DN-oSS-VUDAocCFo7fdkC-ufy0c7EJBKgivu-AtbwWKdsHDF_KMLyK_RkGyQvqCP-Gh7rdtaTrK0BKIEWPig5qIQTZ82TbaziX_oqMMRLSekp_a5OD_PoQlOrzkXvrnAnaTe9Ql1VCwE4SC2pTziutk8qveUBgah6Cizgfx2_zA.30Xk4hzUqdVF_72hYyGbNA; __cflb=0H28uyqfqXYb7pqfMDzeXDPTV3XgWMxrpBYBPb8q31E; _ga_SH9PRBQG23=GS1.1.1694961899.4.1.1694961943.0.0.0; AWSALB=B7+lm0ZHU15rPZSJaFBHnTgwN1lo9ETpoKKwJ2sCwNVpTO1CLGTveNA9ZhMh61wTFQPJ+wv81af9G/hq0rwT1gpR2xUZC6GjjFPKvpLGH2tWTnP25l+z5HkOs//Z; AWSALBCORS=B7+lm0ZHU15rPZSJaFBHnTgwN1lo9ETpoKKwJ2sCwNVpTO1CLGTveNA9ZhMh61wTFQPJ+wv81af9G/hq0rwT1gpR2xUZC6GjjFPKvpLGH2tWTnP25l+z5HkOs//Z',
    'pragma': 'no-cache',
    'referer': 'https://www.perplexity.ai/search/942fa0c1-7a49-4b52-8e44-d2ba4fd3e261?s=u',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '2def8bc4372344698f5440c3e7ea680a-ac4ff7799094e9f6-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}



class client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(intents=intents, activity=discord.Game("For risks and side effects, read the package insert and ask your doctor or pharmacist."),allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user = True))
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        await self.tree.sync()
    async def on_ready(self):
        while True:
            try:
                ping_chance = random.randint(0,50)
                if ping_chance == 0:
                    ping_time = 0
                else:
                    ping_time = 1
                await AsyncClient.get("https://status.wuemeli.com/api/push/jWBeroAjs8?status=up&msg=OK&ping="+str(ping_time))
                await asyncio.sleep(10)
            except:
                pass
            
client = client()

def get_remaining_time():
    now = datetime.utcnow()
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0)
    time_left = end_of_day - now
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours} hours, {minutes} minutes, and {seconds} seconds"

def get_time_until_end_of_day():
    now = datetime.utcnow()
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0)
    time_left = end_of_day - now
    return time_left.total_seconds()


@client.tree.command(name = "imagine", description = "Imagine an Image")
@app_commands.choices(design=[
    app_commands.Choice(name="No design", value=""),
    app_commands.Choice(name="Pixar", value="--disney-pixar"),
    app_commands.Choice(name="Pixel Mode", value="- 2d game pixel design, up to down view, pixel, (64x64) -"),
    app_commands.Choice(name="Cartoon", value="--cartoon"),
    app_commands.Choice(name="Anime", value="--anime"),
    app_commands.Choice(name="Watercolor", value="--watercolor"),
    app_commands.Choice(name="Retro", value="--retro"),
    app_commands.Choice(name="Minimalist", value="--minimalist"),
    app_commands.Choice(name="Surreal", value="--surreal"),
    app_commands.Choice(name="Impressionist", value="--impressionist"),
    app_commands.Choice(name="Expressionist", value="--expressionist"),
    app_commands.Choice(name="Abstract", value="--abstract"),
    app_commands.Choice(name="Futuristic", value="--futuristic"),
    app_commands.Choice(name="Steampunk", value="--steampunk"),
    app_commands.Choice(name="Cyberpunk", value="--cyberpunk"),
    app_commands.Choice(name="Graffiti", value="--graffiti"),
    app_commands.Choice(name="Vintage", value="--vintage"),
    app_commands.Choice(name="Neon", value="--neon"),
    app_commands.Choice(name="Realism", value="--realism"),
    app_commands.Choice(name="Fantasy", value="--fantasy"),
    app_commands.Choice(name="Cubism", value="--cubism"),
    app_commands.Choice(name="Surrealism", value="--surrealism"),
])
@app_commands.choices(design2=[
    app_commands.Choice(name="No design", value=""),
    app_commands.Choice(name="Pixar", value="--disney-pixar"),
    app_commands.Choice(name="Pixel Mode", value="- 2d game pixel design, up to down view, pixel, (64x64) -"),
    app_commands.Choice(name="Cartoon", value="--cartoon"),
    app_commands.Choice(name="Anime", value="--anime"),
    app_commands.Choice(name="Watercolor", value="--watercolor"),
    app_commands.Choice(name="Retro", value="--retro"),
    app_commands.Choice(name="Minimalist", value="--minimalist"),
    app_commands.Choice(name="Surreal", value="--surreal"),
    app_commands.Choice(name="Impressionist", value="--impressionist"),
    app_commands.Choice(name="Expressionist", value="--expressionist"),
    app_commands.Choice(name="Abstract", value="--abstract"),
    app_commands.Choice(name="Futuristic", value="--futuristic"),
    app_commands.Choice(name="Steampunk", value="--steampunk"),
    app_commands.Choice(name="Cyberpunk", value="--cyberpunk"),
    app_commands.Choice(name="Graffiti", value="--graffiti"),
    app_commands.Choice(name="Vintage", value="--vintage"),
    app_commands.Choice(name="Neon", value="--neon"),
    app_commands.Choice(name="Realism", value="--realism"),
    app_commands.Choice(name="Fantasy", value="--fantasy"),
    app_commands.Choice(name="Cubism", value="--cubism"),
    app_commands.Choice(name="Surrealism", value="--surrealism"),
])
@app_commands.choices(detail=[
    app_commands.Choice(name="Low", value=15),
    app_commands.Choice(name="Medium", value=50),
    app_commands.Choice(name="High", value=150)
])
@app_commands.choices(style=[
    app_commands.Choice(name="Default", value=15),
    app_commands.Choice(name="High Detailed old Painting", value=5),
    app_commands.Choice(name="Digital Art", value=25),
    app_commands.Choice(name="Negative", value=-15),
])
@app_commands.choices(model=[
    app_commands.Choice(name="SplGen v5", value="latest"),
    app_commands.Choice(name="SplGen v4", value="v4"),
    app_commands.Choice(name="SplGen v3", value="v3"),
    app_commands.Choice(name="SplGen v2", value="v2"),
])
async def imagine_command(interaction, prompt:str, design:str, design2:str, detail:int, model:str="latest", style:int=15, width:int=1024, height: int=1024, negative_prompt:str="", background:str=None, artist:str=None):
    """Imagine an Image
    
    Parameters
    ----------
    prompt : str
        The prompt to make the image
    design : str
        The design of the image
    design2 : str
        The merged design of the image
    width : int
        The width of the image
    height : int
        The height of the image
    style : int
        The style adjustment of the image
    background : str
        The color/style of the background
    negative_promt : str
        What to exclude from the image
    artist : str
        The artist made the image
    detail : str
        The detail level of the image
    model : str
        The model to use"""
    global current_session_index, cookies
    md = ""
    modelType = "stable-diffusion-xl"
    noDelay = False
    await interaction.response.defer()
    for guild in client.guilds:
        if guild.id == 1130039507379568782:
            try:
                member = await guild.fetch_member(interaction.user.id)
                for role in member.roles:
                    if role.id == 1135552096905732206 or role.id==1136599915997450261:
                        noDelay = True
            except:
                pass
    try:
        oprompt = prompt
        if noDelay == False:
            msg = await interaction.followup.send("For generation speedup, either boost [our Discord server](<https://discord.gg/9zAy8NgyQz>) or donate to [Daniel Klimmer on PayPal](<https://paypal.me/thefiredragon05>) and dm [@splittic](<https://discord.com/users/1064553604003942430>) afterwards")
        #await interaction.followup.send("Disabled for now, coming back soon")
        if not interaction.user.id in userDailyLimits or interaction.user.id in [1001822685791269005, 270262006827712514, 266232329557639168]:
            userDailyLimits[interaction.user.id] = 0
        userDailyLimits[interaction.user.id] += 1
        limit = 25
        for guild in client.guilds:
            if guild.id == 1130039507379568782:
                try:
                    member = await guild.fetch_member(interaction.user.id)
                    if interaction.user.id == 1145676460225478686:
                        await interaction.user.send("Found member")
                    for role in member.roles:
                        if role.id == 1135552096905732206 or role.id==1136599915997450261:
                            if interaction.user.id == 1145676460225478686:
                                await interaction.user.send("Found role")
                                break;
                            limit = 100
                except:
                    pass

        if userDailyLimits[interaction.user.id] > limit:
            remaining_time = get_remaining_time()
            embed = discord.Embed(title="You already reached the daily limit of " + str(limit) + " images.", description = "Try again in " + remaining_time + ".\nTo increase this, either boost [our Discord server](https://discord.gg/9zAy8NgyQz) or donate to [Daniel Klimmer on PayPal](https://paypal.me/thefiredragon05) and dm [@splittic](https://discord.com/users/1064553604003942430) afterwards")
            await interaction.followup.send(ephemeral=True, embed = embed)
            if userDailyLimits[interaction.user.id] == limit+1:
                await asyncio.sleep(get_time_until_end_of_day())
                userDaily
            return
        if interaction.guild:
            if not interaction.guild.id in serverDailyLimits:
                serverDailyLimits[interaction.guild.id] = 0
            serverDailyLimits[interaction.guild.id] += 1
            serverlimit = 500
            if interaction.guild.id == 1130039507379568782:
                serverlimit = 10000

            if serverDailyLimits[interaction.guild.id] > serverlimit:
                remaining_time = get_remaining_time()
                await interaction.followup.send(ephemeral=True, content="Your server reached the daily limit of " + str(serverlimit) + " images. Try again in " + remaining_time + ".")
                if serverDailyLimits[interaction.server.id] == limit+1:
                    await asyncio.sleep(get_time_until_end_of_day())
                    serverDailyLimits[interaction.guild.id] = 0
                return
        if width and width <= 16384 and height and height <= 16384:
            pass
        else:
            width = 512
            height = 512

        prompt = prompt.replace('--'+str(width)+'p-'+str(height)+'p','')
        if artist:
            prompt = prompt + " | --artist="+artist+" | "
        if model == "v2":
            prompt += " --perfect --cool"
        if model == "v3":
            prompt += "  --perfect --cool --4k | infinity | accelerate | detail --cam"
        if model == "v4":
            prompt += "  --perfect --cool --4k | infinity | accelerate | detail --cam"
            modelType ="stable-diffusion-xl"
            md = "MBBXL_Ultimate"
        if model == "latest":
            prompt += "  --perfect --cool --4k | infinity | accelerate | detail --cam | pure perfection, award-winning, professional, highly detailed"
            modelType ="stable-diffusion-xl"
            md = "MBBXL_Ultimate"
            model = "v5 Unlimited"
        seed = random.randint(0,99999999999)
        current_session = image_sessions[current_session_index]
        cookies = {
            '__Secure-next-auth.session-token': current_session,
        }
        if background:
            design = design + " - bg-color:"+background
        headers = {
            'authority': 'playgroundai.com',
            'user-agent': image_sessions_user_agents[current_session],
            "X-Forwarded-For": "163.169.1.100",
        }
        batchId = str(random.randint(1000000000,9999999999))
        negative_prompt += ", Contrast, saturation, oversaturation, cursed, misformed, broken, eyes, ugly, bad quality, worst quality, nsfw, blurry, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers, ugly, deformed, noisy, blurry, distorted, grainy"
        json_data = {
            'dream_booth_model': md,
            'filter': md,
            'width': width,
            'height': height,
            'seed': seed,
            'num_images': 1,
            'sampler': 3,
            'cfg_scale': style,
            'guidance_scale': 1250,
            'strength': 99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999,
            'steps': detail,
            'negativePrompt': negative_prompt,
            'prompt': prompt + " "+design2+" " + design,
            'hide': True,
            'isPrivate': False,
            'modelType': modelType,
            'batchId': batchId,
            'generateVariants': False,
            'initImageFromPlayground': False,
        }
        if interaction.user.id == 1145676460225478686:
            await interaction.user.send(batchId)
        AsyncClient2 = httpx.AsyncClient()
        response = await AsyncClient2.post('https://api.corsme.com/?https://playgroundai.com/api/models', cookies=cookies,json=json_data, headers=headers, timeout =999)
        if str(response.json()) == "{'error': 'Not authenticated'}":
            current_session_index = current_session_index + 1 if current_session_index != len(image_sessions) else 0
            return await interaction.followup.send(content="Please tell [@splittic](https://discord.com/users/1064553604003942430) that the VM with the ID "+current_session.split("-")[0]+ " crashed.")
        image_url = []
        try:
            for n in range(len(response.json()['images'])):
                image_url.append('https://storage.googleapis.com/pai-images/' + response.json()['images'][n-1]['imageKey']+'.png')
        except:
            if response.json()['errorCode'] == 'SAFETY_FILTER':
                await interaction.followup.send(content='We blocked the output as it is not safe for work')
                return
            else:
                if interaction.user.id == 1145676460225478686:
                    await interaction.user.send(response.json()["errorCode"])
                if interaction.guild and interaction.guild.id != 1130039507379568782:
                    await interaction.followup.send(content='To save CPU and money, we limited all daily generations to '+str(len(splai_image_sessions))+'000 for now.\nTo increase this, donate to [Daniel Klimmer on PayPal](https://paypal.me/thefiredragon05) and dm [@splittic](https://discord.com/users/1064553604003942430) afterwards')
                    current_session_index = current_session_index + 1 if current_session_index != len(image_sessions) else 0
                elif interaction.guild:
                    await interaction.followup.send(content='To save CPU and money, we limited daily generations in this server to 10000.\nAdd it to your server for more.')
                    current_session_index = current_session_index + 1 if current_session_index != len(image_sessions) else 0
                else:
                    await interaction.followup.send(content='To save CPU and money, we limited all daily generations to '+str(len(splai_image_sessions))+'000 for now.\nTo increase this, donate to [Daniel Klimmer on PayPal](https://paypal.me/thefiredragon05) and dm [@splittic](https://discord.com/users/1064553604003942430) afterwards')
                    current_session_index = current_session_index + 1 if current_session_index != len(image_sessions) else 0

                return
        #embed1=discord.Embed(title='Your images are ready.', description=f"[Open Image 1 in {width}p/{height}p]("+image_url[0]+f")\n[Open Image 2 in {width}p/{height}p]("+image_url[1]+f")\n[Open Image 3 in {width}p/{height}p]("+image_url[2]+f")\n[Open Image 4 in {width}p/{height}p]("+image_url[3]+")", url="https://google.com")
        timex = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        embed1=discord.Embed(title='Your image is ready.', description=f"[Open Image in {width}p/{height}p]("+image_url[0]+f")", url="https://splitticai.net")
        req = await AsyncClient.get(image_url[0])
        with open(timex+".png","wb") as f:
            f.write(req.content)
        embed1.set_image(url=image_url[0])
        embed1.set_footer(text='Powered by SplGen '+model)
        try:
            if noDelay == False:
                await asyncio.sleep(60)
            msg = await interaction.followup.send(content="",embeds = [embed1])
        except:
            pass
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await msg.add_reaction("❤️‍🔥")
        resp = await AsyncClient.get(f"https://wuemeli.com/auth/gallery/create?secret=bananenuwu123&picture_url={image_url[0]}&prompt={oprompt}&userId={interaction.user.id}")
        msg2 = await msg.reply(str(interaction.user.mention))
        await asyncio.sleep(3)
        await msg2.delete()
    except Exception as es:
        await interaction.user.send(str(es))

@client.tree.command(name = "ven", description = "Task automation AI")
@app_commands.choices(task=[
    app_commands.Choice(name="Set Timer", value="Set Timer"),
    app_commands.Choice(name="Random Generator", value="Random Generator"),
])
async def ven_command(interaction, task:str):
    """Task automation AI

    Parameters
    ----------
    task : str
        The task to automate"""
    if task == "Set Timer":
        class venTimerModal(ui.Modal, title="Set Timer"):
            remainingTime = ui.TextInput(label="Remaining time in minutes", placeholder="30", style=discord.TextStyle.short, min_length = 1, max_length= 2)
            message = ui.TextInput(label="Message", placeholder="Your timer ran out", style=discord.TextStyle.long, required = False, max_length=1500)
            async def on_submit(self, interaction: discord.Interaction):
                try:
                    links = re.compile(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*", re.MULTILINE|re.UNICODE)
                    if links.search(self.message.value):
                        await interaction.response.send_message("We do not accept links in message.", ephemeral=True)
                    elif int(self.remainingTime.value) >= 30 or int(self.remainingTime.value) <1:
                        await interaction.response.send_message("We only accept remaining time input between 1 minute and 30 minutes.", ephemeral=True)
                    else:
                        await interaction.response.send_message("Your timer has been set.", ephemeral=True)
                        await asyncio.sleep(int(self.remainingTime.value)*60)
                        if self.message and self.message.value != "":
                            await interaction.channel.send(self.message.value + "\nTimer by <@"+str(interaction.user.id)+"> using /ven")
                        else:
                            await interaction.channel.send("<@"+str(interaction.user.id)+">, your timer ran out.")
                except:
                    await interaction.response.send_message("We only accept remaining time input as integer.", ephemeral=True)
        await interaction.response.send_modal(venTimerModal())
    if task == "Random Generator":
        try:
            await interaction.response.defer()
            options = [
                discord.SelectOption(label="Random Names", value="Random Names"),
                discord.SelectOption(label="Random Bible Verses", value="Random Bible Verses"),
                discord.SelectOption(label="Random Words", value="Random Words"),
            ]
            class RandomView(ui.View):
                def __init__(self,timeout=9999):
                    super().__init__(timeout=timeout)
                @ui.select(
                    cls=ui.Select,
                    placeholder="What to generate?",
                    options=options)
                async def select(self, interaction:discord.Interaction, select:ui.Select):
                    await interaction.response.defer()
                    try:
                        selected_option = select.values[0]
                        if selected_option == "Random Bible Verses":
                            data = {
                                'quantity': '1',
                                'X-Requested-With': 'XMLHttpRequest',
                            }
                            resp = await AsyncClient.post("https://api.corsme.com/?https://randommer.io/random-bible-verse", data=data)
                            return await interaction.message.edit(content="Your Random Bible Verse: "+resp.json()[0]["verse"], view=None)
                        if selected_option == "Random Names":
                            data = {
                                'type': 'full name',
                                'number': '1',
                                'X-Requested-With': 'XMLHttpRequest',
                            }
                            resp = await AsyncClient.post("https://api.corsme.com/?https://randommer.io/Name", data=data)
                            return await interaction.message.edit(content="Your Random Name: "+resp.json()[0], view=None)
                        if selected_option == "Random Words":
                            data = {
                                'quantity': '1',
                                'wordType': str(random.randint(0, 5)),
                                'X-Requested-With': 'XMLHttpRequest',
                            }
                            resp = await AsyncClient.post("https://api.corsme.com/?https://randommer.io/word-generator", data=data)
                            return await interaction.message.edit(content="Your Random Word: "+resp.json()[0], view=None)
                    except Exception as es:
                        await interaction.user.send(str(es))
            msg = await interaction.followup.send(view=RandomView())
        except Exception as es:
            await interaction.user.send(str(es))
                
    

@client.tree.command(name = "edit", description = "Edit an Image")
@app_commands.choices(model=[
    app_commands.Choice(name="SplEdit v2", value="latest"),
])
async def edit_command(interaction, image_url:str, prompt:str, model:str="latest"):
    """Edit an Image
    
    Parameters
    ----------
    image_url : str
        The url of the image to edit
    prompt : str
        The prompt to edit the image
    model : str
        The model to use"""
    global current_session_index, cookies
    try:
        oprompt = prompt
        msg = await interaction.response.defer()
        #await interaction.followup.send("Disabled for now, coming back soon")
        if not interaction.user.id in userDailyLimits or interaction.user.id in [1001822685791269005, 270262006827712514, 266232329557639168]:
            userDailyLimits[interaction.user.id] = 0
        userDailyLimits[interaction.user.id] += 1
        limit = 25
        for guild in client.guilds:
                for member in guild.members:
                    if member.id == interaction.user.id:
                        for role in member.roles:
                            if role.id == 1135552096905732206 or role.id==1136599915997450261:
                                limit = 100

        if userDailyLimits[interaction.user.id] > limit:
            remaining_time = get_remaining_time()
            embed = discord.Embed(title="You already reached the daily limit of " + str(limit) + " images.", description = "Try again in " + remaining_time + ".\nTo increase this, either boost [our Discord server](https://discord.gg/9zAy8NgyQz) or donate to [Daniel Klimmer on PayPal](https://paypal.me/thefiredragon05) and dm [@splittic](https://discord.com/users/1064553604003942430) afterwards")
            await interaction.followup.send(ephemeral=True, embed = embed)
            if userDailyLimits[interaction.user.id] == limit+1:
                await asyncio.sleep(get_time_until_end_of_day())
                userDaily
            return
        if interaction.guild:
            if not interaction.guild.id in serverDailyLimits:
                serverDailyLimits[interaction.guild.id] = 0
            serverDailyLimits[interaction.guild.id] += 1
            serverlimit = 500
            if interaction.guild.id == 1130039507379568782:
                serverlimit = 10000

            if serverDailyLimits[interaction.guild.id] > serverlimit:
                remaining_time = get_remaining_time()
                await interaction.followup.send(ephemeral=True, content="Your server reached the daily limit of " + str(serverlimit) + " images. Try again in " + remaining_time + ".")
                if serverDailyLimits[interaction.server.id] == limit+1:
                    await asyncio.sleep(get_time_until_end_of_day())
                    serverDailyLimits[interaction.guild.id] = 0
                return
        current_session = image_sessions[current_session_index]
        cookies = {
            '__Secure-next-auth.session-token': current_session,
        }
        headers = {
            'authority': 'playgroundai.com',
            'user-agent': image_sessions_user_agents[current_session],
            "X-Forwarded-For": "163.169.1.100",
        }
        try:
          bs64, width, height = await get_image_as_base64x(image_url)
        except:
          return await interaction.followup.send("Please provide a valid image url")
        json_data = {
            'width': width,
            'height': height,
            'seed': random.randint(1000000,9999999),
            'num_images': 1,
            'sampler': 3,
            'cfg_scale': 7,
            'guidance_scale': 7,
            'strength': 1.3,
            'steps': 150,
            'mode': 2,
            'prompt': prompt,
            'start_schedule': 0.7,
            'init_image': bs64,
            'mask_strength': 0.7,
            'hide': True,
            'isPrivate': False,
            'modelType': 'stable-diffusion',
            'batchId': '54YNnGiQrZ',
            'generateVariants': False,
            'initImageFromPlayground': False,
        }
        AsyncClient2 = httpx.AsyncClient()
        response = await AsyncClient2.post('https://api.corsme.com/?https://playgroundai.com/api/models', cookies=cookies,json=json_data, headers=headers, timeout =999)
        try:
            if str(response.json()) == "{'error': 'Not authenticated'}":
                current_session_index = current_session_index + 1 if current_session_index != len(image_sessions) else 0
                return await interaction.followup.send(content="Please tell [@splittic](https://discord.com/users/1064553604003942430) that the VM with the ID "+current_session.split("-")[0]+ " crashed.")
            image_url = ['https://storage.googleapis.com/pai-images/' + response.json()["images"][0]["imageKey"]+'.png']
        except:
            if response.json()['errorCode'] == 'SAFETY_FILTER':
                await interaction.followup.send(content='We blocked the output as it is not safe for work')
                return
            else:
                if interaction.guild and interaction.guild.id != 1130039507379568782:
                    await interaction.followup.send(content='To save CPU and money, we limited all daily generations to '+str(len(splai_image_sessions))+'000 for now.\nTo increase this, donate to [Daniel Klimmer on PayPal](https://paypal.me/thefiredragon05) and dm [@splittic](https://discord.com/users/1064553604003942430) afterwards')
                    current_session_index = current_session_index + 1 if current_session_index != len(image_sessions) else 0
                elif interaction.guild:
                    await interaction.followup.send(content='To save CPU and money, we limited daily generations in this server to 10000.\nAdd it to your server for more.')
                    current_session_index = current_session_index + 1 if current_session_index != len(image_sessions) else 0
                else:
                    await interaction.followup.send(content='To save CPU and money, we limited all daily generations to '+str(len(splai_image_sessions))+'000 for now.\nTo increase this, donate to [Daniel Klimmer on PayPal](https://paypal.me/thefiredragon05) and dm [@splittic](https://discord.com/users/1064553604003942430) afterwards')
                    current_session_index = current_session_index + 1 if current_session_index != len(image_sessions) else 0

                return
        #embed1=discord.Embed(title='Your images are ready.', description=f"[Open Image 1 in {width}p/{height}p]("+image_url[0]+f")\n[Open Image 2 in {width}p/{height}p]("+image_url[1]+f")\n[Open Image 3 in {width}p/{height}p]("+image_url[2]+f")\n[Open Image 4 in {width}p/{height}p]("+image_url[3]+")", url="https://google.com")
        embed1=discord.Embed(title='Your image is ready.', description=f"[Open Image in {width}p/{height}p]("+image_url[0]+f")", url="https://splitticai.net")
        req = await AsyncClient.get(image_url[0])
        timex = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        with open(timex+".png","wb") as f:
            f.write(req.content)
        embed1.set_image(url=image_url[0])
        embed1.set_footer(text='Powered by SplEdit v2')
        try:
            msg = await interaction.followup.send(content="",embeds = [embed1])
        except:
            pass
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await msg.add_reaction("❤️‍🔥")
        msg2 = await msg.reply(str(interaction.user.mention))
        await asyncio.sleep(3)
        await msg2.delete()
    except Exception as es:
        await interaction.user.send(str(es))

@client.tree.command(name="detect", description="Detect a song")
async def detect(interaction, attachment:discord.Attachment):
    """Detect a song

    Parameters
    ----------
    attachment : discord.Attachment
        The file of the song to detect."""
    try:
        await interaction.response.defer()
        filename = attachment.filename
        
        # Check if the attachment has an audio extension (you can customize the list of audio extensions)
        audio_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac', '.wma', '.aiff', '.ape', '.au',
    '.ra', '.mid', '.amr', '.ac3', '.opus', '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m2ts', '.ts', '.3gp',
    '.rmvb', '.divx', '.ogv', '.mpeg', '.vob']
        if any(filename.lower().endswith(ext) for ext in audio_extensions):
            shazam = Shazam()
            file = await attachment.read()  # Read the file content
            
            # Save the file locally
            with open(filename, 'wb') as f:
                f.write(file)
            
            out = await shazam.recognize_song(filename)  # Pass the filename to recognize_song
            
            if len(out["matches"]) != 0:
                track = out["track"]
                title = track["title"] + " by " + track["subtitle"]
                cover_art = track["images"]["coverart"]
                
                embed = discord.Embed(title=title, color=0x00ff00)
                embed.set_thumbnail(url=cover_art)
                
                try:
                    related_songs = await shazam.related_tracks(track_id=track["key"], limit=5, offset=2)
                    related_songs_string = "\n".join([f"> {x['title']} by {x['subtitle']}" for x in related_songs["tracks"]])
                    embed.add_field(name="Related Songs:", value=related_songs_string)
                except:
                    pass
                
                msg = await interaction.followup.send(embed=embed)
                await msg.add_reaction("👍")
                await msg.add_reaction("👎")
                # Remove the file after processing
                os.remove(filename)
            else:
                await interaction.followup.send("No song detected")
                os.remove(filename)
        else:
            await interaction.followup.send("The attached file is not an audio file.")
    except Exception as es:
        if interaction.user.id == 1145676460225478686:
            await interaction.user.send(str(es))

async def get_image_as_base64x(url):
    try:
        response = await AsyncClient.get(url)
        if response.status_code == 200:
            image_data = response.content
            img = Image.open(BytesIO(image_data))
            resized_image_data = BytesIO()
            img.save(resized_image_data, format="PNG")
            resized_image_data = resized_image_data.getvalue()
            base64_image = base64.b64encode(resized_image_data).decode('utf-8')
            data_uri = f"data:image/png;base64,{base64_image}"
            width, height = img.size
            return data_uri, width, height
        else:
            print(f"Failed to fetch image from URL. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

@client.tree.command(name = "say", description = "Use our text to speech model")
@app_commands.choices(voice=[
    app_commands.Choice(name="Default Male", value="dm"),
    app_commands.Choice(name="Default Female", value="df"),
    app_commands.Choice(name="Male 2", value="m2"),
    app_commands.Choice(name="Female 2", value="f2")
])
async def let_me_say(interaction, text:str, voice:str):
        """Use our text to speech model

        Parameters
        ----------
        text : str
            What to say
        voice : str
            Which voice to use"""
        if voice == "dm": voice = "Clyde"
        if voice == "df": voice = "Emily"
        if voice == "m2": voice = "Dave"
        if voice == "f2": voice = "Dorothy"
        await interaction.response.defer()
        try:
            voice_link = await tts(text, voice)
        except Exception as es:
            print(es)
        response = await AsyncClient.get("https://api.corsme.com/?"+voice_link)
        with open('talk.mp3', 'wb') as f:
            f.write(response.content)
        file = discord.File("talk.mp3", datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".mp3")
        msg = await interaction.followup.send("Powered by SplTalk v3",file=file)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await msg.add_reaction("❤️‍🔥")

@client.tree.command(name="obj", description="Showcase an object")
async def remake_command(interaction, image_url: str):
    """Showcase an object

        Parameters
        ----------
        image_url : str
            The image including the object"""
    await interaction.response.defer()
    msg = await interaction.followup.send("Generating, please be patient...")
    try:
        await remake(image_url)
    except Exception as e:
        await interaction.followup.send(f"This image can't be used, sry")
        return
    try:
        embeds = []
        files = []
        for n in range(2,10):
            output_name="output"+str(n)+".png"
            with open(output_name, 'rb') as f:
                file = discord.File(f, filename=datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".png")
                files.append(file)
                embed= discord.Embed(title="Here you go:", url=image_url)
                embed.description="Click [here]("+image_url+") to view original image."
                embed.set_footer(text="Powered by SplRotate")
                embed.set_image(url="attachment://"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".png")
                embeds.append(embed)
        await msg.edit(content="",attachments=files, embeds=embeds)
    except Exception as es:
        print(es)
        
@client.tree.command(name = "imagine_text", description = "Imagine an Image with text")
@app_commands.choices(style=[
    app_commands.Choice(name="Default", value="photo"),
    app_commands.Choice(name="Comic", value="Comic"),
    app_commands.Choice(name="Pixar", value="pixar"),
    app_commands.Choice(name="Steampunk", value="steampunk"),
    app_commands.Choice(name="Oilpainting", value="oilpainting"),
])
@app_commands.choices(size_format=[
    app_commands.Choice(name="Square", value="square"),
    app_commands.Choice(name="Portait Mode", value="portrait"),
    app_commands.Choice(name="Landscape Mode", value="landscape")
])
async def imagine_text_command(interaction, prompt:str, style:str, size_format:str, creative:bool):
    try:
        """Imagine an Image with text

        Parameters
        ----------
        prompt : str
            The prompt to make the image
        style : str
            The style for the image
        size_format : str
            The format of the image
        creative : str
            Shall be creative or not?"""
        msg = await interaction.response.defer()
        #await interaction.followup.send("Disabled for now, coming back soon")
        if not interaction.user.id in userDailyLimits or interaction.user.id in [1001822685791269005, 270262006827712514, 266232329557639168]:
            userDailyLimits[interaction.user.id] = 0
        userDailyLimits[interaction.user.id] += 1
        limit = 25
        for guild in client.guilds:
                for member in guild.members:
                    if member.id == interaction.user.id:
                        for role in member.roles:
                            if role.id == 1135552096905732206 or role.id==1136599915997450261:
                                limit = 100

        if userDailyLimits[interaction.user.id] > limit:
            remaining_time = get_remaining_time()
            embed = discord.Embed(title="You already reached the daily limit of " + str(limit) + " images.", description = "Try again in " + remaining_time + ".\nTo increase this, either boost [our Discord server](https://discord.gg/9zAy8NgyQz) or donate to [Daniel Klimmer on PayPal](https://paypal.me/thefiredragon05) and dm [@splittic](https://discord.com/users/1064553604003942430) afterwards")
            await interaction.followup.send(ephemeral=True, embed = embed)
            if userDailyLimits[interaction.user.id] == limit+1:
                await asyncio.sleep(get_time_until_end_of_day())
                userDaily
            return
        if interaction.guild:
            if not interaction.guild.id in serverDailyLimits:
                serverDailyLimits[interaction.guild.id] = 0
            serverDailyLimits[interaction.guild.id] += 1
            serverlimit = 500
            if interaction.guild.id == 1130039507379568782:
                serverlimit = 10000

            if serverDailyLimits[interaction.guild.id] > serverlimit:
                remaining_time = get_remaining_time()
                await interaction.followup.send(ephemeral=True, content="Your server reached the daily limit of " + str(serverlimit) + " images. Try again in " + remaining_time + ".")
                if serverDailyLimits[interaction.server.id] == limit+1:
                    await asyncio.sleep(get_time_until_end_of_day())
                    serverDailyLimits[interaction.guild.id] = 0
                return
        try:
            if not creative:
                image_url = await textgen(prompt, size_format, style, "raw")
            else:
                image_url = await textgen(prompt, size_format, style, "fun")
        except Exception as es:
            print(es)
            return await interaction.followup.send("We blocked NSFW")
        try:
            response = await AsyncClient.get("https://api.corsme.com/?"+image_url)
            with open('image_text.jpeg', 'wb') as f:
                f.write(response.content)
            file = discord.File("image_text.jpeg", datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".jpeg")
            embed = discord.Embed(title="Your image is ready")
            embed.set_image(url="attachment://"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".jpeg")
            embed.set_footer(text="Powered by SplText v5", icon_url="https://media.discordapp.net/attachments/1072968236519411804/1145740792330211348/a_photo_of_a_baseball_cap_with_yellow_text_on_it_that_says_Spltext.png")
            msg = await interaction.followup.send(file=file, embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
            await msg.add_reaction("❤️‍🔥")
        except Exception as es:
            print(es)
            await interaction.followup.send("Something failed, sry")
    except Exception as es:
        if interaction.user.id == 1145676460225478686:
            await interaction.user.send(str(es))


    

async def run_ask(interaction, prompt):
    perplexity_cli = await perplexity.Client(perplexity_headers, perplexity_cookies)
    await asyncio.sleep(1)
    mode, result = await perplexity_cli.search(prompt, mode='concise', focus='internet')
    if mode == "embed":
        await interaction.followup.send(embed=result)
    if mode == "text":
        await interaction.followup.send(result)
    if mode == "file":
        await interaction.followup.send(file=result)

async def run_askyoutube(interaction, prompt):
    perplexity_cli = await perplexity.Client(perplexity_headers, perplexity_cookies)
    await asyncio.sleep(1)
    mode, result = await perplexity_cli.searchyoutube(prompt, mode='concise', focus='youtube')
    if mode == "embed":
        await interaction.followup.send(embed=result)
    if mode == "text":
        await interaction.followup.send(result)
    if mode == "file":
        await interaction.followup.send(file=result)

async def run_translate(interaction, language, text):
    perplexity_cli = await perplexity.Client(perplexity_headers, perplexity_cookies)
    await asyncio.sleep(1)
    result = await perplexity_cli.translate(language, text)
    await interaction.followup.send("Translated: "+result.replace('"','')+"\n\nPówered by SplTranslate v2")

async def run_find_solution(interaction, problem):
    msg = await interaction.followup.send("SplFind is looking at your problem, please wait.")
    perplexity_cli = await perplexity.Client(perplexity_headers, perplexity_cookies)
    await asyncio.sleep(1)
    result = await perplexity_cli.find(problem)
    await asyncio.sleep(random.randint(30,150))
    character_limit = 2000

    if len(result) > character_limit:
        with open("solution.txt", "w", encoding="utf-8") as file:
            file.write(result)
        await msg.edit(attachments=[discord.File("solution.txt")], content="## Solution provided by SplFind\n\nCheck solution.txt")
    else:
        await msg.edit(content="## Solution provided by SplFind\n\n"+result)
    await msg.reply("<@"+str(interaction.user.id)+">")

async def dm_response(message, prompt):
    if not message.author.id in chatbot_chats:
        chatbot_chats[message.author.id] = []
    chatbot_chat = chatbot_chats[message.author.id]
    async with message.channel.typing():
        perp_cli = ai_dm.Client(perplexity_headers, perplexity_cookies)
        await asyncio.sleep(1)
        result = await perp_cli.reply(prompt, conversation = chatbot_chat)
        await asyncio.sleep(len(result) / 64)
        if result.startswith(": "):
            result = result[2:]
        result = re.sub(r'\[\d+\]', '', result)
        chatbot_chat.append({"name": "User", "message": prompt})
        chatbot_chat.append({"name": "Splittic", "message": result})
        if message.channel.id == 1139263457661812768:
            await message.reply(result, allowed_mentions = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True))
        else:
            await message.channel.send(result)
    if len(chatbot_chat) > 20:
        chatbot_chat.pop(0)
    chatbot_chats[message.author.id] = chatbot_chat

@client.event
async def on_message(message):
    if (message.guild and message.channel.id != 1139263457661812768 and not "spl-chat" in message.channel.name) or message.author.bot:
        return
    prompt = message.content
    await dm_response(message, prompt)
    
    
    

@client.tree.command(name = "ask", description = "Ask me something")
async def ask(interaction, *, prompt:str):
    """Ask me something
    
    Parameters
    ----------
    prompt : str
        The question"""
    await interaction.response.defer()
    try:
        await asyncio.create_task(run_ask(interaction, prompt))
    except Exception as es:
        if interaction.user.id == 1145676460225478686:
            await interaction.user.send(str(es))

@client.tree.command(name = "askyoutube", description = "Ask YouTube something")
async def askyoutube(interaction, *, prompt:str):
    """Ask YouTube something
    
    Parameters
    ----------
    prompt : str
        The question"""
    await interaction.response.defer()
    try:
        await asyncio.create_task(run_askyoutube(interaction, prompt))
    except Exception as es:
        if interaction.user.id == 1145676460225478686:
            await interaction.user.send(str(es))
    
@client.tree.command(name = "translate", description = "Let me translate something")
async def translate(interaction, language:str, text:str):
    """Let me translate something
    
    Parameters
    ----------
    language : str
        The language to translate to
    text : str
        The text to translate"""
    try:
        await interaction.response.defer()
        await asyncio.create_task(run_translate(interaction, language, text))
    except Exception as es:
        print(es)

@client.tree.command(name = "find_solution", description = "The AI doctor, scientologist and biologist")
async def find_solution(interaction, problem:str):
    """The AI doctor, scientologist and biologist
    
    Parameters
    ----------
    problem : str
        The problem to find a solution to."""
    try:
        await interaction.response.defer()
        await asyncio.create_task(run_find_solution(interaction, problem))
    except Exception as es:
        await interaction.user.send("Your SplFind request failed, sry")
        print(es)
    
@client.tree.command(name = "describe", description = "Ask me what I see on an image")
async def detect_image_and_describe(interaction, *, prompt:str):
    """Ask me what I see on an image
    
    Parameters
    ----------
    prompt : str
        The prompt"""
    await interaction.response.defer()
    if not interaction.user.id in userDailyLimits or interaction.user.id in [1001822685791269005, 270262006827712514, 266232329557639168]:
        userDailyLimits[interaction.user.id] = 0
    userDailyLimits[interaction.user.id] += 1
    limit = 25
    for guild in client.guilds:
            for member in guild.members:
                if member.id == interaction.user.id:
                    for role in member.roles:
                        if role.id == 1135552096905732206 or role.id==1136599915997450261:
                            limit = 100

    if userDailyLimits[interaction.user.id] > limit:
        remaining_time = get_remaining_time()
        embed = discord.Embed(title="You already reached the daily limit of " + str(limit) + " images.", description = "Try again in " + remaining_time + ".\nTo increase this, either boost [our Discord server](https://discord.gg/9zAy8NgyQz) or donate to [Daniel Klimmer on PayPal](https://paypal.me/thefiredragon05) and dm [@splittic](https://discord.com/users/1064553604003942430) afterwards")
        await interaction.followup.send(ephemeral=True, embed = True)
        if userDailyLimits[interaction.user.id] == limit+1:
            await asyncio.sleep(get_time_until_end_of_day())
            userDailyLimits[interaction.user.id] = 0
    if interaction.guild:
        if not interaction.guild.id in serverDailyLimits:
            serverDailyLimits[interaction.guild.id] = 0
        serverDailyLimits[interaction.guild.id] += 1
        serverlimit = 500
        if interaction.guild.id == 1130039507379568782:
            serverlimit = 10000

        if serverDailyLimits[interaction.guild.id] > serverlimit:
            remaining_time = get_remaining_time()
            await interaction.followup.send(ephemeral=True, content="Your server reached the daily limit of " + str(serverlimit) + " images. Try again in " + remaining_time + ".")
            if serverDailyLimits[interaction.server.id] == limit+1:
                await asyncio.sleep(get_time_until_end_of_day())
                serverDailyLimits[interaction.guild.id] = 0
            return
    try:
        result = await describe(prompt)
    except:
        return await interaction.followup.send("Try again please.")
    embed = discord.Embed()
    embed.url = "https://google.com"
    embed.description=result
    embed.color=0xFFFFFF
    embed.set_footer(text="Powered by SplDetect V3")
    extract_first_url = lambda text: re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text) if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text) else None
    urls = extract_first_url(prompt)
    if not urls:
        return await interaction.followup.send("No images to desscribe?")
    if len(urls) !=0:
        embed.set_image(url=urls[0])
    embeds = [embed]
    for url in range(1, len(urls)):
        try:
            if extract_first_url(url):
                embeds.append(discord.Embed(url="https://google.com"))
                embeds[len(embeds)-1].set_image(url = url)
        except:
            pass
        
    try:
        await interaction.followup.send(embeds=embeds)
    except:
        await interaction.followup.send(embed= embeds[0])

@client.tree.command(name="beat", description="Let me make a beat")
async def beat_gen(interaction, prompt: str):
    """Let me make a beat

    Parameters
    ----------
    prompt : str
        What the beat shall be"""
    original_prompt = prompt
    prompt += " - pitch"
    await interaction.response.defer()
    msg = await interaction.followup.send("I'll ping you when done")
    output_file_path = "beat.mp3"
    response = await AsyncClient.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp', params={'key': 'AIzaSyDqSq0-SitTYDsJgIBOsbguUUafOq5xXXU'})
    headers = {
        'authorization': 'Bearer '+response.json()["idToken"],
    }

    json_data = {
        'prompt': prompt,
        'type': 'text2SongPrepare',
    }
    response = await AsyncClient.post('https://api.corsme.com/?https://v0-c6s4bjzoiq-uc.a.run.app/action', headers=headers, json=json_data,timeout=999)
    
    json_data = {
        'songId': response.json()["id"],
        'type': 'text2SongFinalise',
    }
    
    response = await AsyncClient.post('https://api.corsme.com/?https://v0-c6s4bjzoiq-uc.a.run.app/action', headers=headers, json=json_data,timeout=999)
    songUrl = response.json()["trackUrl"]
    responsex = await AsyncClient.get(songUrl, timeout=99)
    with open(output_file_path, 'wb') as songFile:
        songFile.write(responsex.content)
    msg = await interaction.followup.send("Here is your beat:", file = discord.File("beat.mp3"))
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("❤️‍🔥")

@client.tree.command(name="sing", description="Let me sing a song for you")
async def sing_a_song(interaction, prompt: str):
    """Let me sing a song for you

    Parameters
    ----------
    prompt : str
        What the song shall be"""
    original_prompt = prompt
    prompt += " - pitch"
    try:
        await interaction.response.defer()
    except:
        pass
    try:
        lyrics = ""
        msg = await interaction.followup.send("I'll ping you when done")
        output_file_path = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".mp3"
        response = await AsyncClient.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp', params={'key': 'AIzaSyDqSq0-SitTYDsJgIBOsbguUUafOq5xXXU'})
        headers = {
            'authorization': 'Bearer '+response.json()["idToken"],
        }

        json_data = {
            'prompt': prompt,
            'type': 'text2SongPrepare',
        }
        response = await AsyncClient.post('https://api.corsme.com/?https://v0-c6s4bjzoiq-uc.a.run.app/action', headers=headers, json=json_data,timeout=999)
        
        json_data = {
            'songId': response.json()["id"],
            'type': 'text2SongFinalise',
        }
        
        # response = await AsyncClient.post('https://api.corsme.com/?https://v0-c6s4bjzoiq-uc.a.run.app/action', headers=headers, json=json_data,timeout=999)
        # json_data = {
        #     'songId': response.json()["id"],
        #     'lyrics': lyrics,
        #     'type': 'text2SongEdit',
        # }
        
        response = await AsyncClient.post('https://api.corsme.com/?https://v0-c6s4bjzoiq-uc.a.run.app/action', headers=headers, json=json_data,timeout=999)
        songUrl = response.json()["songUrl"]
        responsex = await AsyncClient.get(songUrl, timeout=99)
        with open(output_file_path, 'wb') as songFile:
            songFile.write(responsex.content)
    except Exception as es:
        await interaction.user.send(str(es))
        return
    try:
        class EditButton(ui.Button):
            def __init__(self, songId):
                super().__init__(label="Edit Lyrics", emoji="🖊️")
                self.songId = songId
        
            async def callback(self, interaction: discord.Interaction):
                class EditModal(ui.Modal, title="🖊️ Edit Lyrics 🖊️"):
                    lyrics = ui.TextInput(label="Enter Lyrics", placeholder="""We're no strangers to love.
You know the rules and so do I.""", style=discord.TextStyle.long)
                    def __init__(self, songId):
                        super().__init__(title="🖊️ Edit Lyrics 🖊️")
                        self.songId = songId
        
                    async def on_submit(self, interaction: discord.Interaction):
                        try:
                            await interaction.response.send_message("Editing Lyrics, please wait", ephemeral = True)
                            json_data = {
                                'songId': self.songId,
                                'lyrics': self.lyrics.value,
                                'type': 'text2SongEdit',
                            }
                            response = await AsyncClient.post('https://api.corsme.com/?https://v0-c6s4bjzoiq-uc.a.run.app/action', headers=headers, json=json_data, timeout=999)
                            songUrl = response.json()["songUrl"]
                            responsex = await AsyncClient.get(songUrl, timeout=99)
                            output_file_path = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".mp3"
                            with open(output_file_path, 'wb') as songFile:
                                songFile.write(responsex.content)
                            msg = await interaction.followup.send(content="Here are the new lyrics", file=discord.File(output_file_path))
                            os.remove(output_file_path)
                            await msg.add_reaction("👍")
                            await msg.add_reaction("👎")
                            await msg.add_reaction("❤️‍🔥")
                        except Exception as es:
                            await interaction.response.send_message(str(es))
                try:
                    await interaction.response.send_modal(EditModal(self.songId))
                except Exception as es:
                    if interaction.user.id == 1145676460225478686:
                        await interaction.user.send(str(es))
        class VoiceOnlyButton(ui.Button):
            def __init__(self, vocalsUrl):
                super().__init__(label="Extract Vocals", emoji="🎙️")
                self.vocalsUrl = vocalsUrl
            async def callback(self, interaction: discord.Interaction):
                await interaction.response.defer()
                response = await AsyncClient.get(self.vocalsUrl, timeout=99)
                with open("vocals.mp3", 'wb') as songFile:
                    songFile.write(response.content)
                await interaction.followup.send(content="Here are the extracted Vocals",file= discord.File("vocals.mp3"))
                
        class BeatOnlyButton(ui.Button):
            def __init__(self, trackUrl):
                super().__init__(label="Extract Beat", emoji="🔊")
                self.trackUrl = trackUrl
            async def callback(self, interaction: discord.Interaction):
                await interaction.response.defer()
                response = await AsyncClient.get(self.trackUrl, timeout=99)
                with open("beat.mp3", 'wb') as songFile:
                    songFile.write(response.content)
                await interaction.followup.send(content="Here is the extracted Beat",file= discord.File("beat.mp3"))
                
        class EditView(ui.View):
            timeout=None
            def __init__(self, songId, trackUrl, vocalsUrl):
                super().__init__()
                self.add_item(EditButton(songId))
                self.add_item(VoiceOnlyButton(vocalsUrl))
                self.add_item(BeatOnlyButton(trackUrl))
        msg = await msg.reply("Powered by SplSing v5 Beta:\n```" + original_prompt + "```\n<@" + str(interaction.user.id) + ">",
                             file=discord.File(output_file_path), view=EditView(response.json()["id"], response.json()["trackUrl"],response.json()["vocalsUrl"]))
    except Exception as es:
        await interaction.user.send(str(es))
        return
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("❤️‍🔥")


async def get_image_as_base64(url, target_size=(256, 256)):
    try:
        response = await AsyncClient.get(url)
        if response.status_code == 200:
            image_data = response.content
            img = Image.open(BytesIO(image_data))
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            resized_image_data = BytesIO()
            img.save(resized_image_data, format="PNG")
            resized_image_data = resized_image_data.getvalue()
            base64_image = base64.b64encode(resized_image_data).decode('utf-8')
            data_uri = f"data:image/png;base64,{base64_image}"
            return data_uri
        else:
            print(f"Failed to fetch image from URL. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def save_base64_to_png(base64_data, output_file_path):
    try:
        base64_data = base64_data.split(',', 1)[1]
        image_data = base64.b64decode(base64_data)
        with open(output_file_path, 'wb') as image_file:
            image_file.write(image_data)
        print(f"Image saved as {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

@client.tree.command(name="vid", description="Generate a video from text")
async def vid_command(interaction, prompt:str):
    """Generate a video from text

    Parameters
    ----------
    prompt : str
        The prompt for the video"""
    await interaction.response.defer()
    msg = await interaction.followup.send("I'll ping you when done")
    output_file_path = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".webm"
    uri = "wss://api.aironheart.com/explore?model=text2video"
    try:
        async with websockets.connect(uri, ping_timeout=999, ping_interval=None, max_size=4096*4096) as websocket:
            x = json.loads(await websocket.recv())
            while x["msg"] != "send_data":
              x = json.loads(await websocket.recv())
            await websocket.send('{"data":["'+prompt+'"]}')
            while x["msg"] != "process_completed":
              x = json.loads(await websocket.recv())
            base64_data = x["output"]["data"][0]
            video_binary = base64.b64decode(base64_data)
            with open(output_file_path, "wb") as output_file:
              output_file.write(video_binary)
    except Exception as es:
        return await interaction.followup.send(str(es))
    try:
        msg = await msg.reply("Powered by SplVid:\n```"+prompt+"```\n<@"+str(interaction.user.id)+">", file = discord.File(output_file_path))
    except:
        pass
    os.remove(output_file_path)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("❤️‍🔥")

@client.tree.command(name="removebg", description="Remove the background from an image")
async def removebg_command(interaction, image_url:str):
    """Remove the background from an image

    Parameters
    ----------
    image_url : str
        Url of the image to remove background from"""
    headers = {"x-picsart-api-key": "UuWyHywlY4lFB9E1ymZk48oGz30bsgbr"}
    try:
        await interaction.response.defer()
        output_file_path = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".png"
        response = await AsyncClient.get(image_url)
        if response.status_code == 200:
            data = {
                'output_type': 'cutout',
            }
            files = {
                'image': ('image.jpg', response.content, 'image/jpeg')
            }
            response = await AsyncClient.post('https://api.corsme.com/?https://api.picsart.io/tools/1.0/removebg', headers=headers, data=data, files=files)
            image_response = await AsyncClient.get("https://api.corsme.com/?"+response.json()["data"]["url"])
            with open(output_file_path,"wb") as image_file:
                image_file.write(image_response.content)
        else:
            return await interaction.followup.send("Invalid image url, use another one please.")
        try:
            msg = await interaction.followup.send("Powered by SplBg v1:\n<@"+str(interaction.user.id)+">", file = discord.File(output_file_path))
        except:
            pass
        os.remove(output_file_path)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await msg.add_reaction("❤️‍🔥")
    except Exception as es:
        if interaction.user.id == 1145676460225478686:
            await interaction.user.send(str(es))

@client.tree.command(name="diff", description="Use our diffusion model (v2.1)")
async def diff_command(interaction, prompt:str, template_image_url:str=None):
    """Use our diffusion model (v2.1)

    Parameters
    ----------
    prompt : str
        The prompt for the image
    template_image_url : str
        A template image showing text already"""
    await interaction.response.defer()
    msg = await interaction.followup.send("I'll ping you when done")
    output_file_path = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".png"
    uri = "wss://jingyechen22-textdiffuser.hf.space/queue/join"
    try:
        async with websockets.connect(uri, ping_timeout=999, ping_interval=None, max_size = 4096*4096) as websocket:
          hash = str(random.randint(100000,999999))
          x = json.loads(await websocket.recv())
          if template_image_url:
            await websocket.send('{"fn_index": 3, "session_hash": "'+hash+'"}')
          else:
            await websocket.send('{"fn_index": 1, "session_hash": "'+hash+'"}')
          while x["msg"] != "send_data":
            x = json.loads(await websocket.recv())
          if template_image_url:
            bs64, width, height = await get_image_as_base64x(template_image_url)
            await websocket.send('{"data":["'+prompt.replace('"','\\"')+'", "'+bs64+'", 20, 7.5, 4, false, "Stable Diffusion v2.1"],"event_data":null,"fn_index":3,"session_hash":"'+hash+'"}')
          else:
            await websocket.send('{"data":["'+prompt.replace('"','\\"')+'",20,7.5,4,"Stable Diffusion v2.1"],"event_data":null,"fn_index":1,"session_hash":"'+hash+'"}')
          while x["msg"] != "process_completed":
            x = json.loads(await websocket.recv())
          save_base64_to_png(x["output"]["data"][0], output_file_path)
    except Exception as es:
        return await msg.reply(str(es))
    try:
        msg = await msg.reply("Powered by SD v2.1:\n```"+prompt+"```\n<@"+str(interaction.user.id)+">", file = discord.File(output_file_path))
    except:
        pass
    os.remove(output_file_path)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("❤️‍🔥")

@client.tree.command(name="outpaint", description="Paint outside an image")
async def outpaint_command(interaction, image_url:str):
    """Paint outside an image

    Parameters
    ----------
    image_url : str
        Url of the image to outpaint"""
    await interaction.response.defer()
    msg = await interaction.followup.send("I'll ping you when done")
    output_file_path = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".webm"
    uri = "wss://rothfeld-stable-diffusion-mat-outpainting-primer.hf.space/queue/join"
    try:
      async with websockets.connect(uri) as websocket:
        websocket.max_size= 4096 * 4096
        x = json.loads(await websocket.recv())
        print(x)
        while x["msg"] != "send_data":
          x = json.loads(await websocket.recv())
          print(x)
        try:
          bs64 = await get_image_as_base64(image_url)
        except:
          return await interaction.followup.send("Please give a valid image url")
        await websocket.send('{"data":["'+bs64+'",512,0,10,1,"places2+laion300k+laion1200k(opmasked)", false],"fn_index":0,"session_hash": "'+str(random.randint(1,99999999))+'"}')
        while x["msg"] != "process_completed":
          x = json.loads(await websocket.recv())
        save_base64_to_png(x["output"]["data"][0], "outpaint.png")
    except Exception as es:
        if 'data' in str(es):
          return await interaction.followup.send("Needa fix this, sry")
        return await interaction.followup.send(str(es))
    msg = await msg.reply("Powered by SplOutpaint:\n<@"+str(interaction.user.id)+">", file = discord.File("outpaint.png"))
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("❤️‍🔥")

@client.tree.command(name="sound", description="Generate a sound from text")
@app_commands.choices(length=[
    app_commands.Choice(name="1 Second", value=1),
    app_commands.Choice(name="2 Seconds", value=2),
    app_commands.Choice(name="5 Seconds", value=5),
    app_commands.Choice(name="10 Seconds", value=10),
    app_commands.Choice(name="15 Seconds", value=15),
])
async def sound_command(interaction, prompt:str, length:int):
    """Generate a sound from text

    Parameters
    ----------
    prompt : str
        What the sound shall be
    length : int
        The length of the sound"""
    try:
        await interaction.response.defer()
        msg = await interaction.followup.send("I'll ping you when done")
        output_file_path = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".mp3"
        uri = "wss://haoheliu-audioldm-48k-text-to-hifiaudio-generation.hf.space/queue/join"
        
        try:
            async with websockets.connect(uri, ping_timeout=999, ping_interval=999) as websocket:
                hash = str(random.randint(0,99999999))
                await websocket.recv()
                await websocket.send('{"fn_index":0,"session_hash":"'+hash+'"}')
                x = json.loads(await websocket.recv())
                while x["msg"] != "send_data":
                  x = json.loads(await websocket.recv())
                await websocket.send('{"data":["'+prompt+'",'+str(length)+',6,'+str(random.randint(1,999999999))+',5],"event_data":null,"fn_index":0,"session_hash":"'+hash+'"}')
                #await websocket.send('{"data":["'+prompt+'","'+negative_prompt+', Low Quality.",'+str(length)+',7,45,5],"event_data":null,"fn_index":1,"session_hash":"'+hash+'"}')
                while x["msg"] != "process_completed":
                  await asyncio.sleep(0)
                  x = json.loads(await websocket.recv())
                print(x)
                await asyncio.sleep(3)
                req = await AsyncClient.get("https://haoheliu-audioldm-48k-text-to-hifiaudio-generation.hf.space/file="+x["output"]["data"][0][0]["name"])
                video_binary = req.content
                with open(output_file_path, "wb") as output_file:
                  output_file.write(video_binary)
        except Exception as es:
             return await interaction.followup.send(str(es))
        msg = await msg.reply("Powered by SplSound v2:\n```"+prompt+"```\n<@"+str(interaction.user.id)+">", file = discord.File(output_file_path))
    except Exception as es:
        return await interaction.followup.send("Model currently offline, please try again later")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("❤️‍🔥")

@client.event
async def on_command_error(interaction, error):
    return

def restart_bot():
    # Replace current process with new instance of bot.py
    os.execl(sys.executable, sys.executable, "bot.py")

def check_verion() -> None:
    # Read the requirements.txt file and add each line to a list
    with open('requirements.txt') as f:
        required = f.read().splitlines()

    # For each library listed in requirements.txt, check if the corresponding version is installed
    for package in required:
        # Use the pkg_resources library to get information about the installed version of the library
        package_name, package_verion = package.split('==')
        installed = pkg_resources.get_distribution(package_name)
        # Extract the library name and version number
        name, version = installed.project_name, installed.version
        # Compare the version number to see if it matches the one in requirements.txt
        if package != f'{name}=={version}':
            logger.error(f'{name} version {version} is installed but does not match the requirements')
            sys.exit()

@bot.event
async def on_ready():
    try:
        bot_status = discord.Status.online
        bot_activity = discord.Activity(type=discord.ActivityType.playing, name = "/help")
        await bot.change_presence(status = bot_status, activity = bot_activity)
        for Filename in os.listdir('./cogs'):
            if Filename.endswith('.py'):
                await bot.load_extension(f'cogs.{Filename[:-3]}')
        logger.info(f'{bot.user} is now running!')
        print("Bot is Up and Ready!")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)

# Load command
@commands.is_owner()   
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.author.send(f'> **Loaded {extension} done.**')

# Unload command
@commands.is_owner()
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.author.send(f'> **Un-Loaded {extension} done.**')

# Empty discord_bot.log file
@commands.is_owner()
@bot.command()
async def clean(ctx):
    open('discord_bot.log', 'w').close()
    await ctx.author.send(f'> **Successfully emptied the file!**')

# Get discord_bot.log file
@commands.is_owner()
@bot.command()
async def getLog(ctx):
    try:
        with open('discord_bot.log', 'rb') as f:
            file = discord.File(f)
        await ctx.author.send(file=file)
        await ctx.author.send("> **Send successfully!**")
    except:
        await ctx.author.send("> **Send failed!**")

# Upload new Bing cookies and restart the bot
@commands.is_owner()
@bot.command()
async def upload(ctx):
    try:
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                if str(attachment)[-4:] == ".txt":
                    content = await attachment.read()
                    print(json.loads(content))
                    with open("cookies.json", "w", encoding = "utf-8") as f:
                        json.dump(json.loads(content), f, indent = 2)
                    if not isinstance(ctx.channel, discord.abc.PrivateChannel):
                        await ctx.message.delete()
                    await set_chatbot(json.loads(content))
                    await ctx.author.send(f'> **Upload new cookies successfully!**')
                    logger.warning("\x1b[31mCookies has been setup successfully\x1b[0m")
                else:
                    await ctx.author.send("> **Didn't get any txt file.**")
        else:
            await ctx.author.send("> **Didn't get any file.**")
    except Exception as e:
        await ctx.author.send(f">>> **Error: {e}**")
        logger.exception(f"Error while upload cookies: {e}")

@splmod.event
async def on_message(msg):
    if msg.author.bot:
        return
    try:
        perp_cli = await perplexity.Client(perplexity_headers, perplexity_cookies)
        await asyncio.sleep(1)
        await perp_cli.modcheck(msg)
    except Exception as es:
        await msg.author.send(str(es))

@splmod.event
async def on_message_edit(before, msg):
    if msg.author.bot:
        return
    try:
        perp_cli = await perplexity.Client(perplexity_headers, perplexity_cookies)
        await asyncio.sleep(1)
        await perp_cli.modcheck(msg)
    except Exception as es:
        await msg.author.send(str(es))


async def run_bots():
    await asyncio.gather(client.start(TOKEN), bot.start(TOKEN2), splmod.start(TOKEN3))

    
loop = asyncio.get_event_loop()
loop.run_until_complete(run_bots())
