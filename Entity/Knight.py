from Entity.Entity import Entity

# Statuses: Normal or In-Combat or Dead or opening_chest
class Knight(Entity):
    # The current stats still need to be changed to the default stats later
    def __init__(self, Hp=1, Hpcap=1, Mp=1, Mpcap=1, name="Rion", level=1, strength=1, magic=1, vitality=1, agility=1, defence=1, exp=0, expcap=1, money=0):
        Entity.__init__(self, Hp, Hpcap, Mp, Mpcap, name, level, strength, magic, vitality, agility, defence, exp, money)
        self.Expcap = expcap
        self.Stance = "1"
        self.growths = {"Hpcap": self.Vit * 1 + 50, "Mpcap": self.Mpcap * 1 + 50, "Str": self.Str * 1 + 50, "Vit": self.Vit * 1 + 50,
                        "Agl": self.Agl * 1 + 50, "Defence": self.Defence + 50}
        self.moveList = ["Attack"]
        self.equipment = {
            "Weapon": None,
            "Helmet": None,
            "Chestplate": None,
            "Shoes": None,
            "Accessory": None
        }

    def level_up(self):
        # add to stats
        knightDict = self.__dict__
        for stat, growth in self.growths.items():
            knightDict[stat] = knightDict[stat] + growth
            if stat.find("cap") != -1 and stat.find("exp") == -1:  # if it's a cap of some sort and isn't expCap
                newStat = stat[0:2]  # take the first 2 letters of the string
                knightDict[newStat] = knightDict[newStat] + growth  # add to the stat too

        # Reset growths to incorperate new stats
        self.growths = {"Hpcap": self.Vit * 1 + 50, "Mpcap": self.Mpcap * 1 + 50, "Str": self.Str * 1 + 50, "Vit": self.Vit * 1 + 50,
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
            if amount > 1:
                itemList.append(item + " x" + str(amount))
            else:
                itemList.append(item)
        return itemList

    def correct_inventory(self):
        # function to remove items that have an amount of, i.e. items the player doesn't have anymore
        deletableItems = []
        # add the key to the list
        for item, amount in self.Inventory.items():
            if amount == 0:
                deletableItems.append(item)
        # pop all items in the list from inventory
        for i in range(len(deletableItems)):
            self.Inventory.pop(deletableItems[i])

    def equip(self, equipment, remove=False):
        if not remove:
            if self.equipment.get(equipment.type) is not None:
                self.equipment[equipment.type].remove_stat_bonuses(self)
            equipment.apply_stat_bonuses(self)
            self.equipment.update({equipment.type: equipment})
        else:
            self.equipment[equipment.type].remove_stat_bonuses(self)  # remove the buffs from player
            self.equipment.update({equipment.type: None})  # replaces the current equipment slot with None
        self.correct_stats()  # correct the stats
    # Loads the Knight characters stats based on a given dictionary
    def load_dict(self, knightDict):
        self.__dict__ = knightDict

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

