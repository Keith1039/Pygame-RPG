from Entity.Entity import Entity

class Enemy(Entity):
    def __init__(self, jsonInfo):
        Entity.__init__(self, jsonInfo["Hp"], jsonInfo["Hpcap"], jsonInfo["Mp"], jsonInfo["Mpcap"], jsonInfo["Name"],
                        jsonInfo["Lvl"], jsonInfo["Str"], jsonInfo["Vit"],
                        jsonInfo["Agl"], jsonInfo["Defence"], jsonInfo["Exp"], jsonInfo["Money"],
                        jsonInfo["Inventory"])
        self.moveList = jsonInfo["moveList"]
        self.uniqueBuff = jsonInfo["uniqueBuff"]  # For bosses only really
        self.weakness = jsonInfo["Weakness"]  # What stance they're weak to

    def take_attack(self, damage, lootpool):  # take_attack is the Enemy specific version of `take_damage()`
        # In this case it checks if the attack was fatal and then if it is, invokes the "`die()` function
        self.take_damage(damage)
        if self.Status == "Dead":
            self.die(lootpool)
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


