# Parent class of hero and monster classes. Saves me the trouble of re-writing a
# bunch of code
class Entity:
    def __init__(self, Hp, Hpcap, name, level, strength, vitality, agility, defence, exp, money, inventory=None):
        if inventory is None:
            inventory = {}  # Inventory is a dictionary of it with key pairs (string: int)
        self.Hp = Hp
        self.Hpcap = Hpcap
        self.Name = name
        self.Lvl = level
        self.Str = strength
        self.Vit = vitality
        self.Agl = agility
        self.Status = "Normal"
        self.bonuses = {  # A dict of all positive and negative effects on Knight character, includes stance bonuses
            "Str": (0, -1), "Vit": (0, -1), "Agl": (0, -1), "Defence": (0, -1)  # -1 means unlimited duration for bonus
        }
        self.moveSet = []
        self.Defence = defence
        self.Exp = exp
        self.Bal = money
        self.Inventory = inventory  # For heroes, it's a bunch of useful items, for monsters it's dropped items

    def attack(self, target):  # Write later
        pass

    def take_damage(self, damage):
        damage = damage - self.Defence  # how much damage you ACTUALLY take
        if damage > 0:  # can't have damage healing you now can I?
            self.Hp -= damage
            if self.Hp < 0:  # Check if you died to the attack
                self.Hp = 0  # Set hp to 0 or else weird things will start happening
                self.Status = "Dead"  # Change status to dead

    def apply_bonuses(self):
        # applies the bonus to the relevant stat
        # Only one bonus can be applied to a stat at a time leading to some interesting strats...
        knightDict = self.__dict__  # This is a horrible idea... still doing it
        for stat in self.bonuses:
            bonusInfo = self.bonuses[stat]
            bonus = bonusInfo[0]
            turnCount = bonusInfo[1]
            knightDict.update({stat: knightDict[stat] + bonus})
            if turnCount != -1:  # If it isn't an infinite buff then decrement counter
                self.bonuses.update({stat: (bonus, turnCount - 1)})  # Add the updated turn count to bonuses dict

    def remove_bonuses(self):
        # Removes any buff effect at the end of turn so buff effects don't linger
        knightDict = self.__dict__  # This is a horrible idea... still doing it
        for stat in self.bonuses:
            bonusInfo = self.bonuses[stat]
            bonus = bonusInfo[0]
            turnCount = bonusInfo[1]
            knightDict.update({stat: knightDict[stat] - bonus})  # Resetting the stat to it's initial value
            if turnCount == 0:  # Removes buffs from bonuses if it's turnCount has reached 0
                self.bonuses.update({stat: (0, -1)})  # Reset the buff entry to default value