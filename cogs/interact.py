import nextcord, random, json, global_, sqlite3
from nextcord import Intents
from nextcord.ext import commands

class Interact_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # -------------- .interact -------------- 
    @commands.command(name="interact", brief="List of all interaction commands with Rex Lapis", 
                      description = "Want to interact with Rex Lapis? Refer to this command to learn how to feed, gift, or even pet him!")
    async def interactCmds(self, ctx):
        # interaction commands
        desc1 = ("1. **.pet** - hug, belly rub, or even cuddle with rex lapis if you dare to...\n\n"
                 "2. **.feed <item #> <quantity>** - feed Rex Lapis with dishes bought from the shop, yum!\n\n"
                 "3. **.advice** - need of any wise words for your fellow dragon deity? ask Rex Lapis!\n\n"
                 "4. **.pray** - one must pray to their God like they should to the mighty Rex Lapis\n\n"
                 "5. **.gift <amount>** - feeling generous? gift Rex Lapis some mora to help out the broke dragon\n\n"
        )

        embed = nextcord.Embed(title = "Interact with Rex Lapis!", description= (desc1), color=0xFEC04B)   
        file = nextcord.File("Images/21.png")
        embed.set_image(url="attachment://21.png")
        await ctx.send(file=file, embed=embed)

     # -------------- .feed -------------- 
    @commands.command(name="feed", brief="Feed Rex Lapis with dishes bought from the shop, yum!", description="Feed Rex Lapis with treats bought from the shop or earned through pulls")
    async def feedGod(self, ctx, itemNum: int, quantity: int):
        if global_.inventory.count(global_.food[itemNum]) >= quantity:
            if itemNum == 1:
                embed = nextcord.Embed(title = "Delivered!", description="Ah I see you got my favorite dish! When heated, slowly, gently, and with the utmost care and technique...Such a particular taste may only be shared with those who know how to appreciate it. **HP** **+" + str(global_.buyHP[itemNum] * quantity * 2) + "** :coffee:", color=0xFEC04B)
                global_.happinessPts += global_.buyHP[itemNum] * quantity * 2
            else:
                embed = nextcord.Embed(title = "Delivered!", description="This is quite delicious, thank you friend. We should get a quick meal to pick us back up later on. I know a good place in Chihu Rock! **HP** **+" + str(global_.buyHP[itemNum] * quantity) + "** :coffee:", color=0xFEC04B)
                global_.happinessPts += global_.buyHP[itemNum] * quantity

            global_.inventory.remove(global_.food[itemNum])
            file = nextcord.File("Images/8.png")
            embed.set_image(url="attachment://8.png")
            await ctx.send(file=file, embed=embed)
        else:
            await ctx.send("Seems like the dish you requested is either not in your inventory or you don't have enough. If you want to buy some more food, go to `.shop` and use `.buy <item #> <quantity>` to buy your desired items!")
    
     # -------------- .advice -------------- 
    @commands.command(name="advice", brief="Need of any wise words for your fellow dragon deity? Ask Rex Lapis!", description = "Rex Lapis can give members free advice at anytime to the member if asked")
    async def getAdvice(self, ctx):
        quotes = [ "Every journey has its final day. Don't rush", "Nothing can be accomplished without rules or standards. No matter if it is mortals or adepti, everyone has their place",
                  "Trade relies on both contracts and fairness. There is one thing you must never forget when making and abiding by a contract: if fairness is lost, then the contract shall become proof of one's deception.", 
                  "You should know that all power comes at a price. For every bit of power you gain, so too do you gain more responsibility."
        ]
        quote = random.choice(quotes)
        await ctx.send(quote)
    
    # -------------- .gift -------------- 
    @commands.command(name="gift", brief="Feeling generous? Gift Rex Lapis some mora to help him out!", descripton = "Give Rex Lapis some mora as a token of appreication if your feeling nice today! Do .gift <amount> to specify how much mora to give")
    async def giveGift(self, ctx, amount: int):
        member = ctx.author
        embed = nextcord.Embed(title="Gift Received!", description="Your well wishes are more than enough, but thank you. Bless your pulls my good lad. **HP** **+" + str(amount) + "** :two_hearts:", color=0xFEC04B)
        db = sqlite3.connect("main.sqlite")
        cur = db.cursor()
        cur.execute(f"SELECT mora FROM main WHERE user_id = {member.id}")
        mora = cur.fetchone()

        try:
            mora = mora[0]
        except:
            mora = 0
        
        sql = ("UPDATE main SET mora = ? WHERE user_id = ?")
        val = (mora - amount, member.id)
        cur.execute(sql, val) 
        
        global_.happinessPts += amount

        file = nextcord.File("Images/9.png")
        embed.set_image(url="attachment://9.png")
        await ctx.send(file=file, embed=embed)

        db.commit()
        cur.close()
        db.close()
    
    # -------------- .pet -------------- 
    @commands.command(name="pet", brief="Hug, belly rub, or even cuddle with rex lapis if you dare to...", description = "Hug, belly rub, or even cuddle with rex lapis if you dare to...he may or may not like the gesture. HL can be increased or decreased through this interaction")
    async def embed(self, ctx):
        randomNum = random.randint(1,5)
        match randomNum:
            # belly rub
            case 1:
                embed = nextcord.Embed(title="Belly Rub", description="I approve human. **HP +5**", color =0xFEC04B)
                file = nextcord.File("Images/2.png")
                embed.set_image(url="attachment://2.png")
                global_.happinessPts += 5
                await ctx.send(file=file, embed=embed)
            # pick up 
            case 2:
                embed = nextcord.Embed(title="Pick Up", description="I approve human. **HP +5**", color =0xFEC04B)
                file = nextcord.File("Images/6.png")
                embed.set_image(url="attachment://6.png")
                global_.happinessPts += 5
                await ctx.send(file=file, embed=embed)
            # stretch 
            case 3:
                embed = nextcord.Embed(title="Stretching", description="I approve human. **HP +5**", color =0xFEC04B)
                file = nextcord.File("Images/13.png")
                embed.set_image(url="attachment://13.png")
                global_.happinessPts += 5
                await ctx.send(file=file, embed=embed)
            # hug
            case 4:
                embed = nextcord.Embed(title="Hug", description="I approve human. **HP +5**", color =0xFEC04B)
                file = nextcord.File("Images/17.png")
                embed.set_image(url="attachment://17.png")
                global_.happinessPts += 5
                await ctx.send(file=file, embed=embed)
            # rejected
            case 5:
                embed = nextcord.Embed(title="Nope.", description="You shall suffer the Wrath of the Rock for touching me human **HP -20**", color =0xFEC04B)
                file = nextcord.File("Images/1.png")
                embed.set_image(url="attachment://1.png")
                global_.happinessPts -= 10
                await ctx.send(file=file, embed=embed)

def setup(bot):
    bot.add_cog(Interact_Commands(bot))
    print("2!")