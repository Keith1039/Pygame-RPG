from Entity.Entity import Entity
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
class Knight(Entity):
    # The current stats still need to be changed to the default stats later
    def __init__(self, Hp=1, HPcap=1, name="Rion", level=1, strength=1, vitality=1, agility=1, defence=1, exp=1, expcap=1, money=1):
        Entity.__init__(self, Hp, HPcap, name, level, strength, vitality, agility, defence, exp, money)
        self.Mp = 1     # deal with this later when you're doing battle manager
        self.Mpcap = 1  # deal with this later when you're doing battle manager
        self.Expcap = expcap
        self.Stance = "1"
        # self.growths = []

    def level_up(self):
        # add to stats
        # Recalculate health via vitality stat
        self.Exp = self.Exp - self.Expcap  # level_up is only called when self.Exp is greater or equal to self.Expcap

    # Function that's called at the end of a fight for BattleManager
    def get_rewards(self, lootPool):
        experience = lootPool.get("Exp")
        money = lootPool.get("Money")
        itemDict = lootPool.get("Items")
        # For loop can become a function when directory structure is done
        for key in self.Inventory:
            if itemDict.get(key) is not None:  # sees if there is already an entry to update
                number = itemDict.get(key)  # How many of the item is in the actual inventory
                itemDict.update({key: number + self.Inventory[key]})  # add drop amount to the loot pool
            else:
                itemDict.update({key: self.Inventory[key]})  # Add the key to the loot pool if not already in
        self.Bal += money
        self.Exp += experience
        while self.Exp >= self.Expcap:  # Account for the potential multiple level up
            self.level_up()

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
