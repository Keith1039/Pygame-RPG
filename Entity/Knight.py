import pygame as game
from Entity.Entity import Entity

# Statuses: Normal or In-Combat or Dead or opening_chest
class Knight(Entity):
    # The current stats still need to be changed to the default stats later
    def __init__(self, Hp=1, Hpcap=1, Mp=1, Mpcap=1, name="Knight", sprite="Entity_Sprites/Knight/", level=1, strength=1, magic=1, vitality=1, agility=1, defence=1, exp=0, expcap=1, money=0):
        super().__init__(Hp, Hpcap, Mp, Mpcap, name, sprite, level, strength, magic, vitality, agility, defence, exp, money)
        self.fieldStatus = "Normal"  # indicator for the knight class
        self.reset_max_animation_val()  # set the limit
        self.default_x = 0  # default x value
        self.default_y = 590  # default y value 350 works for battles
        self.x = self.default_x  # set the x value
        self.y = self.default_y  # set the y value
        self.flipped = False  # determines whether the sprite is inverted or not
        self.image = None
        self.rect = None
        self.set_image_and_rect()  # set the image and rectangle variables
        self.Expcap = expcap
        self.Stance = "1"
        self.growths = {
            "Hpcap": self.Vit * 1 + 50, "Mpcap": self.Mpcap * 1 + 50, "Str": self.Str * 1 + 50,
            "Vit": self.Vit * 1 + 50, "Agl": self.Agl * 1 + 50, "Def": self.Def + 50
        }
        self.moveList = ["Attack"]
        self.equipment = {
            "Weapon": None,
            "Helmet": None,
            "Chestplate": None,
            "Shoes": None,
            "Accessory": None
        }

    def set_image_and_rect(self):
        spot = str((self.aniTracker // 10) + 1)  # the frame of the animation
        if self.aniTracker == -1:  # check if we have a -1
            spot = str(self.maxAniVal)  # set the spot to the max
        filePath = self.Sprite + self.Name + "_" + self.aniStatus + "_" + spot + ".png"  # create the file path
        self.image = game.image.load(filePath)  # load the new image
        if self.flipped:  # if the run is to be flipped
            self.image = game.transform.flip(self.image, True, False)  # flip across y axis
        self.image = game.transform.scale(self.image, (450, 300))  # scale the image
        self.rect = self.image.get_rect()  # get the new rectangle
        self.rect.center = (self.x, self.y)  # center the rectangle to the players coordinates

    def update(self, force=False):
        # this behavior is for overworld behavior
        if self.aniTracker != -1:  # -1 means that the animation is stuck for it
            self.aniTracker += 1  # increment the tracker
        if self.aniTracker % 10 == 0 or force:  # every 10 frames we shift the animation or if we force it
            update = False  # indicator for if an update is needed
            if (self.aniTracker // 10) + 1 > self.maxAniVal and self.aniStatus == "Death":
                self.aniTracker = -1  # set it so that it can't change
            elif (self.aniTracker // 10) + 1 > self.maxAniVal:
                self.aniTracker = 0  # reset animation timer
                update = True  # indicate that an update is needed
            elif (self.aniTracker // 10) + 1 <= self.maxAniVal:
                update = True  # indicate that an update is needed
            if update:
                self.set_image_and_rect()  # sets the image and the rectangle

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
                        "Agl": self.Agl * 1 + 50, "Def": self.Def + 50}
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
        self.add_all_to_inventory(itemDict)
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

    def add_all_to_inventory(self, itemDict):
        for key, number in itemDict.items():  # add all items from loot pool to inventory
            self.add_to_inventory(key, number)

    def add_to_inventory(self, item, amount=1):
        # if the item isn't in the inventory, add an entry
        if self.Inventory.get(item) is None:
            self.Inventory.update({item: amount})
        else:
            # if the item is in the inventory, add to the amount present
            capacity = self.Inventory[item]
            self.Inventory.update({item: capacity + amount})

    def remove_from_inventory(self, item, amount=1):
        # removes a certain amount for a specific item
        capacity = self.Inventory[item]
        self.Inventory.update({item: capacity - amount})
        self.correct_inventory()
    # Loads the Knight characters stats based on a given dictionary

    def load_dict(self, knightDict):
        self.__dict__.update(knightDict)
        self.reset_max_animation_val()  # reset the max animation value
        self.set_image_and_rect()  # sets the image and the rectangle
        self.Status = tuple(self.Status)  # turn status back into a tuple
        self.moveList = list(self.moveList)  # turn the tuple back into a list

    def equals(self, other):
        fields = ["fieldStatus", "aniStatus", "aniTracker", "x", "y", "flipped", "Name", "Sprite", "Status",
            "Lvl", "Hpcap", "Hp", "Mpcap", "Mp", "Exp", "Bal", "Str", "Mag", "Vit", "Agl", "Def", "moveList",
            "equipment", "Inventory"]
        flag = True
        for key in fields:
            flag = self.__dict__[key] == other.__dict__[key]
            if not flag:
                print(key)
                break
        return flag
