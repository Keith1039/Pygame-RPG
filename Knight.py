weapons = {"sword":10,"poisoned sword":12,"silver sword":20,"rusty dagger":1,"poisoned rusty dagger":2,"lance":5,"silver lance":10,"???":999999,"unarmed":3}
items_shop_list = ["old map", "old bread","potion"]
items_shop = {"old map":1000,"old bread":50,"potion":150,"moonstone":300,"silver polish":50}
items_sell = {"sword":100, "lance":80,"old bread":10, "potion":50, "rusty dagger":20,"silver lance":100,"silver sword":150}
books = ['Gospel of the dragons',"History book" "Ruined journal #1","Ruined journal #2", "Ruined journal #3", "Demons", "old book", "Items"]
items = {"Volatile Poison","silver polish","emblem","moonlit map",'Gospel of the dragons', "Ruined journal #1","Ruined journal #2", "Ruined journal #3", "Werewolf tooth"
"Demons", "old book","History book", "Items","moonstone","basement key", "upstairs key"}
combinable_items = ["Volitile poison", "silver polish","lance", "rusty dagger", "sword", "old map", "moonstone"]
consumable_item = {"old bread":20,"potion":50}
inventory = []

# Statuses: Normal or In-Combat or Dead or opening_chest
class Knight:
    # The current stats still need to be changed to the default stats later
    def __init__(self, name="Rion", level=1, strength=1, vitality=1, Hp=1, HPcap=1, agility=1, defence=1, exp=1, expcap=1, money=1):
        self.Hp = Hp
        self.Hpcap = HPcap
        self.Mp = 1     # deal with this later when you're doing battle manager
        self.Mpcap = 1  # deal with this later when you're doing battle manager
        self.Name = name
        self.Lvl = level
        self.Str = strength
        self.Vit = vitality
        self.Agl = agility
        self.Status = "Normal" 
        self.Stance = "1"
        self.Defence = defence
        self.Exp = exp
        self.Expcap = expcap
        self.Bal = money

    # Loads the Knight characters stats based on a given dictionary
    def load_dict(self, knightDict):
        self.Hp = knightDict["Hp"]
        self.Hpcap = knightDict["Hpcap"]
        self.Name = knightDict["Name"]
        self.Lvl = knightDict["Lvl"]
        self.Str = knightDict["Str"]
        self.Vit = knightDict["Vit"]
        self.Agl = knightDict["Agl"]
        self.Status = knightDict["Status"]
        self.Stance = knightDict["Stance"]
        self.Defence = knightDict["Defence"]
        self.Exp = knightDict["Exp"]
        self.Expcap = knightDict["Expcap"]
        self.Bal = knightDict["Bal"]
