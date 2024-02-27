
class Move:
    def __init__(self, name, entity, jsonInfo):
        self.name = name
        self.damage = parse_damage_calculation(jsonInfo["Damage Calculation"], entity)  # Damage the move does
        self.type = jsonInfo["Type"]  # The type of move in question
        self.cost = jsonInfo["Cost"]  # The Mp cost of the move
        self.restriction = jsonInfo["Restriction"]  # Conditions that need to be met for the move to be used
        self.effect = jsonInfo["Effect"]  # Attached effect of the move
        self.AOE = jsonInfo["AOE"]  # boolean value that mentions if the move targets the entire screen
        self.targetNumber = jsonInfo["Target Number"]  # Integer representing the amount of targets for the given move
        # Chance for the effect of a move to be applied
        self.probability = jsonInfo["Probability"]
        self.weight = jsonInfo["Weight"]  # Probability of the move being used (Enemy object only)
        self.description = jsonInfo["Description"]  # Description of the attack being used

def parse_damage_calculation(damageFormula, entity):
    # Function that interprets the string as a simple math formula
    # Need to make this more advanced later
    damage = 0
    parseableText = damageFormula.split()
    if len(parseableText) == 3:
        stat = entity.__dict__[parseableText[0]]  # Grabbing the int value of the stat from entity
        damage = stat * float(parseableText[2])  # Calculating what the damage is going to be
    return int(damage)
