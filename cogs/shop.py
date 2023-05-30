import nextcord, random, json, global_
from nextcord import Intents
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
        embed = nextcord.Embed(title="Welcome to the Wanmin Restaurant!", description="Current Balance: " + str(global_.mora) + " Mora" + " :coin:", color = 0xFEC04B)
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
        total = prices[itemNum] * quantity
        if global_.mora > total:
            global_.mora -= total
            await ctx.send("You have successfully bought `" + str(quantity) + " " + global_.food[itemNum] + "`. These item(s) are now in your inventory! (`.inventory`) :yum:")
            for i in range(0, quantity):
                global_.inventory.append(global_.food[itemNum])
        else:
            await ctx.send("Seems like you are short on Mora! Complete daily commmisions by using `.commission` or try your luck in getting free Mora by using `.pull`")

    # -------------- .balance -------------- 
    @commands.command(name="balance", brief="Display member's current balance (mora)", description ="Display current amount of mora the member has")
    async def findBalance(self, ctx):
        await ctx.send("Current Balance: **" + str(global_.mora) + " Mora** :purse:")

    # -------------- .pull -------------- 
    @commands.command(name="pull", brief="Try your luck to get a free dish or some mora!", description="Randomized pull where member can get a free dish or a specfic amount of Mora. Can be done every 24 hours.")
    async def pullItems(self, ctx):
        # pullItems: 10, 20, 50, 75, 100 (Mora), "Bamboo Shoot Soup", "Rice Buns", "Triple Layered Consomme", "Stir Fried Fish Noodle", "Tricolor Dango"
        pullMora = ["", 10, 20, 50, 75, 100]
        num = random.randint(1,10)
        
        if num < 6:
            await ctx.send(f'Congrats, you pulled {pullMora[num]} Mora. Try again tommorow! **Mora + {pullMora[num]}**')
            global_.mora += pullMora[num]
        else:
            await ctx.send(f'Congrats, you pulled a {global_.food[num-5]} dish! You can view this in `.inventory`. Try again tommorow! **HP** **+' + str(global_.buyHP[num-5]) + "**")
            global_.inventory.append(global_.food[num-5])
            global_.happinessPts += global_.buyHP[num-5]
    
    # -------------- .inventory -------------- 
    @commands.command(name="inventory", brief="View all of your dishes here", description="Any dishes bought from the store or earned by pull can be viewed here")
    async def invItems(self, ctx):
        desc1 = (f'{global_.food[1]}\n' f'{global_.food[2]}\n' f'{global_.food[3]}\n' f'{global_.food[4]}\n' f'{global_.food[5]}\n')
        desc2 = (f'{global_.inventory.count(global_.food[1])}\n' f'{global_.inventory.count(global_.food[2])}\n' f'{global_.inventory.count(global_.food[3])}\n'
                 f'{global_.inventory.count(global_.food[4])}\n' f'{global_.inventory.count(global_.food[5])}\n'
        )

        embed = nextcord.Embed(title = "Inventory", description="", color = 0xFEC04B)
        embed.add_field(name="__Item #__", value = "1\n" "2\n" "3\n" "4\n" "5\n", inline=True)
        embed.add_field(name="__Dishes__", value = (desc1), inline=True)
        embed.add_field(name = "__Quantity__", value = (desc2), inline =True)
        embed.add_field(name="Want to give Rex Lapis a treat?" + " :cookie:", value = "Use `.feed <item #> <quantity>`" + " (e.g. `.feed 1 2`)\n", inline=False)

        file = nextcord.File("Images/8.png")
        embed.set_thumbnail(url="attachment://8.png")
        await ctx.send(file=file, embed=embed)

def setup(bot):
    bot.add_cog(Shop_Commands(bot))
    print("Setup Done!")