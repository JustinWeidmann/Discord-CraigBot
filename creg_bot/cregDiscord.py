import discord
from discord.ext import commands

import scrape
import moneyScrape
import asyncio
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "Nzk4NjQ3NTY5ODk0MjExNjM0.X_4Egg.XQspqdLEL3mkJrMX9XBEDB6IkUA"
searchList = ["monitor", "tv"]
universalBudget = 100

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    #message.channel.send(f'Heyyyy mann im your local scraper for {searchList} and posting to {channelID}. !creg help to get started bro ͡° ͜ʖ ͡ –')

#sets value in json to guild id upon the bot joining the guild
@bot.event
async def on_guild_join(guild):
    #loads json file to dictionary
    with open('serverChannles.json', "r") as f:
        channels = json.load(f)

    channel = discord.utils.get(guild.channels, name = str(guild.text_channels[0]))
    channelID = channel.id
    channels[str(guild.id)] = channelID
    #print(f'channels: {channels}')

    #writes dictionary to json file
    with open('serverChannles.json', "w") as f:
        json.dump(channels, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('serverChannles.json', "r") as f:
        channels = json.load(f)

    channels.pop(str(guild.id))

    #writes dictionary to json file
    with open('serverChannles.json', "w") as f:
        json.dump(channels, f, indent=4)

#allows server members to set channel for welcome messages to send to    
@bot.command()
async def changeChannle(ctx, channleID):
    with open('serverChannles.json', "r") as f:
        channels = json.load(f)

    channels[str(ctx.guild.id)] = channleID
    print(channels)

    #writes dictionary to json file
    with open('serverChannles.json', "w") as f:
        json.dump(channels, f, indent=4)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('!creg help'):
        await message.channel.send(f'**!setChannelID <channelID>**:   Sets defalt channel\n**!give me the scoop**:   Prints all results for {searchList}\n**!search <term>**:   Searches for <term> then prints all results\n**!mSearch <term>**:   Searches for <term> with budget of ${universalBudget} then prints all results')

    # if message.content.startswith('!setChannelID'):
    #     global channelID
    #     channelID = message.content[14:]
    #     await message.channel.send(f'Channel set to: **{channelID}**')

    if message.content.startswith('!give me the scoop'):
        print(f'Scraping all the {searchList}...')
        await message.channel.send("Give me a sec...")
        global oldPostTime

        for i in range(len(searchList)):
            cregResults = scrape.runScrape(searchList[i])
            postIndex = cregResults[0][0]
            postTitle = cregResults[0][1]
            postTime = cregResults[0][2]
            postLocation = cregResults[0][3]
            postURL = cregResults[0][4]
            funFact = cregResults[1]

            j = 0
            for cregResults in postIndex:
                await message.channel.send(f'{postIndex[j]}: {postTitle[j]}\n {postTime[j]}\n {postLocation[j]}\n {postURL[j]}\n')

                j += 1
            
            await message.channel.send(funFact)
            oldPostTime[i] = postTime

    if message.content.startswith('!search'):
        searchGrab = message.content[8:]
        await message.channel.send(f'Searching for {searchGrab}...')
        print(f'Scraping for {searchGrab}...')

        cregResults = scrape.runScrape(searchGrab)
        postIndex = cregResults[0][0]
        postTitle = cregResults[0][1]
        postTime = cregResults[0][2]
        postLocation = cregResults[0][3]
        postURL = cregResults[0][4]
        funFact = cregResults[1]

        if len(postIndex) != 0:
            for i in range(len(postIndex)):
                await message.channel.send(f'{postIndex[i]}: {postTitle[i]}\n {postTime[i]}\n {postLocation[i]}\n {postURL[i]}\n')
            await message.channel.send(funFact)
        else:
            await message.channel.send(f'There are no "{searchGrab}" on Craigslist right now')
        
    
    if message.content.startswith('!mSearch'):
        searchGrab = message.content[9:]
        await message.channel.send(f'Searching for {searchGrab}...')
        print(f'Scraping for {searchGrab}...')

        cregResults = moneyScrape.runScrapeMon(searchGrab, universalBudget)
        postIndex = cregResults[0][0]
        postTitle = cregResults[0][1]
        postTime = cregResults[0][2]
        postLocation = cregResults[0][3]
        postPrice = cregResults[0][4]
        postURL = cregResults[0][5]
        funFact = cregResults[1]

        if len(postIndex) != 0:
            for i in range(len(postIndex)):
                await message.channel.send(f'{postIndex[i]}: {postTitle[i]}\n {postTime[i]}\n {postLocation[i]}\n ${postPrice[i]}\n {postURL[i]}\n')
            await message.channel.send(funFact)
        else:
            await message.channel.send(f'There are no "{searchGrab}" in your budget of **${universalBudget}** on Craigslist right now')


def initialCheck():
    print("Runing ititial check...")
    global oldPostTime
    oldPostTime = []

    for i in range(len(searchList)):
        cregResults = scrape.runScrape(searchList[i])
        oldPostTime.append(cregResults[0][2])
    print("Done with initial check!")

async def checkForNew():
    global oldPostTime
    print("Checking for new posts...")

    for i in range(len(searchList)):
        cregResults = scrape.runScrape(searchList[i])
        postTitle = cregResults[0][1]
        postTime = cregResults[0][2]
        postLocation = cregResults[0][3]
        postURL = cregResults[0][4]

        
        for j in range(len(postTime)):
            print(f'Checking: {j}')
            if postTime[j] <= oldPostTime[i][0]:
                print("Ran out of new")
                print(f'Because: {postTime[j]} is <= then {oldPostTime[i][0]}')
                break
            elif postTime[j] > oldPostTime[i][0]:
                print(f'{j} is new!!')
                print(f'Because: {postTime[j]} is > then {oldPostTime[i][0]}')
                
                with open('serverChannles.json', 'r') as f:
                    channel_id = json.load(f)
                    for k in range(len(channel_id)):
                        channelID = list(channel_id.values())
                        channel = bot.get_channel(channelID[k])
                        await channel.send(f'{postTitle[j]}\n {postTime[j]}\n {postLocation[j]} {postURL[j]}\n')
        
        oldPostTime[i] = postTime
    
    print("Done checking!")
    

initialCheck()
if __name__ == '__main__':
    sched = AsyncIOScheduler()
    sched.add_job(checkForNew, 'interval', minutes = 5)
    sched.start()
bot.run(TOKEN)
