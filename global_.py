import nextcord, random, json, global_, sqlite3, math
from nextcord.ext import commands

# -------------- check for friendship level updates --------------
def flUpdate(cur, member):
    cur.execute("SELECT hp FROM main")
    data = cur.fetchall()
    tot = 0
    for row in data:
        tot += row[0]
        
    current = math.floor(tot/100)
    if current >  global_.friendshipLvl:
        global_.friendshipLvl = current

# -------------- check for happiness level updates --------------
def hlUpdate(cur, member):
    cur.execute(f"SELECT hp, level FROM main WHERE user_id = {member.id}")
    data = cur.fetchone()
    try:
        hp = data[0]
        level = data[1]
    except:
        hp = 0
        level = 0
    value = math.floor(hp/50)
    if value > level:
        sql = ("UPDATE main SET level = ? WHERE user_id = ?")
        val = (value, member.id)
        cur.execute(sql, val) 

# -------------- update member's current balance (mora) --------------
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

# -------------- update happiness points --------------
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
food = ["", "Bamboo Shoot Soup", "Rice Buns", "Triple Layered Consomme", "Stir Fried Fish Noodle", "Tricolor Dango"]
itemNum = [0, 1, 2, 3, 4, 5]
buyHP = [0, 50, 15, 5, 25, 10]