from Entity.Entity import Entity

class Enemy(Entity):
    def __init__(self, jsonInfo):
        super().__init__(jsonInfo["Hp"], jsonInfo["Hpcap"], jsonInfo["Mp"], jsonInfo["Mpcap"], jsonInfo["Name"],
                        jsonInfo["Sprite"], jsonInfo["Lvl"], jsonInfo["Str"], jsonInfo["Mag"], jsonInfo["Vit"],
                        jsonInfo["Agl"], jsonInfo["Def"], jsonInfo["Exp"], jsonInfo["Money"],
                        jsonInfo["Inventory"])
        self.flipped = jsonInfo["flipped"]
        self.moveList = jsonInfo["moveList"]
        self.uniqueBuff = jsonInfo["uniqueBuff"]  # For bosses only really
        self.weakness = jsonInfo["Weakness"]  # What stance they're weak to
        # self.reset_max_animation_val()  # reset the max animation value
        # self.set_image_and_rect()  # set the image and rectangle

    def take_attack(self, damage, lootpool, effect=False):
        # take_attack is the Enemy specific version of `take_damage()`
        # In this case it checks if the attack was fatal and then if it is, invokes the "`die()` function
        damageVal = self.take_damage(damage, effect)
        if self.Status[0] == "Dead":
            self.die(lootpool)
        return damageVal  # returns how much damage the unit took

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
