from Entity.Entity import Entity

class Enemy(Entity):
    def __init__(self, Hp, Hpcap, name, level, strength, vitality, agility, defence, exp, money, inventory, weakness,
                 uniquebuff=None):
        Entity.__init__(Hp, Hpcap, name, level, strength, vitality, agility, defence, exp, money, inventory)
        self.uniqueBuff = uniquebuff  # For bosses only really
        self.weakness = weakness  # What stance they're weak to

    def die(self, lootPool):  # Will not work
        # add values to loot pool upon death
        # None of these should be None
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
        lootPool.update({"Exp": experience + self.Exp})
        lootPool.update({"Money": money + self.Bal})
        lootPool.update({"Items": itemDict})


