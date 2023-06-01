import nextcord, random, json, global_, sqlite3
from nextcord.ext import commands

 # shop arrays 
prices = [0, 500, 125, 500, 250, 75]

# -------------- SHOP COMMANDS -----------------
class Shop_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")   

    # -------------- .shop --------------
    @commands.command(name = "shop", brief ="Displays the shop's inventory of treats and goodies", 
                description = "Displays all of the shop's inventory of items which the user can buy. These items can be purchased and given to Rex Lapis or delivered to other members on the server")
    async def embed(self, ctx):
        member = ctx.author
        
        db = sqlite3.connect("main.sqlite")
        cur = db.cursor()
        cur.execute(f"SELECT mora FROM main WHERE user_id = {member.id}")
        mora = cur.fetchone()
        try:
            mora = mora[0]
        except:
            mora = 0 

        embed = nextcord.Embed(title="Welcome to the Wanmin Restaurant!", description="Current Balance: " + str(mora) + " Mora" + " :coin:", color = 0xFEC04B)
        desc2 = (f'{global_.food[1]}\n' f'{global_.food[2]}\n' f'{global_.food[3]}\n' f'{global_.food[4]}\n' f'{global_.food[5]}\n')
        desc3 = (f'{prices[1]}\n' f'{prices[2]}\n' f'{prices[3]}\n' f'{prices[4]}\n' f'{prices[5]}\n')

        embed.add_field(name="__Item #__", value = "1 - :bamboo:\n" "2 - :rice_cracker:\n" "3 - :curry:\n" "4 - :ramen:\n" "5 - :dango:\n", inline=True)
        embed.add_field(name="__Dishes__", value = (desc2), inline=True)
        embed.add_field(name="__Cost__", value = (desc3), inline=True)
        
        embed.add_field(name="How to Buy" + " :moneybag:", value = "Use `.buy <item #> <quantity>`" + " (e.g. `.buy 1 2`)\n", inline=False)

        file = nextcord.File("Images/10.png")
        embed.set_thumbnail(url="attachment://10.png")
        await ctx.send(file=file, embed=embed)
    
    # -------------- .buy -------------- 
    @commands.command(name="buy", brief="Buy a shop item by specifying the item # and quantity", description ="Buy a shop item by specifying the item # and quantity." + "Use `.buy <item #> <quantity>`" + " (e.g. `.buy 01 2`)\n")
    async def buyFood(self, ctx, itemNum: int, quantity: int):
        member = ctx.author
        total = prices[itemNum] * quantity

        db = sqlite3.connect("main.sqlite")
        cur = db.cursor()
        cur.execute(f"SELECT mora FROM main WHERE user_id = {member.id}")
        mora = cur.fetchone()

        try:
            mora = mora[0]
        except:
            mora = 0

        if mora >= total:
            sql = ("UPDATE main SET mora = ? WHERE user_id = ?")
            val = (mora - total, member.id)
            cur.execute(sql, val)
            
            global_.addDish(itemNum, quantity, cur, member)
            await ctx.send("You have successfully bought `" + str(quantity) + " " + global_.food[itemNum] + "`. These item(s) are now in your inventory! (`.inventory`) :yum:")
        else:
            await ctx.send("Seems like you are short on Mora! Complete daily commmisions by using `.commission` or try your luck in getting free Mora by using `.pull`")

        db.commit()
        cur.close()
        db.close()

    # -------------- .balance -------------- 
    @commands.command(name="balance", brief="Display member's current balance (mora)", description ="Display current amount of mora the member has")
    async def findBalance(self, ctx, member:nextcord.Member = None):
        if member is None:
            member = ctx.author 
        
        db = sqlite3.connect("main.sqlite")
        cur = db.cursor()
        cur.execute(f"SELECT mora FROM main WHERE user_id = {member.id}")
        mora = cur.fetchone()
        try:
            mora = mora[0]
        except:
            mora = 0
        
        await ctx.send(f"Current Balance: **{mora} Mora** :purse:")

    # -------------- .pull -------------- 
    @commands.command(name="pull", brief="Try your luck to get a free dish or some mora!", description="Randomized pull where member can get a free dish or a specfic amount of Mora. Can be done every 24 hours.")
    async def pullItems(self, ctx):
        member = ctx.author

        # pullItems: 10, 20, 50, 75, 100 (Mora), "Bamboo Shoot Soup", "Rice Buns", "Triple Layered Consomme", "Stir Fried Fish Noodle", "Tricolor Dango"
        pullMora = ["", 10, 20, 50, 75, 100]
        num = random.randint(1,10)

        db = sqlite3.connect("main.sqlite")
        cur = db.cursor()
        
        if num < 6:
            global_.updateMora(pullMora[num], cur, member)   
            await ctx.send(f'Congrats, you pulled {pullMora[num]} Mora. Try again tommorow! **Mora + {pullMora[num]}**')
        else:            
            global_.addDish(global_.itemNum[num-5], 1, cur, member)
            await ctx.send(f'Congrats, you pulled a {global_.food[num-5]} dish! You can view this in `.inventory`. Try again tommorow!')
        
        db.commit()
        cur.close()
        db.close()
    
    # -------------- .inventory -------------- 
    @commands.command(name="inventory", brief="View all of your dishes here", description="Any dishes bought from the store or earned by pull can be viewed here")
    async def invItems(self, ctx, member:nextcord.Member = None):
        if member is None:
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

        desc0 = (f'{global_.itemNum[1]}\n' f'{global_.itemNum[2]}\n' f'{global_.itemNum[3]}\n' f'{global_.itemNum[4]}\n' f'{global_.itemNum[5]}\n')
        desc1 = (f'{global_.food[1]}\n' f'{global_.food[2]}\n' f'{global_.food[3]}\n' f'{global_.food[4]}\n' f'{global_.food[5]}\n')
        desc2 = (f'{soup}\n' f'{buns}\n' f'{consomme}\n' f'{noodles}\n' f'{dango}\n')

        embed = nextcord.Embed(title = "Inventory", description="", color = 0xFEC04B)
        embed.add_field(name="__Item #__", value = (desc0), inline=True)
        embed.add_field(name="__Dishes__", value = (desc1), inline=True)
        embed.add_field(name = "__Quantity__", value = (desc2), inline =True)
        embed.add_field(name="Want to give Rex Lapis a treat?" + " :cookie:", value = "Use `.feed <item #> <quantity>`" + " (e.g. `.feed 1 2`)\n", inline=False)

        file = nextcord.File("Images/8.png")
        embed.set_thumbnail(url="attachment://8.png")
        await ctx.send(file=file, embed=embed)

def setup(bot):
    bot.add_cog(Shop_Commands(bot))
    print("1!")