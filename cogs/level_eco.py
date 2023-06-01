import nextcord, json, global_, sqlite3
from nextcord.ext import commands

class Level_Eco_System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener("on_ready")
    async def listen1(self):
        db = sqlite3.connect("main.sqlite")
        cur = db.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS main (user_id INTEGER, mora INTEGER, hp INTEGER, level INTEGER)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS dishes (user_id INTEGER, soup INTEGER, buns INTEGER, consomme INTEGER, noodles INTEGER, dango INTEGER)''')
    
    @commands.Cog.listener("on_message")
    async def listen2(self, message):
        if message.author.bot:
            return 
        
        author = message.author
        db = sqlite3.connect("main.sqlite")
        cur = db.cursor()

        cur.execute(f"SELECT user_id FROM main WHERE user_id = {author.id}")
        result = cur.fetchone()
        if result is None:
            sql = ("INSERT INTO main(user_id, mora, hp, level) VALUES (?, ?, ?, ?)")
            val = (author.id, global_.mora, global_.happinessPts, global_.happinessLvl)
            cur.execute(sql, val)
        
        cur.execute(f"SELECT user_id FROM dishes WHERE user_id = {author.id}")
        result = cur.fetchone()
        if result is None:
            sql2 = ("INSERT INTO dishes(user_id, soup, buns, consomme, noodles, dango) VALUES (?, ?, ?, ?, ?, ?)")
            val2 = (author.id, global_.soup, global_.buns, global_.consomme, global_.noodles, global_.dango)
            cur.execute(sql2, val2)

        db.commit()
        cur.close()
        db.close()


def setup(bot):
    bot.add_cog(Level_Eco_System(bot))
    print("3!")