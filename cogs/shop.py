import nextcord, random, json, global_
from nextcord import Intents
from nextcord.ext import commands

# shop arrays 
prices = [0, 500, 125, 500, 250, 75]
food = ["", "Bamboo Shoot Soup", "Rice Buns", "Triple Layered Consomme", "Stir Fried Fish Noodle", "Tricolor Dango"]
buyHP = [0, 50, 15, 5, 25, 10]

# -------------- SHOP COMMANDS -----------------
class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")  

    # -------------- .buy -------------- 
    @commands.command(name="buy", brief="Buy a shop item by specifying the item # and quantity", description ="Buy a shop item by specifying the item # and quantity." + "Use `.buy <item #> <quantity>`" + " (e.g. `.buy 01 2`)\n")
    async def sendMsg(self, ctx, itemNum: int, quantity: int):
        total = prices[itemNum] * quantity
        if global_.mora > total:
            global_.mora -= total
            await ctx.send("You have successfully bought `" + str(quantity) + " " + food[itemNum] + "`. These will be delivered to Rex Lapis! **HP** **+" + str(buyHP[itemNum]) + "**")
        else:
            await ctx.send("Seems like you are short on Mora! Complete daily commmisions by using `.commission` or try your luck in getting free Mora by using `.pull`")

    # -------------- .shop --------------
    @commands.command(name = "shop", brief ="Displays the shop's inventory of treats and goodies", 
                description = "Displays all of the shop's inventory of items which the user can buy. These items can be purchased and given to Rex Lapis or delivered to other members on the server")
    async def embed(self, ctx):
        embed = nextcord.Embed(title="Welcome to the Wanmin Restaurant!", description="Current Balance: " + str(global_.mora) + " Mora" + " :coin:", color = 0xFEC04B)
        desc2 = (f'{food[1]}\n' f'{food[2]}\n' f'{food[3]}\n' f'{food[4]}\n' f'{food[5]}\n')
        desc3 = (f'{prices[1]}\n' f'{prices[2]}\n' f'{prices[3]}\n' f'{prices[4]}\n' f'{prices[5]}\n')

        embed.add_field(name="__Item #__", value = "1 - :bamboo:\n" "2 - :rice_cracker:\n" "3 - :curry:\n" "4 - :ramen:\n" "5 - :dango:\n", inline=True)
        embed.add_field(name="__Dishes__", value = (desc2), inline=True)
        embed.add_field(name="__Cost__", value = (desc3), inline=True)
        
        embed.add_field(name="How to Buy" + " :moneybag:", value = "Use `.buy <item #> <quantity>`" + " (e.g. `.buy 1 2`)\n", inline=False)

        file = nextcord.File("Images/10.png")
        embed.set_thumbnail(url="attachment://10.png")
        await ctx.send(file=file, embed=embed)

class pullCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # -------------- .pull -------------- 
    @commands.command(name="pull", brief="Try your luck to get a free dish or some mora!", description="Randomized pull where member can get a free dish or a specfic amount of Mora. Can be done every 24 hours.")
    async def sendMsg(self, ctx):
        # pullItems: 10, 20, 50, 75, 100 (Mora), "Bamboo Shoot Soup", "Rice Buns", "Triple Layered Consomme", "Stir Fried Fish Noodle", "Tricolor Dango"
        pullMora = ["", 10, 20, 50, 75, 100]
        num = random.randint(1,10)
        
        if num < 6:
            await ctx.send(f'Congrats, you pulled {pullMora[num]} Mora. Try again tommorow! **Mora + {pullMora[num]}**')
        else:
            await ctx.send(f'Congrats, you pulled a {food[num-5]} dish which will be delivered to Rex Lapis. Try again tommorow! **HP** **+' + str(buyHP[num-5]) + "**")

class balanceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # -------------- .balance -------------- 
    @commands.command(name="balance", brief="Display member's current balance (mora)", description ="Display current amount of mora the member has")
    async def sendMsg(self, ctx):
        await ctx.send("Current Balance: **" + str(global_.mora) + " Mora**")

def setup(bot):
    bot.add_cog(ShopCog(bot))
    bot.add_cog(pullCog(bot))
    bot.add_cog(balanceCog(bot))
    print("Setup Done!")