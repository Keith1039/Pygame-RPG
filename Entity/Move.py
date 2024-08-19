
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

def isfloat(stringVal):
    # checks and sees if a string is an eligible float
    try:
        float(stringVal)
        return True
    except ValueError:
        return False

def parse_damage_calculation(damageFormula, entity):
    # Function that interprets the string as a simple math formula
    # Need to make this more advanced later
    stat = 0  # the stat we use
    value = 0  # the second value that is in the equation
    op = ""  # the math operator
    damage = 0
    if damageFormula != "":
        flag = look_for_special_symbols(damageFormula)  # check if the formula has special symbols
        parseableText = damageFormula.split()  # split the formula
        # we always assume we get an array of size 0
        if not flag:
            # replace all the stat names with the values from the entity
            damageFormula = replace_all_stats_with_values(damageFormula, entity)
            parseableText = damageFormula.split()  # split the formula again with the new formula
            stat = int(parseableText[0])  # get the value for the stat
        else:
            stat = entity.__dict__[parseableText[0]]  # should be an int
        value = parse_special_symbols(parseableText[2], entity)
        op = parseableText[1]  # get the math operator
        if op == "*":
            damage = stat * value
        elif op == "+":
            damage = stat + value
    return round(damage)  # round up to nearest integer

def replace_all_stats_with_values(damageFormula, entity):
    # replaces all the key values that pair to an integer in the formula string
    objectiveList = []
    for stat, value in entity.__dict__.items():
        if isinstance(value, int):  # we only want the actual stats
            objectiveList.append(stat)  # add it to the objective list
    objectiveList.sort(reverse=True)  # sort the list in reverse order (ensures Hpcap is always above Hp etc.)
    for stat in objectiveList:
        damageFormula = damageFormula.replace(stat, str(entity.__dict__[stat]))  # replaces the name with the value
    return damageFormula  # return the new damage formula

def look_for_special_symbols(damageFormula):
    # check if the damageFormula has special symbols
    specialSymbols = ["-Hp%", "Hp%"]  # READ FROM FILE LATER?
    flag = False
    for symbol in specialSymbols:
        flag = damageFormula.find(symbol) != -1
    return flag

def parse_special_symbols(parseString, entity):
    # function that processes the second part of the equation for special symbols
    if isfloat(parseString):
        return float(parseString)

    else:
        # the multiplier and the special symbol that indicate how to parse the value into a number
        multiplier = ""
        specialSymbol = ""
        # loop that strips the number multiplier from the special symbol
        for i in range(len(parseString)):
            flag = parseString[i].isnumeric()
            # once we reach the first, non-numeric character, we parse out the multiplier and special symbol
            # we also break the loop
            if not flag:
                if i == 0:
                    multiplier = "1"
                    specialSymbol = parseString
                else:
                    multiplier = parseString[0: i]
                    specialSymbol = parseString[i: len(parseString)]
                break
        # we return the value we get from parsing
        return apply_symbol(int(multiplier), specialSymbol, entity)

def apply_symbol(multiplier, specialSymbol, entity):
    # converts the special symbol and multiplier into a tangible number
    specialSymbolVal = 0
    if specialSymbol == "-Hp%":
        # inverse health scaling
        specialSymbolVal = 1 - (entity.Hp/entity.Hpcap)
    elif specialSymbolVal == "Hp%":
        # normal health scaling
        specialSymbolVal = entity.Hp/entity.Hpcap
    # return the multiplier * the value
    return float(multiplier * specialSymbolVal)

