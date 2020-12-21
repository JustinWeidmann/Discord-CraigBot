import discord
import scrape
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "Nzg1NjkzNDk3MTU5OTc0OTgy.X87kFw.KGnloEjq4qVHfUw_Z1qmzQelgac"
searchTerm = "metal"
channelID = 790714962037309530

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #message.channel.send(f'Heyyyy mann im your local scraper for {searchTerm} and posting to {channelID}. !creg help to get started bro ͡° ͜ʖ ͡ –')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!creg help'):
        await message.channel.send(f'**!setChannelID <channelID>**:   Sets defalt channel\n**!give me the scoop**:   Prints all results for {searchTerm}\n**!search <term>**:   Searches for <term> then prints all results')

    # if message.content.startswith('!setChannelID'):
    #     global channelID
    #     channelID = message.content[14:]
    #     await message.channel.send(f'Channel set to: **{channelID}**')

    if message.content.startswith('!give me the scoop'):
        print(f'Scraping all the {searchTerm}...')
        await message.channel.send("Give me a sec...")
        global oldPostTime

        cregResults = scrape.runScrape(searchTerm)
        postIndex = cregResults[0][0]
        postTitle = cregResults[0][1]
        postTime = cregResults[0][2]
        postLocation = cregResults[0][3]
        postURL = cregResults[0][4]
        funFact = cregResults[1]

        i = 0
        for cregResults in postIndex:
            await message.channel.send(f'{postIndex[i]}: {postTitle[i]}\n {postTime[i]}\n {postLocation[i]}\n {postURL[i]}\n')

            i += 1
        
        await message.channel.send(funFact)
        oldPostTime = postTime

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

        i = 0
        for cregResults in postIndex:
            await message.channel.send(f'{postIndex[i]}: {postTitle[i]}\n {postTime[i]}\n {postLocation[i]}\n {postURL[i]}\n')
            i += 1
        
        await message.channel.send(funFact)

    # if message.content.startswith('!stop'):
    #     print("got stop")
    #     break command

def initialCheck():
    print("Runing ititial check...")
    cregResults = scrape.runScrape(searchTerm)
    global oldPostTime
    oldPostTime = cregResults[0][2]

async def checkForNew():
    global oldPostTime
    global channelID
    channel = client.get_channel(channelID)    # Discord Channel ID, Room-1:528448098293514240,
    print("Checking for new posts...")
    cregResults = scrape.runScrape(searchTerm)
    postTitle = cregResults[0][1]
    postTime = cregResults[0][2]
    postLocation = cregResults[0][3]
    postURL = cregResults[0][4]

    
    i = 0
    for cregResults in postTime:
        print(f'Checking: {i}')
        if postTime[i] <= oldPostTime[0]:
            print("Ran out of new")
            print(f'Because: {postTime[i]} is <= then {oldPostTime[0]}')
            #await channel.send("Nada")
            break
        elif postTime[i] > oldPostTime[0]:
            print(f'{i} is new!!')
            print(f'Because: {postTime[i]} is > then {oldPostTime[0]}')
            await channel.send(f'{postTitle[i]}\n {postTime[i]}\n {postLocation[i]} {postURL[i]}\n')
        
        i += 1
    
    oldPostTime = postTime
    

initialCheck()
if __name__ == '__main__':
    sched = AsyncIOScheduler()
    sched.add_job(checkForNew, 'interval', minutes = 10)
    sched.start()
client.run(TOKEN)
