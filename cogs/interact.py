import nextcord, random, json, global_, sqlite3
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
                 "4. **.gift <amount>** - feeling generous? gift Rex Lapis some mora to help out the broke dragon\n\n"
        )

        embed = nextcord.Embed(title = "Interact with Rex Lapis!", description= (desc1), color=0xFEC04B)   
        file = nextcord.File("Images/21.png")
        embed.set_image(url="attachment://21.png")
        await ctx.send(file=file, embed=embed)

     # -------------- .feed -------------- 
    @commands.command(name="feed", brief="Feed Rex Lapis with dishes bought from the shop, yum!", description="Feed Rex Lapis with treats bought from the shop or earned through pulls")
    async def feedGod(self, ctx, itemNum: int, quantity: int):
        member = ctx.author
        db = sqlite3.connect("main.sqlite")
        cur = db.cursor()
        cur.execute(f"SELECT soup, buns, consomme, noodles, dango FROM dishes WHERE user_id = {member.id}")
        inv = cur.fetchone()

        try:
            soup = inv[0]
            buns = inv[1]
            consomme = inv[2]
            noodles = inv[3]
            dango = inv[4]
        except:
            soup = 0
            buns = 0
            consomme = 0
            noodles = 0
            dango = 0

        num = 0

        match itemNum:
            case 1:
                cur.execute(f"SELECT soup FROM dishes WHERE user_id = {member.id}")
                soup = cur.fetchone()

                try:
                    soup = soup[0]
                except:
                    soup = 0 
                if soup >= quantity:
                    num = 1
            case 2:
                cur.execute(f"SELECT buns FROM dishes WHERE user_id = {member.id}")
                buns = cur.fetchone()

                try:
                    buns = buns[0]
                except:
                    buns = 0
                if buns >= quantity:
                    num = 1
            case 3:
                cur.execute(f"SELECT consomme FROM dishes WHERE user_id = {member.id}")
                consomme = cur.fetchone()

                try:
                    consomme = consomme[0]
                except:
                    consomme = 0
                if consomme >= quantity:
                    num = 1
            case 4:
                cur.execute(f"SELECT noodles FROM dishes WHERE user_id = {member.id}")
                noodles = cur.fetchone()

                try:
                    noodles = noodles[0]
                except:
                    noodles = 0
                if noodles >= quantity:
                    num = 1
            case 5:
                cur.execute(f"SELECT dango FROM dishes WHERE user_id = {member.id}")
                dango = cur.fetchone()

                try:
                    dango = dango[0]
                except:
                    dango = 0
                if dango >= quantity:
                    num = 1

        if num == 1:
            if itemNum == 1:
                embed = nextcord.Embed(title = "Delivered!", description="Ah I see you got my favorite dish! When heated, slowly, gently, and with the utmost care and technique...Such a particular taste may only be shared with those who know how to appreciate it. **HP** **+" + str(global_.buyHP[itemNum] * quantity * 2) + "** :coffee:", color=0xFEC04B)
                value = global_.buyHP[itemNum] * quantity * 2
                global_.updateHP(value, cur, member)
            else:
                embed = nextcord.Embed(title = "Delivered!", description="This is quite delicious, thank you friend. We should get a quick meal to pick us back up later on. I know a good place in Chihu Rock! **HP** **+" + str(global_.buyHP[itemNum] * quantity) + "** :coffee:", color=0xFEC04B)
                value = global_.buyHP[itemNum] * quantity 
                global_.updateHP(value, cur, member)

            global_.addDish(itemNum, -quantity, cur, member)  
            global_.flUpdate(cur, member)  
            global_.hlUpdate(cur, member)
            file = nextcord.File("Images/8.png")
            embed.set_image(url="attachment://8.png")
            await ctx.send(file=file, embed=embed)

            db.commit()
            cur.close()
            db.close()
        else:
            await ctx.send("Appreciate it but seems like the dish you requested is either not in your inventory or you don't have enough. If you want to buy some more food, go to `.shop` and use `.buy <item #> <quantity>` to buy your desired items!")
    
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
        cur.execute(f"SELECT mora, hp FROM main WHERE user_id = {member.id}")
        bal = cur.fetchone()

        try:
            mora = bal[0]
            hp = bal[1]
        except:
            mora = 0
            hp = 0
        
        if mora >= amount:
            sql = ("UPDATE main SET mora = ?, hp = ? WHERE user_id = ?")
            val = (mora - amount, hp + amount, member.id)
            cur.execute(sql, val) 
            global_.flUpdate(cur, member)  
            global_.hlUpdate(cur, member)

            file = nextcord.File("Images/9.png")
            embed.set_image(url="attachment://9.png")
            await ctx.send(file=file, embed=embed)
        else:
            await ctx.send("Appreciate the gesture, but it seems like you are broke like me :broken_heart: You can earn mora through playing `.games` or other interactions.")

        db.commit()
        cur.close()
        db.close()
    
    # -------------- .pet -------------- 
    @commands.command(name="pet", brief="Hug, belly rub, or even cuddle with rex lapis if you dare to...", description = "Hug, belly rub, or even cuddle with rex lapis if you dare to...he may or may not like the gesture. HL can be increased or decreased through this interaction. Can be done twice every hour")
    @commands.cooldown(2, 3600, commands.BucketType.user)
    async def pet(self, ctx):
        member = ctx.author
        db = sqlite3.connect("main.sqlite")
        cur = db.cursor()

        randomNum = random.randint(1,5)
        match randomNum:
            # belly rub
            case 1:
                embed = nextcord.Embed(title="Belly Rub", description="I approve human. **HP +5**", color =0xFEC04B)
                file = nextcord.File("Images/2.png")
                embed.set_image(url="attachment://2.png")
                global_.updateHP(5, cur, member)
                await ctx.send(file=file, embed=embed)
            # pick up 
            case 2:
                embed = nextcord.Embed(title="Pick Up", description="I approve human. **HP +5**", color =0xFEC04B)
                file = nextcord.File("Images/6.png")
                embed.set_image(url="attachment://6.png")
                global_.updateHP(5, cur, member)
                await ctx.send(file=file, embed=embed)
            # stretch 
            case 3:
                embed = nextcord.Embed(title="Stretching", description="I approve human. **HP +5**", color =0xFEC04B)
                file = nextcord.File("Images/13.png")
                embed.set_image(url="attachment://13.png")
                global_.updateHP(5, cur, member)
                await ctx.send(file=file, embed=embed)
            # hug
            case 4:
                embed = nextcord.Embed(title="Hug", description="I approve human. **HP +5**", color =0xFEC04B)
                file = nextcord.File("Images/17.png")
                embed.set_image(url="attachment://17.png")
                global_.updateHP(5, cur, member)
                await ctx.send(file=file, embed=embed)
            # rejected
            case 5:
                embed = nextcord.Embed(title="Nope.", description="You shall suffer the Wrath of the Rock for touching me human **HP -10**", color =0xFEC04B)
                file = nextcord.File("Images/1.png")
                embed.set_image(url="attachment://1.png")
                global_.updateHP(-10, cur, member)
                await ctx.send(file=file, embed=embed)

        global_.flUpdate(cur, member)  
        global_.hlUpdate(cur, member)
        db.commit()
        cur.close()
        db.close()

    # error message for pet command
    @pet.error
    async def pet_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'I do not wish to be touched anymore human, that is quite enough for nowTry again in {round(error.retry_after, 1)} seconds.')

def setup(bot):
    bot.add_cog(Interact_Commands(bot))