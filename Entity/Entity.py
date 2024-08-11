# Parent class of hero and monster classes. Saves me the trouble of re-writing a
# bunch of code
class Entity:
    def __init__(self, Hp, Hpcap, Mp, Mpcap, name, sprite, level, strength, magic, vitality, agility, defence, exp, money, inventory=None):
        if inventory is None:
            inventory = {}  # Inventory is a dictionary of it with key pairs (string: int)
        self.Name = name
        self.Sprite = sprite
        self.Status = ("Normal", -1)
        self.Lvl = level
        self.Hpcap = Hpcap
        self.Hp = Hp
        self.Mpcap = Mpcap
        self.Mp = Mp
        self.Exp = exp
        self.Bal = money
        self.Str = strength
        self.Mag = magic
        self.Vit = vitality
        self.Agl = agility
        self.Def = defence
        self.Bonuses = {  # A dict of all positive and negative effects on Knight character, includes stance bonuses
            "Str": (0, -1), "Vit": (0, -1), "Agl": (0, -1), "Def": (0, -1)  # -1 means unlimited duration for bonus
        }
        self.Inventory = inventory  # For heroes, it's a bunch of useful items, for monsters it's dropped items

    def take_damage(self, damage, effect=False):
        if not effect:  # if it isn't effect damage, consider defence
            damage = damage - self.Def  # how much damage you ACTUALLY take
        if damage > 0 and self.Status[0] != "Dead":  # Only allows positive damage to be inflicted on alive opponents
            self.Hp -= damage
            if self.Hp <= 0:  # Check if you died to the attack
                self.Hp = 0  # Set hp to 0 or else weird things will start happening
                self.Status = ("Dead", -1)  # Change status to dead
            return damage
        return 0  # if the damage is below 0

    def apply_bonuses(self, flag=True):
        # flag being False stops the turn count from lowering
        # applies the bonus to the relevant stat
        # Only one bonus can be applied to a stat at a time leading to some interesting strats...
        knightDict = self.__dict__  # This is a horrible idea... still doing it
        for stat, bonusInfo in self.Bonuses.items():
            bonus = bonusInfo[0]
            turnCount = bonusInfo[1]
            knightDict.update({stat: knightDict[stat] + bonus})
            if turnCount != -1 and flag:  # If it isn't an infinite buff then decrement counter
                self.Bonuses.update({stat: (bonus, turnCount - 1)})  # Add the updated turn count to bonuses dict

    def remove_bonuses(self, flag=True):
        # flag being False stops the removal of buffs
        # Removes any buff effect at the end of turn so buff effects don't linger
        knightDict = self.__dict__  # This is a horrible idea... still doing it
        for stat, bonusInfo in self.Bonuses.items():
            bonus = bonusInfo[0]
            turnCount = bonusInfo[1]
            knightDict.update({stat: knightDict[stat] - bonus})  # Resetting the stat to it's initial value
            if turnCount == 0 and flag:  # Removes buffs from bonuses if it's turnCount has reached 0
                self.Bonuses.update({stat: (0, -1)})  # Reset the buff entry to default value

    def correct_stats(self):
        # fix for the Hp stat
        if self.Hp > self.Hpcap:
            self.Hp = self.Hpcap
        # fix the Mp stat
        if self.Mp > self.Mpcap:
            self.Mp = self.Mpcap
        elif self.Mp < 0:
            self.Mp = 0
        # fix the balance
        if self.Bal < 0:
            self.Bal = 0

    def __lt__(self, other):
        return other.Agl > self.Agl

    ########## DEBUG FUNCTIONS (NO TESTING REQUIRED)

    def print_status(self):
        statusStr = ""
        d = self.__dict__.copy()
        for key, value in d.items():
            if key == "Mp" or key == "Hp" or (key == "Exp" and d.get("Expcap") is not None):
                statusStr += key + ":" + str(value) + "/" + str(d[key + "cap"]) + "\n"
            elif key != "Hpcap" and key != "Mpcap" and key != "Expcap":
                statusStr += key + ":" + str(value) + "\n"
        print(statusStr)
