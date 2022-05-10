# bot.py essentials
import discord
import os
import json
import random
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv

# external API
import pixivapi
from pathlib import Path
from pixivapi import Client
from pixivapi import Size
from datetime import date

# general uses of library
from random import randint

#.env file to hide some informations
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PIXIV_USERNAME = os.getenv('PIXIV_USERNAME')
PIXIV_PASSWORD = os.getenv('PIXIV_PASSWORD')

# Implementing API
bot = commands.Bot(command_prefix='!')
myPixiv = pixivapi.Client()

print('We have logged in')

myPixiv.login(PIXIV_USERNAME, PIXIV_PASSWORD)

# Jebaited trivia question
@bot.command(name='trivia')
async def trivia(ctx):
    file = open("jebaited.txt", "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    selection = random.randint(0, line_count - 1)
    print(selection)
    if(selection % 2) == 0:
        line = read_line_from_file('jebaited.txt', selection)
        print(line)
        await ctx.send(line)
        await bot.wait_for('message')
        line = read_line_from_file('jebaited.txt', selection + 1)
        print(line)
        pepelaugh = discord.utils.get(bot.emojis, name='pepelaugh')
        await ctx.send(str(pepelaugh) + ' ' + line + ' ' + str(pepelaugh), tts=True)  
    else:
        selection += 1
        line = read_line_from_file('jebaited.txt', selection)
        print(line)
        await ctx.send(line)
        await bot.wait_for('message')
        line = read_line_from_file('jebaited.txt', selection + 1)
        print(line)
        pepelaugh = discord.utils.get(bot.emojis, name='pepelaugh')
        await ctx.send(str(pepelaugh) + ' ' + line + ' ' + str(pepelaugh), tts=True)    

#readline in txt.file
def read_line_from_file(file_name, line_number):
    with open(file_name, 'r') as f:
        for line_no, line in enumerate(f):
            if line_no == line_number:
                f.close()
                return line
        else:
            f.close()
            raise ValueError('line %s does not exist in file %s' % (line_number, file_name))

# Command for Pixiv
@bot.group(name='pixiv')
async def pixiv(ctx):
    pass

@pixiv.command(name='bookmark')
@commands.is_owner()
async def bookmark(ctx, arg):
    myPixiv.add_bookmark(arg)
    print('added to bookmarks')
    await ctx.send('Illustration ID: ' + str(arg) + ' has been added into your bookmarks')

masterIllustration = None

@pixiv.command(name='gacha')
async def gacha(ctx, arg=None): 
    global masterIllustration
    print('Give me a sec, I am still working on it')
    if arg != None: 
        print('Hello')  
        offsetRange = randint(100, 500)
        illustrations = myPixiv.search_illustrations(arg, offset=offsetRange)
        masterIllustration = illustrations['illustrations'][randint(0, len(illustrations) - 1)]
        try:
            masterIllustration.download(
            directory=Path.home() / 'Desktop' / 'Shameless',
            size=Size.ORIGINAL,       
            )
        except:
            await ctx.send("Couldn't download that folder. Try again.")
        embed = discord.Embed(
            title = "Illustration",
            description = 'Tag: ' + arg,
            colour = discord.Colour.darker_grey()
        )   
        embed.add_field(name='Illustration ID', value=masterIllustration.id, inline=True)      
        embed.add_field(name='Author ID', value=masterIllustration.user.id, inline=True)      
        embed.add_field(name='Dimensions', value='{} x {}'.format(masterIllustration.width, masterIllustration.height), inline=True)
        embed.add_field(name='Total Views', value=masterIllustration.total_view, inline=True)
        embed.add_field(name='Total Bookmarks', value=masterIllustration.total_bookmarks, inline=True)
        embed.add_field(name='Total "Coomments"', value=masterIllustration.total_comments, inline=True)
        embed.add_field(name='Creation date', value=masterIllustration.create_date, inline=False)
        embed.set_footer(text='Generated at ' + str(date.today()))
        file_path = 'C:/Users/light/Desktop/Shameless/' + str(masterIllustration.id)
        if masterIllustration.page_count != 1:
            print("Folder inc")
            file_path = 'C:/Users/light/Desktop/Shameless/' + str(masterIllustration.id) + '/' + str(masterIllustration.id) + '_p0'
        attach_path = file_path.split('/')[-1]
        if Path(file_path + '.png').exists():
            print('Crafting lewd PNG')
            file_extension = Path(str(masterIllustration.id) + '.png').suffix 
            file = discord.File(file_path + file_extension)
            embed.set_image(url='attachment://' + attach_path + file_extension)
            embed.set_thumbnail(url='attachment://' + attach_path + file_extension)
            await ctx.send(embed=embed, file=file)
        elif Path(file_path + '.jpg').exists():
            print('Crafting lewd JPG')
            file_extension = Path(str(masterIllustration.id) + '.jpg').suffix 
            file = discord.File(file_path + file_extension)
            embed.set_image(url='attachment://' + attach_path + file_extension)
            embed.set_thumbnail(url='attachment://' + attach_path + file_extension)
            await ctx.send(embed=embed, file=file)       
    else:
        print('Hello')
        try:
            illustrations = myPixiv.fetch_illustration_related(masterIllustration.id)['illustrations']
            masterIllustration = illustrations[randint(0, len(illustrations) - 1)]
            try:
                masterIllustration.download(
                    directory=Path.home() / 'Desktop' / 'Shameless',
                    size=Size.ORIGINAL,       
                )
            except:
                await ctx.send("Couldn't download that folder. Try again.")
            await ctx.send(':drum_with_drumsticks: "DRAMATIC DRUMROLL NOISES" :drum_with_drumsticks:')
            embed = discord.Embed()
            print('Give me a sec, I am still working on it')
            if 0 < masterIllustration.total_bookmarks < 10:
                embed = discord.Embed(
                    title = "TRASH",
                    description = 'Rating: ' + str(masterIllustration.total_bookmarks),
                    colour = discord.Colour.darker_grey()
                    )
            elif 10 <= masterIllustration.total_bookmarks < 100:
                embed = discord.Embed(
                    title = "COMMON",
                    description = 'Rating: ' + str(masterIllustration.total_bookmarks),
                    colour = discord.Colour.dark_grey()
                )
            elif 100 <= masterIllustration.total_bookmarks < 1000:
                embed = discord.Embed(
                    title = "UNCOMMON",
                    description = 'Rating: ' + str(masterIllustration.total_bookmarks),
                    colour = discord.Colour.green()
                )
            elif 1000 <= masterIllustration.total_bookmarks < 10000:
                embed = discord.Embed(
                    title = "RARE",
                    description = 'Rating: ' + str(masterIllustration.total_bookmarks),
                    colour = discord.Colour.blue()
                )
            elif 10000 <= masterIllustration.total_bookmarks < 20000:
                embed = discord.Embed(
                    title = "EPIC",
                    description = 'Rating: ' + str(masterIllustration.total_bookmarks),
                    colour = discord.Colour.purple()
                )
            elif 20000 <= masterIllustration.total_bookmarks < 50000:
                embed = discord.Embed(
                    title = "LEGENDARY",
                    description = 'Rating: ' + str(masterIllustration.total_bookmarks),
                    colour = discord.Colour.orange()
                )
            elif 50000 <= masterIllustration.total_bookmarks < 100000:
                embed = discord.Embed(
                    title = "SR - You're a lucky one!",
                    description = 'Rating: ' + str(masterIllustration.total_bookmarks),
                    colour = discord.Colour.red()
                )
            elif 100000 <= masterIllustration.total_bookmarks:
                embed = discord.Embed(
                    title = "SSR - You just won the lottery!",
                    description = 'Rating: ' + str(masterIllustration.total_bookmarks),
                    colour = discord.Colour.teal()
                )     
            embed.add_field(name='Illustration ID', value=masterIllustration.id, inline=True)      
            embed.add_field(name='Author ID', value=masterIllustration.user.id, inline=True)      
            embed.set_footer(text='Generated at ' + str(date.today()))
            file_path = 'C:/Users/light/Desktop/Shameless/' + str(masterIllustration.id)
            if masterIllustration.page_count != 1:
                print("Folder inc")
                file_path = 'C:/Users/light/Desktop/Shameless/' + str(masterIllustration.id) + '/' + str(masterIllustration.id) + '_p0'
            attach_path = file_path.split('/')[-1]
            if Path(file_path + '.png').exists():
                print('Crafting lewd PNG')
                file_extension = Path(str(masterIllustration.id) + '.png').suffix 
                file = discord.File(file_path + file_extension)
                embed.set_image(url='attachment://' + attach_path + file_extension)
                embed.set_thumbnail(url='attachment://' + attach_path + file_extension)
                await ctx.send(embed=embed, file=file)
            elif Path(file_path + '.jpg').exists():
                print('Crafting lewd JPG')
                file_extension = Path(str(masterIllustration.id) + '.jpg').suffix 
                file = discord.File(file_path + file_extension)
                embed.set_image(url='attachment://' + attach_path + file_extension)
                embed.set_thumbnail(url='attachment://' + attach_path + file_extension)
                await ctx.send(embed=embed, file=file)
        except:
            await ctx.send('No related illustrations associated with this one. Please try another illustration.')

bot.run(TOKEN)

