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
    def __init__(self, Hp=1, HPcap=1, Mp=1, Mpcap=1, name="Rion", level=1, strength=1, vitality=1, agility=1, defence=1, exp=0, expcap=1, money=0):
        Entity.__init__(self, Hp, HPcap, Mp, Mpcap, name, level, strength, vitality, agility, defence, exp, money)
        self.Expcap = expcap
        self.Stance = "1"
        self.growths = {"Hpcap": self.Vit * 1 + 50, "Str": self.Str * 1 + 50, "Vit": self.Vit * 1 + 50,
                        "Agl": self.Agl * 1 + 50, "Defence": self.Defence + 50}
        self.moveList = ["Attack"]

    def level_up(self):
        # add to stats
        knightDict = self.__dict__
        for stat, growth in self.growths.items():
            knightDict[stat] = knightDict[stat] + growth
        # Reset growths to incorperate new stats
        self.growths = {"Hpcap": self.Vit * 1 + 50, "Str": self.Str * 1 + 50, "Vit": self.Vit * 1 + 50,
                        "Agl": self.Agl * 1 + 50, "Defence": self.Defence + 50}
        while self.Exp >= self.Expcap:  # Account for the potential multiple level up
            self.Lvl += 1  # increase the level for each level up
            self.Exp -= self.Expcap  # Decrease the Exp of the player to prevent multiple level ups
            self.Expcap += 50  # increase Expcap for each level up

    # Function that's called at the end of a fight for BattleManager
    def get_rewards(self, lootPool):
        experience = lootPool.get("Exp")
        money = lootPool.get("Money")
        itemDict = lootPool.get("Items")
        # For loop can become a function when directory structure is done
        for key in itemDict:
            if self.Inventory.get(key) is not None:  # sees if there is already an entry to update
                number = itemDict.get(key)  # How many of the item is in the actual inventory
                self.Inventory.update({key: number + self.Inventory[key]})  # add drop amount to the loot pool
            else:
                self.Inventory.update({key: itemDict[key]})  # Add the key to the loot pool if not already in
        self.Bal += money       # Add the money gained to the players balance
        self.Exp += experience  # Add the experience to the players Exp bar
        self.level_up()  # see if the player leveled up

    # turning the inventory dictionary into a list
    def inventory_to_list(self):
        itemList = []
        for item, amount in self.Inventory.items():
            itemList.append(item + " x" + str(amount))
        return itemList

    # Loads the Knight characters stats based on a given dictionary
    def load_dict(self, knightDict):
        self.__dict__ = knightDict
