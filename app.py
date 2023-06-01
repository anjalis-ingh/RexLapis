import nextcord, random, json, global_, os, asyncio, sqlite3
from nextcord import Intents
from nextcord.ext import commands

with open('config.json') as f:
    data = json.load(f)
    token = data["token"]

# change only the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Basic Commands'
)

intents = Intents.default()
intents.message_content = True
# create the bot 
bot = commands.Bot(
    command_prefix=".",
    intents=intents,
    help_command = help_command
)

# load all the cogs 
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print("File loaded!")

# main
async def main():
    await load()
    await bot.start(token)

# -------------- BASIC COMMANDS -----------------
# -------------- .hello --------------
@bot.command(name="hello", brief="Introduce yourself to Rex Lapis and get started!", 
             description="Rex Lapis will introduce himself and a list of starter commands will be presented")
async def embed(ctx):
    embed = nextcord.Embed(title = "Rex Lapis - Your Local God of Contracts!", 
                           description = "You stand in the presence of the mighty Rex Lapis fellow human. What are you wanting to do today? If you are in any need of help about commands, I suggest you refer to `.help`\n\n", 
                           color = 0xFEC04B)
    # starter commands 
    desc1 = ("> **.status** - ask him what he has been up to in his free time :)\n\n"
             "> **.interact** - list of all the interaction commands such as .feed, .advice, .gift, .pray\n\n"
             "> **.games** - battle against Rex Lapis in minigames and win to get mora as a reward!\n\n"
             "> **.shop** - displays the shop's inventory where you can buy treats and goodies for Rex Lapis\n\n"
             "> **.level** - check stats on your friendship and happiness levels, happiness points, and amount of mora\n\n"
    )
    embed.add_field(name="__Here are a few commands to get started!__", value = (desc1), inline=False)
    embed.add_field(name="__Want to know more?__", value = "Learn about the purpose of the bot using `.purpose` and get more clarity with the bot's terminology using `.terms`", inline=False)
    file = nextcord.File("Images/14.png")
    embed.set_thumbnail(url="attachment://14.png")
    embed.set_footer(text=" | Ones who break their contracts shall suffer the Wrath of the Rock.", icon_url="https://i.pinimg.com/originals/bd/9e/e6/bd9ee6d943aa0c814c52b3f7b2b94878.jpg")
    await ctx.send(file = file, embed=embed)

# -------------- .level --------------
@bot.command(name="level", brief="Check stats on your friendship and happiness level and mora", 
            description = "Gives an overview of the server friendship level, member's happiness level/points with Rex Lapis, and amount of balance currently")
async def embed(ctx, member:nextcord.Member = None):
    names = ['Rex Lapis', 'Morax', 'Geo Archon', 'God of Contracts', 'God of War', 'Prime of the Adepti', 'Lord of Rock', 'Deity of Dirt', 
             'Emperor of Earth', 'Governor of the Ground', 'Master of Minerals', 'Tyrant of Terrain', 'Sovereign of Soil', 'Baron of Boulders','God of Stoves' 
    ]
    if member is None:
            member = ctx.author 
        
    db = sqlite3.connect("main.sqlite")
    cur = db.cursor()
    cur.execute(f"SELECT mora, hp FROM main WHERE user_id = {member.id}")
    bal = cur.fetchone()
    try:
        mora = bal[0]
        hp = bal[1]
    except:
        mora = 0 
        hp = 0

    randomName = random.choice(names)
    embed = nextcord.Embed(title = "Current Stats", description="", color = 0xFEC04B)
    embed.add_field(name="Name", value=randomName, inline=True)
    embed.add_field(name="Balance (Mora)", value=mora, inline=True)
    embed.add_field(name="Friendship Level", value=global_.friendshipLvl, inline=False)
    embed.add_field(name="Happiness Level", value=global_.happinessLvl, inline=False)
    embed.add_field(name="Happiness Points", value=hp, inline=False)


    file = nextcord.File("Images/3.png")
    embed.set_thumbnail(url="attachment://3.png")
    await ctx.send(file=file, embed=embed)

# -------------- .purpose --------------
@bot.command(name="purpose", brief="States the the purpose the Rex Lapis Discord Bot", 
             description="States the the purpose the Rex Lapis Discord Bot")
async def embed(ctx):
    embed = nextcord.Embed(title = "Purpose", 
                           description = " > Rex Lapis can be used both for fun or as a community engagement tool, to keep or revive quiet servers. He typically acts as the mighty, wise god he once was in his prime but this precious loaf also acts as a laid back friend at times on your server! Everyone is responsible for taking care of the overlord as happiness levels are raised collectively as a server.\n\n"
                                        "> As a devoted friend and believer of Rex Lapis, members can interact with him and improve his happiness levels using a variety of petting commands. Members can also interact and ask advice as a friend, pray and gift the god, earn money, shop for items, and more!\n", 
                           color = 0xFEC04B)
    await ctx.send(embed=embed)

# -------------- .status --------------
@bot.command(name="status", brief="Ask Rex Lapis what he has been up to during his free time :)", 
             description ="Rex Lapis will state his mood or what hobby he was pursuing a little while back. Can be done every 8 hours.")
async def embed(ctx):
    member = ctx.author

    db = sqlite3.connect("main.sqlite")
    cur = db.cursor()
    
    # should be used by user once every 8 hours 
    # randomize which of the 7 statuses to choose from 
    randomNum = random.randint(1,9)
    match randomNum:
        case 1:
            embed = nextcord.Embed(title = "Chilling", description = "Today has been a relaxing day. I hope tomorrow too shall be prosperous.", color = 0xFEC04B)
            file = nextcord.File("Images/4.png")
            embed.set_image(url="attachment://4.png")
            await ctx.send(file=file, embed=embed)
        
        case 2:
            embed = nextcord.Embed(title = "Bored", description = "What can I say? Much has not been happening. How has your day been friend?", color = 0xFEC04B)
            file = nextcord.File("Images/5.png")
            embed.set_image(url="attachment://5.png")

            await ctx.send(file=file, embed=embed)

            def check(m):
                return m.author.id == ctx.author.id 
            
            m = await bot.wait_for("message", check=check)
            await ctx.send('Good to know, hope the rest of your day shall be prosperous!')

        case 3:
            embed = nextcord.Embed(title = "Drawing", description = "I decided to indulge my time today doing the arts. When I get time to relax like this, it definitely puts my mind at ease.", color = 0xFEC04B)
            file = nextcord.File("Images/7.png")
            embed.set_image(url="attachment://7.png")
            await ctx.send(file=file, embed=embed)
        
        case 4:
            embed = nextcord.Embed(title = "Playing", description = "Now and then we all got to have a little bit of fun, you know? Would you like to join? [yes or no]", color = 0xFEC04B)
            file = nextcord.File("Images/15.png")
            embed.set_image(url="attachment://15.png")
            await ctx.send(file=file, embed=embed)

            def check(m):
                return m.author.id == ctx.author.id 
            
            m = await bot.wait_for("message", check=check)
            if m.content == "yes": # HP +20
                global_.updateHP(20, cur, member)
                await ctx.send('I enjoyed your company today, lets hang out later if the opportunity arises! **HP +20**')
            else:
                await ctx.send('No worries, I understand you must be very busy. Maybe next time I suppose.')
        
        case 5:
            embed = nextcord.Embed(title = "Finding Mora", description = "It seems like yet again I can't find any Mora on me. You wouldn’t mind lending some to me, friend? I just need 100 Mora for a quick buy. [yes or no]", color = 0xFEC04B)
            file = nextcord.File("Images/16.png")
            embed.set_image(url="attachment://16.png")
            await ctx.send(file=file, embed=embed)

            def check(m):
                return m.author.id == ctx.author.id 
            m = await bot.wait_for("message", check=check)

            if m.content == "yes": # HP +40 Mora -100
                cur.execute(f"SELECT mora, hp FROM main WHERE user_id = {member.id}")
                bal = cur.fetchone()

                try:
                    mora = bal[0]
                    hp = bal[1]
                except:
                    mora = 0
                    hp = 0

                if int(mora) >= 100:
                    sql = ("UPDATE main, hp SET mora = ?, hp = ? WHERE user_id = ?")
                    val = (mora - 100, hp + 40, member.id)
                    cur.execute(sql, val) 
                    await ctx.send('Thank you for the token of appreciation. Bless your pulls my good lad. **HP +40, Mora -100**')
                else:
                    await ctx.send('Seems like you are broke too lad. Oh well, thanks for wanting to help!')
            else:
                await ctx.send('I guess I remain a penniless dragon today -shrugs-')
        
        case 6: # Mora +20
            embed = nextcord.Embed(title = "Exploring", description = "I enjoy partaking in walks through the city — when time permits. Are you interested in exploring? If you'd like to see Liyue's tourist spots, I have a few references. I also found some treausres along the way, use it wisely! **Mora +20**", color = 0xFEC04B)
            file = nextcord.File("Images/11.png")
            embed.set_image(url="attachment:/11.png")

            global_.updateMora(20, cur, member)
            await ctx.send(file=file, embed=embed)
        
        case 7: # Mora +20
            embed = nextcord.Embed(title = "Making a Gift", description = "Happen to remember a close friend of mine and wanting to return a gesture of kindness back. Because I am feeling so kind, here is some Mora for you. Spend it wisely. **Mora +20**", color = 0xFEC04B)
            file = nextcord.File("Images/12.png")
            embed.set_image(url="attachment://12.png")

            global_.updateMora(20, cur, member)
            await ctx.send(file=file, embed=embed)
        case 8:
            embed = nextcord.Embed(title="Camping", description="Went on a expedition recently, had time to think. For those that live too long, the friends of days gone by and scenes from their adventures live on in their memories. As such I want to say I have no regrets in meeting you, friend. Should the day ever come that we are not together, you will continue to shine like gold in my memories.", color = 0xFEC04B)
            file = nextcord.File("Images/18.png")
            embed.set_image(url="attachment://18.png")
            await ctx.send(file=file, embed=embed)
        case 9:
            embed = nextcord.Embed(title="Shopping", description="Had some time off from my busy schedule and decided to partake in some shopping. One can never overspend on tea.")
            file = nextcord.File("Images/19.png")
            embed.set_image(url="attachment://19.png")
            await ctx.send(file=file, embed=embed)

    db.commit()
    cur.close()
    db.close()

# -------------- .terms --------------
@bot.command(name="terms", brief="Explanation of unfamiliar terminology to members", description = "Words such as mora, happiness points, friendship level, and such are further explained in detail")
async def embed(ctx):
    embed = nextcord.Embed(title = "Terminology", description="", color =0xFEC04B) 
    embed.add_field(name="Mora", value="It is the `main currency unit` used to purchase various dishes at the shop. It can be earned through commissions, pulls, and sometimes interactions with Rex Lapis. It can be viewed anytime using `.balance`", inline=False)
    embed.add_field(name="Happiness Points (HP)", value="These points are earned through `interactions with Rex Lapis` (.status and .interact) and can increase or decrease which can affect levels. Each member can view how many points they have individually by doing `.level`", inline=False)
    embed.add_field(name="Friendship Level (FL)", value="This is based off the `total # of HP earned by a member`. Every `50 HP` unlocks a new level. View the member's FL by doing `.level`", inline=False)
    embed.add_field(name="Happiness Level (HL)", value="This is based off the `total # of HP earned by the server`. Every `100 HP` unlocks a new level. View the server's HL by doing `.level`", inline=False)
    await ctx.send(embed=embed)

# -------------- .bye --------------
@bot.command(name="bye", brief = "Say bye to Rex Lapis and sign off!", description = "Rex Lapis waves bye back to you :)")
async def sendGif(ctx):
    await ctx.send("May we meet again!", file = nextcord.File("rex lapis.gif"))

# main runner 
asyncio.get_event_loop().run_until_complete(main())
