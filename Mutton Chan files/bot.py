import os
from dotenv import load_dotenv
import discord
from discord import app_commands, Color
from discord.ext import commands, tasks
from itertools import cycle
import random
import myStory
import requests
import json
import tracemalloc
from datetime import datetime
import asyncio

load_dotenv()

TOKEN = os.environ.get("DISCORD_TOKEN")
GOOGLE = os.environ.get('GOOGLE_API_KEY')
SEARCH = os.environ.get('CUSTOM_SEARCH_ENGINE_ID')

# Initialize tracemalloc
tracemalloc.start()

# Periodically check memory usage
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 10**6} MB, Peak memory usage: {peak / 10**6} MB")
print("Module Name: {}".format(__name__))

#starting bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
#bot status on discord
bot_status = cycle(["myself", "/help", "other people(?)", "the Matrix"])

class Menu(discord.ui.View):
    def _init_(self):
        super()._init_()
        self.value = None

    @discord.ui.button(label="Utility🔧", style=discord.ButtonStyle.blurple)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color = discord.Color.random())
        embed.set_author(name=f"Utility🔧")
        embed.add_field(name="/help", value="Lists all the commands available!", inline=False)
        embed.add_field(name="/poll", value="Sets up a poll for your server. (will discontinue soon)", inline=False)
        embed.add_field(name="/status", value="Bot Status.", inline=False)
        embed.add_field(name="/purge", value="Deletes an amount of messages as specified by user.", inline=False)
        embed.add_field(name = "/blacklist", value="Blacklists a word on the server", inline=False)
        embed.add_field(name = "/unblacklist", value="Unblacklists a blacklisted word on the server", inline=False)
        embed.add_field(name="/set_welcome", value="Sets welcome message for your server!", inline=False)
        embed.add_field(name="/unset_welcome", value="Removes welcome message for your server.", inline=False)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Fun👀", style=discord.ButtonStyle.blurple)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color = discord.Color.random())
        embed.set_author(name=f"Fun👀")
        embed.add_field(name="/coinflip", value="Flips a coin!", inline=False)
        embed.add_field(name="/rockpaperscissors", value="Fight Mutton-Chan in a game of Rock Papers Scissors!", inline=False)
        embed.add_field(name="/statcreator", value="What would your character stats be?", inline=False)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Cool Commands😎", style=discord.ButtonStyle.blurple)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color = discord.Color.random())
        embed.set_author(name=f"Cool Commands😎")
        embed.add_field(name="/hello", value="Mutton-Chan says hello.", inline=False)
        embed.add_field(name="/imagesearch", value="Searches an image from the Internet", inline=False)
        embed.add_field(name="/newyearsalert", value="Countdown to New Years", inline=False)
        embed.add_field(name="/prompt", value="Mutton-Chan would like to tell you a story!", inline=False)
        embed.add_field(name="/avatar", value="Returns the image of another user's (or your own) avatar!", inline=False)
        await interaction.response.edit_message(embed=embed)

# displays an embed with a list of commands
@tree.command(name = "help", description = "list of commands")
async def menu(interaction: discord.Interaction):
    view = Menu()
    view.add_item(discord.ui.Button(label="GitHub", style=discord.ButtonStyle.link, url="https://github.com/Mutton9558", emoji="<a:4601_github:1184120254591406100>"))
    await interaction.response.send_message(view=view)

#loop status
@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

#when user uses /hello
@tree.command(name = "hello", description = "the bot greets back",)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("lmao die")

#check ping
@tree.command(name = "status", description = "Check bot status",)
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency*1000)
    emb = discord.Embed(title="Bot Status", description ="", color = discord.Color.random())

    emb.set_author(name=f"Requested by @{interaction.user.name}", icon_url=interaction.user.avatar)
    emb.set_thumbnail(url = interaction.guild.icon)
    emb.add_field(name="Ping: ", value=(f"{bot_latency} ms."), inline=False)
    emb.add_field(name="Memory Usage: ", value=(f"Current memory usage: {current / 10**6} MB, Peak memory usage: {peak / 10**6} MB"), inline=False)
    emb.set_footer(text = "bro finna dox me.")
    await interaction.response.send_message(embed = emb)

# New Years Countdown Command
@tree.command(name="newyearsalert", description = "See how long it is till new years!")
async def ny(interaction: discord.Interaction):
    dateinitial = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    dateinitial = dateinitial.split("-")
    # new year date
    newyeardate = datetime(int(dateinitial[0]) + 1, 1, 1,0,0,0)
    #current date
    dateinitial = datetime(int(dateinitial[0]), int(dateinitial[1]), int(dateinitial[2]), int(dateinitial[3]) ,int(dateinitial[4]), int(dateinitial[5]))
    # difference left in new year
    difference = newyeardate - dateinitial
    emb = discord.Embed(title="How long until New Years:", color = discord.Color.from_rgb(0, 0, 128))

    emb.set_author(name=f"Requested by @{interaction.user.name}", icon_url=interaction.user.avatar)
    emb.add_field(name = " TIME LEFT: ", value = f"{difference}")
    emb.set_footer(text = "Format in Hours:Minutes:Seconds")
    await interaction.response.send_message(embed = emb)

@tree.command(name = "coinflip", description = "Flip a coin and see the result: heads or tails.")
async def coinflip(interaction: discord.Interaction):
    result = "Heads" if random.choice([True, False]) else "Tails"
    await interaction.response.send_message(f"The coin landed on **{result}**!")

#bot makes prompt
@tree.command(name = "prompt", description = "Bot makes a random prompt",)
async def embed(interaction: discord.Interaction):
    emb = discord.Embed(title="Your Prompt:", description = f"{myStory.storyPrompt()}", color = discord.Color.random())

    emb.set_author(name=f"Requested by @{interaction.user.name}", icon_url=interaction.user.avatar)
    emb.set_thumbnail(url = interaction.guild.icon)
    emb.set_footer(text = "End of Prompt.")
    await interaction.response.send_message(embed = emb)

@tree.command(name = "imagesearch", description = "Searches an image of anything (character, food, etc) from the Internet!",)
async def emb2(interaction: discord.Interaction, name:str):
    search_params = {
        'key': GOOGLE,
        'cx': SEARCH,
        'q': name,
        'searchType': 'image',
    }

    response = requests.get('https://www.googleapis.com/customsearch/v1', params=search_params)
    data = response.json()

    if 'items' in data:
        items = data['items']
        if items:
            random_item = random.choice(items)  # Choose a random image
            image_url = random_item['link']
            emb2 = discord.Embed(title="Chosen image:", description = f"Image of {name}", color = discord.Color.random())
            emb2.set_image(url=image_url)

            emb2.set_author(name=f"Requested by @{interaction.user.name}", icon_url=interaction.user.avatar)
            emb2.set_thumbnail(url = interaction.guild.icon)
            emb2.set_footer(text = "Here you go.")
            await interaction.response.send_message(embed = emb2)
        else:
            await interaction.response.send_message("No images found for the given query.")
    else:
        await interaction.response.send_message("No image found for the given query.")

@tree.command(name = "poll", description = "Start a poll")
async def rearrange(interaction: discord.Interaction, question:str, choice1:str, choice2:str):
    emb = discord.Embed(title=f"{question}", description = "Choose an option: ", color = discord.Color.random())
        # Use left and right arrow emojis instead of numbers
    emb.add_field(name="Option 1", value=f"1️⃣ {choice1}", inline=True)
    emb.add_field(name="Option 2", value=f"2️⃣ {choice2}", inline=True)
    emb.set_author(name=f"Requested by @{interaction.user.name}", icon_url=interaction.user.avatar)
    emb.set_footer(text="Why can't humans just agree with one another?")

    # Send the menu as a message
    menu_message = await interaction.response.send_message(embed=emb)
    menu_message = await interaction.original_response()

    # Add reactions to the menu for user selection
    for emoji in ["1️⃣", "2️⃣"]:
        await menu_message.add_reaction(emoji)

selected_options = {}
@tree.command(name = "rockpaperscissors", description = "Play Rock, Paper, Scissors against Mutton-Chan!")
async def rearrange(interaction: discord.Interaction):
    selected_options.clear()
    options = ["Rock 🪨", "Paper 📝", "Scissors ✂️"]
    emb = discord.Embed(title="Play a game:", description = f"Choose an option:", color = discord.Color.random())
    for index, option in enumerate(options, start=1):
        # Use left and right arrow emojis instead of numbers
        emb.add_field(name=f"Option {index}", value=option, inline=True)


    # Send the menu as a message
    menu_message = await interaction.response.send_message(embed=emb)
    menu_message = await interaction.original_response()

    # Add reactions to the menu for user selection
    for emoji in ['🪨', '📝', '✂️']:
        await menu_message.add_reaction(emoji)

@tree.command(name="avatar", description = "Displays the avatar of a user.")
async def avatar(interaction: discord.Interaction, member: discord.Member):
    emb = discord.Embed(title="User Avatar:", color=discord.Color.random())
    emb.set_author(name=f"Requested by @{interaction.user.name}", icon_url=interaction.user.avatar)
    emb.add_field(name=f"@{member}'s Avatar:", value="", inline=False)
    emb.set_image(url=member.avatar)
    await interaction.response.send_message(embed=emb)

@client.event
async def on_raw_reaction_add(payload):
    # Check if the reaction was added by a bot or not the menu message
    if payload.member.bot:
        return

    # Check if the user has already made a selection
    user_id = str(payload.user_id)
    if user_id in selected_options:
        return

    # Check if the reaction is a valid option
    valid_reactions = ['🪨', '📝', '✂️']  # These are the emojis for options 1, 2, 3
    if payload.emoji.name not in valid_reactions:
        return

    # Get the selected option based on the emoji
    selected_option = valid_reactions.index(payload.emoji.name)

    # Do something based on the selected option
    try:
        options = ["Rock", "Paper", "Scissors"]
        selected_option_text = options[selected_option]
        channel = client.get_channel(payload.channel_id)
        botchoice = random.choice(options)
        outcomes = {
            "Rock": {"Rock": "tied", "Scissors": "won", "Paper": "lost"},
            "Paper": {"Rock": "won", "Scissors": "lost", "Paper": "tied"},
            "Scissors": {"Rock": "lost", "Scissors": "tied", "Paper": "won"},
        }
        outcome = outcomes[selected_option_text][botchoice]
        message = f"{payload.member.mention} {outcome} against Mutton-Chan!"
        await channel.send(f"Mutton-Chan chose {botchoice}, {message}")

        # Mark the user as having made a selection
        selected_options[user_id] = True
    except Exception as e:
        print(f"An error occurred: {e}")

# Moderation Commands
@tree.command(name = "purge", description = "Purges a set amount of Messages.")
async def purge(interaction: discord.Interaction, amount: int):
    if interaction.user.guild_permissions.manage_messages:
        channel = interaction.channel
        async for message in channel.history(limit=amount):
            await message.delete()
                
        await interaction.response.send_message(f"Deleted {amount} messages! Requested by {interaction.user.mention}.")
        await asyncio.sleep(5)
        async for message in channel.history(limit=1):
            await message.delete()
    else:
        await interaction.response.send_message("No Permissions? Womp Womp.")

try:
    with open('blacklist.json', 'r') as file1:
        blacklist_list = json.load(file1)
except FileNotFoundError:
    blacklist_list = {}

@tree.command(name="blacklist", description="Blacklists certain words")
async def blacklist(interaction: discord.Interaction, word: str):
    if interaction.user.guild_permissions.manage_messages:
        server_id = str(interaction.guild.id)
        if server_id not in blacklist_list:
            blacklist_list[server_id] = {}
            if word not in blacklist_list[server_id]:
                blacklist_list[server_id][word] = True
                with open('blacklist.json', 'w') as file:
                    json.dump(blacklist_list, file)  # Write the updated list back to the file
                await interaction.response.send_message("Blacklisted a word")
            else:
                if blacklist_list[server_id][word] == False:
                    blacklist_list[server_id][word] = True
                    with open('blacklist.json', 'w') as file:
                        json.dump(blacklist_list, file)  # Write the updated list back to the file
                    await interaction.response.send_message("Blacklisted a word")
                else:
                    await interaction.response.send_message("Word is already blacklisted!")
        else:
            if word not in blacklist_list[server_id]:
                blacklist_list[server_id][word] = True
                with open('blacklist.json', 'w') as file:
                    json.dump(blacklist_list, file)  # Write the updated list back to the file
                await interaction.response.send_message("Blacklisted a word")
            else:
                if blacklist_list[server_id][word] == False:
                    blacklist_list[server_id][word] = True
                    with open('blacklist.json', 'w') as file:
                        json.dump(blacklist_list, file)  # Write the updated list back to the file
                    await interaction.response.send_message("Blacklisted a word")
                else:
                    await interaction.response.send_message("Word is already blacklisted!")
    else:
        await interaction.response.send_message("Who do you think you are?")

@tree.command(name="unblacklist", description="Blacklists certain words")
async def blacklist(interaction: discord.Interaction, word: str):
    if interaction.user.guild_permissions.manage_messages:
        server_id = str(interaction.guild.id)
        if blacklist_list[server_id][word] ==  True:
            blacklist_list[server_id][word] = False 
            with open('blacklist.json', 'w')as file:
                json.dump(blacklist_list, file)
            await interaction.response.send_message("Unblacklisted a word")
        else:
            await interaction.response.send_message("Word has already been unblacklisted Mr. Alzheimers")
    else:
        await interaction.response.send_message("I went to mod town and nobody knew you")

@tree.command(name="statcreator", description="Creates imaginary stats for your character!")
async def statcreator(interaction: discord.Interaction):
    user = interaction.user.name
    COUNT = 100
    strength, tenacity, dexterity, wisdom = 0, 0, 0, 0
    # strength = random.randint(0, 100)
    # dexterity = random.randint(0, 100-strength)
    # tenacity = random.randint(0, 100-strength-dexterity)
    # wisdom = random.randint(0, 100-tenacity-strength-dexterity)
    while COUNT != 0:
        x = random.randint(0,3)
        if x == 0:
            strength += random.randint(0, COUNT)
        elif x == 1:
            tenacity += random.randint(0, COUNT)
        elif x== 2:
            dexterity += random.randint(0, COUNT)
        elif x == 3:
            wisdom += random.randint(0, COUNT)
        else:
            print("Error")
        COUNT = (100-strength-tenacity-dexterity-wisdom)

    emb = discord.Embed(title=f"{user}'s stats!", description = "Still weaker than Mutton-Chan...", color = discord.Color.random())
    emb.set_thumbnail(url = interaction.user.avatar)
    emb.add_field(name="Strength: ", value=f"{strength}%", inline=False)
    emb.add_field(name="Tenacity: ", value=f"{tenacity}%", inline=False)
    emb.add_field(name="Dexterity: ", value=f"{dexterity}%", inline=False)
    emb.add_field(name="Wisdom: ", value=f"{wisdom}%", inline=False)
    emb.set_author(name=f"Requested by @{interaction.user.name}", icon_url=interaction.user.avatar)
    emb.set_footer(text="What? Did you really think you were stronger than this?")

    await interaction.response.send_message(embed=emb)

#on bot
@client.event
async def on_ready():
    print("Connected to Discord uwu haha app")
    await tree.sync()
    change_status.start()

@client.event
async def on_message(message):
    if client.user in message.mentions and not message.author.bot:
        random_response = random.randint(1, 2)
        if random_response == 1:
            await message.channel.send(f"Go do something more productive")
        else:
            await message.channel.send(f"Get a life")

@client.event
async def on_message(message):
    if not message.author.bot:
        server_id = str(message.guild.id)
        if server_id in blacklist_list:
            for word, is_blacklisted in blacklist_list[server_id].items():
                if is_blacklisted and word in message.content.lower():
                    await message.delete()
                    await message.channel.send(f"{message.author} said a bad word it hurt my feelings")
                    break  # Exit the loop once a blacklisted word is found

# Load welcome function status from a JSON file
try:
    with open('welcome_function.json', 'r') as file:
        welcome_function_per_guild = json.load(file)
except FileNotFoundError:
    welcome_function_per_guild = {}

# set welcome command
@tree.command(name = "set_welcome", description = "set welcome channel",)
async def setwelcome(interaction: discord.Interaction):
    try:
        global welcome_function_per_guild
        guild_id = str(interaction.guild.id)
        
        if guild_id in welcome_function_per_guild and welcome_function_per_guild[guild_id] ==  True:
            await interaction.response.send_message("Welcome message is already on!")
        else:
            if interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("Welcome message set")
                welcome_function_per_guild[guild_id] = True
                with open('welcome_function.json', 'w') as file:
                    json.dump(welcome_function_per_guild, file)
            else:
                await interaction.response.send_message("You're not admin")
    except Exception as e:
        print(f"An error occurred in 'set_welcome' command: {e}")

# remove welcome command
@tree.command(name = "unset_welcome", description = "Remove welcome channel",)
async def unsetwelcome(interaction: discord.Interaction):
    try:
        global welcome_function_per_guild
        guild_id = str(interaction.guild.id)
        if guild_id in welcome_function_per_guild and welcome_function_per_guild[guild_id] == False:
            await interaction.response.send_message("Welcome message is already off!")
        else:
            if interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("Removed welcome message")
                welcome_function_per_guild[guild_id] = False
                with open('welcome_function.json', 'w') as file:
                    json.dump(welcome_function_per_guild, file)
            else:
                await interaction.response.send_message("You're not admin")
    except Exception as e:
        print(f"An error occurred in 'set_welcome' command: {e}")

@tree.command(name="addautorole", description="Adds Auto Roles for user when they join")
async def addAutoRole(interaction: discord.Interaction, role: discord.Role):
    try:
        with open('serverroles.json', 'r') as file:
            roleData = json.load(file)
    except FileNotFoundError:
        roleData = {}
    guild_id = str(interaction.guild.id)
    if interaction.user.guild_permissions.administrator:
        roleData[guild_id] = str(role.name)
        with open("serverroles.json", "w") as file:
            json.dump(roleData, file)
        await interaction.response.send_message(f"Auto Role set to {role.name}")
    else:
        await interaction.response.send_message("You're not admin loser")

# when member joins start function
@client.event
async def on_member_join(member):
    global welcome_function_per_guild
    guild_id = str(member.guild.id)
    if guild_id in welcome_function_per_guild and welcome_function_per_guild[guild_id]:
        channel = member.guild.system_channel
        await channel.send(f'Mutton-Chan welcomes {member.mention} to the server ♡!')
        await channel.send('https://media.tenor.com/73wKQVjruFcAAAAC/chiaki-nanami-anime.gif')
    else:
        print(f'A user joined in server with id {guild_id}')

    #sets auto role
    with open('serverroles.json', 'r') as file:
            roleData = json.load(file)
    if guild_id in roleData and roleData[guild_id]:
        role = discord.utils.get(member.guild.roles, name=roleData[guild_id])
        await member.add_roles(role)
    else:
        print(f"No roles assigned to user in {str(member.guild.name)}")

#for 24/7 go replit
client.run(TOKEN)
