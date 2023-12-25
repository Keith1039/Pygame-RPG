# Parent class of hero and monster classes. Saves me the trouble of re-writing a
# bunch of code
class Entity:
    def __init__(self, Hp, Hpcap, Mp, Mpcap, name, level, strength, vitality, agility, defence, exp, money, inventory=None):
        if inventory is None:
            inventory = {}  # Inventory is a dictionary of it with key pairs (string: int)
        self.Hp = Hp
        self.Hpcap = Hpcap
        self.Mp = Mp
        self.Mpcap = Mpcap
        self.Name = name
        self.Lvl = level
        self.Str = strength
        self.Vit = vitality
        self.Agl = agility
        self.Status = "Normal"
        self.Bonuses = {  # A dict of all positive and negative effects on Knight character, includes stance bonuses
            "Str": (0, -1), "Vit": (0, -1), "Agl": (0, -1), "Defence": (0, -1)  # -1 means unlimited duration for bonus
        }
        self.Defence = defence
        self.Exp = exp
        self.Bal = money
        self.Inventory = inventory  # For heroes, it's a bunch of useful items, for monsters it's dropped items


    def take_damage(self, damage):
        damage = damage - self.Defence  # how much damage you ACTUALLY take
        if damage > 0 and self.Status != "Dead":  # Only allows positive damage to be inflicted on alive opponents
            self.Hp -= damage
            if self.Hp <= 0:  # Check if you died to the attack
                self.Hp = 0  # Set hp to 0 or else weird things will start happening
                self.Status = "Dead"  # Change status to dead

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
        if self.Hp > self.Hpcap:
            self.Hp = self.Hpcap
        if self.Bal < 0:
            self.Bal = 0
