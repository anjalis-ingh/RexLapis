import nextcord, random, json, global_, sqlite3
from nextcord.ext import commands

def updateMora(value, cur, member):
    cur.execute(f"SELECT mora FROM main WHERE user_id = {member.id}")
    mora = cur.fetchone()
    try:
        mora = mora[0]
    except:
        mora = 0

    sql = ("UPDATE main SET mora = ? WHERE user_id = ?")
    val = (mora + value, member.id)
    cur.execute(sql, val) 

def updateHP(value, cur, member):
    cur.execute(f"SELECT hp FROM main WHERE user_id = {member.id}")
    hp = cur.fetchone()

    try:
        hp = hp[0]
    except:
        hp = 0

    sql = ("UPDATE main SET hp = ? WHERE user_id = ?")
    val = (hp + value, member.id)
    cur.execute(sql, val) 

# -------------- ADD DISH TO INVENTORY --------------
def addDish(itemNum, quantity, cur, member):
    match itemNum:
        case 1:
            cur.execute(f"SELECT soup FROM dishes WHERE user_id = {member.id}")
            soup = cur.fetchone()

            try:
                soup = soup[0]
            except:
                soup = 0

            sql2 = (f"UPDATE dishes SET soup = ? WHERE user_id = ?")
            val2 = (soup + quantity, member.id)
        case 2:
            cur.execute(f"SELECT buns FROM dishes WHERE user_id = {member.id}")
            buns = cur.fetchone()

            try:
                buns = buns[0]
            except:
                buns = 0

            sql2 = (f"UPDATE dishes SET buns = ? WHERE user_id = ?")
            val2 = (buns + quantity, member.id)
        case 3:
            cur.execute(f"SELECT consomme FROM dishes WHERE user_id = {member.id}")
            consomme = cur.fetchone()

            try:
                consomme = consomme[0]
            except:
                consomme = 0

            sql2 = (f"UPDATE dishes SET consomme = ? WHERE user_id = ?")
            val2 = (consomme + quantity, member.id)
        case 4:
            cur.execute(f"SELECT noodles FROM dishes WHERE user_id = {member.id}")
            noodles = cur.fetchone()

            try:
                noodles = noodles[0]
            except:
                noodles = 0

            sql2 = (f"UPDATE dishes SET noodles = ? WHERE user_id = ?")
            val2 = (noodles + quantity, member.id)
        case 5:
            cur.execute(f"SELECT dango FROM dishes WHERE user_id = {member.id}")
            dango = cur.fetchone()

            try:
                dango = dango[0]
            except:
                dango = 0

            sql2 = (f"UPDATE dishes SET dango = ? WHERE user_id = ?")
            val2 = (dango + quantity, member.id)

    cur.execute(sql2, val2)

# initial starting values for variables 
friendshipLvl = 0
happinessLvl = 0
happinessPts = 0
mora = 0

# dishes quantity values 
soup = 0
buns = 0
consomme = 0
noodles = 0
dango = 0

# arrays
inventory = [""]
food = ["", "Bamboo Shoot Soup", "Rice Buns", "Triple Layered Consomme", "Stir Fried Fish Noodle", "Tricolor Dango"]
itemNum = [0, 1, 2, 3, 4, 5]
buyHP = [0, 50, 15, 5, 25, 10]