import random
import json

from Entity.Move import Move

class BattleManager:
    def __init__(self, knight):
        # First value in tuple is whether there's a battle going on, second value is the victor
        self.battleState = (False, "")
        self.moveDict = self.get_move_dict()  # fills up the move dictionary
        self.hero = knight
        self.heroPos = ()  # write it down later
        self.enemies = []  # tuple dict with enemy object and the x and y position of the object (max 6)
        self.turnOrder = []  # turn order list for the entities
        self.lootPool = {
            "Exp": 0,
            "Money": 0,
            "Items": {

            }
        }

    def add_enemy(self, enemy):
        # this function adds the enemy into the enemies list
        # while automatically giving them a set coordinate
        i = len(self.enemies)
        x = 900 + int(i / 3) * 300
        y = 100 + (i % 3) * 250
        self.enemies.append(((x, y), enemy))


    def get_move_dict(self):
        # Loads the move dictionary from a file
        file = open("JSON/Moves/Complete_Move_List.json", "r")
        jsonInfo = json.load(file)
        file.close()
        return jsonInfo

    def do_one_turn(self, move, target):
        # I'll worry about the drawing later
        # One round of battle
        returnable_strings = []
        turnObject = self.turnOrder[0]  # Get the first index object but don't remove it
        objectType = turnObject.__class__.__name__
        # Note that the move that is given is assumed to have been validated
        if objectType == "Knight" and move != "" and target != ():
            targetObj = self.get_entity_from_pos(target)
            moveObj = Move(move, self.hero, self.moveDict[move])
            if moveObj.AOE:  # if the move is an AOE move, target all enemies
                returnable_strings = self.use_move(self.hero, moveObj, self.enemies)
            else:
                returnable_strings = self.use_move(self.hero, moveObj, [targetObj])
            self.turnOrder.pop(0)  # now that the hero has successfully completed their turn, kick them from turn order
        elif objectType == "Enemy":
            usable = False
            loopNum = 0
            moveObj = Move("Attack", turnObject, self.moveDict["Attack"])
            while not usable and loopNum < 20:
                moveNum = random.randint(0, (len(turnObject.moveList) - 1))
                move = turnObject.moveList[moveNum]
                weightNum = random.randint(0, 100)
                moveInfo = self.moveDict[move]
                if weightNum <= moveInfo["Weight"] and self.parse_restriction(turnObject, moveInfo)\
                        and turnObject.Mp >= moveInfo["Cost"]:
                    usable = True
                    moveObj = Move(move, turnObject, moveInfo)
                loopNum += 1
            self.turnOrder.pop(0)  # remove the enemy entity from turnOrder
            returnable_strings = self.use_move(turnObject, moveObj, [self.hero])
        self.clear_dead_enemies()  # removes dead entities
        self.fix_entity_stats()  # correct the stats of all entities that are still alive
        return returnable_strings

    def use_move(self, turnObject, move,  targets):
        returnableStrings = []
        effectList = self.parse_effects(move)  # the function null checks the effects of the move
        for i in range(len(targets)):
            returnableStrings.append(turnObject.Name + " used " + move.name + "!")
            turnObject.Mp -= move.cost  # lower Mp by the cost of the move
            if move.type == "Attack":  # if this move is an attack, do damage to the target object
                # text outputted for attack type moves
                battleText = targets[i].Name + " took " + str(move.damage) + " damage!"
                returnableStrings.append(battleText)
                objectType = targets[i].__class__.__name__
                if objectType == "Knight":
                    targets[i].take_damage(move.damage)
                else:
                    targets[i].take_attack(move.damage, self.lootPool)
            # merge the 2 lists of move strings together
            returnableStrings = returnableStrings + self.apply_effects(effectList, turnObject, targets[i])
        return returnableStrings

    def parse_effects(self, move):
        effectList = []
        if move is not None and move.effect is not None:
            effects = move.effect.split(",")
            if len(effects) % 2 == 0:
                # immediate effect
                for i in range(0, len(effects), 2):
                    effect = effects[i]
                    target = effects[i + 1].strip()
                    effectList.append((target, effect))

            elif len(effects) % 3 == 0:
                # Debuff/buff effect
                for i in range(0, len(effects), 3):
                    buffAndStat = effects[i].split()
                    buff = int(buffAndStat[i])
                    stat = buffAndStat[i + 1]
                    target = effects[i + 1].strip()
                    buff = {stat: (buff, int(effects[i + 2]))}
                    effectList.append((target, buff))  # tuple with target and the buff
        return effectList

    def apply_effects(self, effectList, turnObject, target):
        returnableStrings = []  # Strings regarding the effects
        targetName = ""
        for i in range(len(effectList)):
            currentEffectTup = effectList[i]
            targetIndicator = currentEffectTup[0]
            if targetIndicator == "T":
                effectTarget = target
                targetName = target.Name
            else:
                effectTarget = turnObject
                targetName = turnObject.Name
            effectString = targetName + " "
            effect = currentEffectTup[1]
            if effect.__class__ == str:
                effectSplit = effect.split()
                try:
                    # do if the first string is a number
                    # this is a bad idea waiting to happen if a stat gets hit with this
                    # checks need to be added
                    # This is for immediate effects (healing, fixed damage, etc)
                    num = int(effectSplit[0])
                    stat = effectSplit[1]
                    ################### Make this work for percentages
                    if stat == "Hp" and num < 0:
                        effectString += "took " + str(abs(num)) + " damage!"
                    elif stat == "Hp" and num > 0:
                        effectString += "recovered " + str(num) + " Hp!"
                    elif stat == "Bal" and num < 0:
                        effectString += "lost " + str(abs(num)) + " Gold!"
                    elif stat == "Bal" and num > 0:
                        effectString += "gained " + str(num) + " Gold!"
                    ###################
                    effectTarget.__dict__[stat] += num

                except:
                    # if the first string isn't a number then do other things
                    # Assume it is applying a status or something
                    word = effectSplit[0]  # Word determines what gets done
                    result = effectSplit[1]
                    if word == "Apply":
                        # Apply a status effect
                        effectString += "is " + result + "ed !" # burn-ed, poison-ed, shock-ed, need something for bleed tho... etc

            else:
                # Debuff/buff
                stat = list(effect.keys())[0]  # the stat is the first and only key
                buff_details = effect[stat]  # the actual buff details
                ################### This also doesn't account for infinite buffs
                if buff_details[0] > 0:
                    effectString += "increased their " + stat + " by " + str(buff_details[0]) + " for " + str(buff_details[1]) + " turns!"
                elif buff_details[0] < 0:
                    effectString += "had their " + stat + " reduced by " + str(abs(buff_details[0])) + " for " + str(buff_details[1]) + " turns!"
                ###################
                self.apply_effect_buff(effectTarget, effect)
            #print(effectString)
            returnableStrings.append(effectString)
        return returnableStrings
    def apply_effect_buff(self, target, buff):
        target.remove_bonuses(False)  # strip off bonuses but don't remove buffs
        target.Bonuses.update(buff)  # Overwrite the buffs
        target.apply_bonuses(False)  # re-apply the bonuses but don't lower turn count

    def parse_restriction(self, entity, moveInfo):
        # in the future it should parse the MP cost too, not a hard change to make
        # parses the requirement and returns a boolean
        flag = True
        restriction = moveInfo["Restriction"]  # gets the restriction value
        if restriction is not None:  # None check
            restriction = restriction.split()
            stat = entity.__dict__[restriction[0]]
            operator = restriction[1]
            condition = restriction[2]
            hasPercentage = (condition.find("%") != -1)
            if isinstance(stat, str):
                flag = stat == condition
            else:
                if hasPercentage:
                    # converts the percentage to a real number (only usable by Hp and Mp stats)
                    condition = entity.__dict__[restriction[0] + "cap"] * (int(condition[0: len(condition) - 1]) / 100)
                if operator == "<" and isinstance(stat, int):
                    flag = stat < int(condition)

                elif operator == ">" and isinstance(stat, int):
                    flag = stat > int(condition)
        return flag

    def reset_turn_order(self):
        if len(self.turnOrder) == 0:
            # add the hero object to the turn order with the agility stat as the first index of the tuple
            self.turnOrder.append(self.hero)
            # add the enemy objects to the turn order with the agility stat as the first index of the tuple
            for i in range(len(self.enemies)):
                enemy = self.enemies[i][1]
                self.turnOrder.append(enemy)
            # sort the list, since the tuple has a number in the first index in descending order
            self.turnOrder.sort(reverse=True)  # WILL BREAK IF MULTIPLE OF THE SAME ENEMY EXISTS IN LIST

    def clear_dead_enemies(self):
        newEnemies = []  # empty list of enemies that aren't dead
        newTurnOrder = []  # empty list of entities that aren't dead
        # Loop through enemies list and append the not dead enemies to the newEnemies list
        for i in range(len(self.enemies)):
            enemy = self.enemies[i][1]
            if enemy.Status != "Dead":
                newEnemies.append(self.enemies[i])
        self.enemies = newEnemies  # set the enemies list to the newEnemies list
        # Loop through the turnOrder list and append the not dead entities to the newTurnOrder list
        # turnOrder does not need position of the enemy Object
        for i in range(len(self.turnOrder)):
            enemy = self.turnOrder[i]
            if enemy.Status != "Dead":
                newTurnOrder.append(enemy)
        self.turnOrder = newTurnOrder  # set the turnOrder list to the newTurnOrder list

    def fix_entity_stats(self):
        # Goes through all Entities and fixes their stats
        for i in range(len(self.turnOrder)):
            entity = self.turnOrder[i]
            entity.correct_stats()

    def get_entity_from_pos(self, pos):
        # find out the entity that this position is mapped to and return it
        if pos == self.heroPos:
            return self.hero
        else:
            for i in range(len(self.enemies)):
                enemyPos = self.enemies[i][0]
                if enemyPos == pos:
                    return self.enemies[i][1]

    def determine_battle_state(self):
        if len(self.enemies) == 0 and self.hero.Status != "Dead":
            self.battleState = (False, "Hero Wins")  # Battle ended, hero wins
        elif self.hero.Status == "Dead":
            self.battleState = (False, "Hero Loses")  # Battle ended, hero lost
        elif len(self.enemies) != 0 and self.hero.Status != "Dead":  # Battle is on going
            self.battleState = (True, "")
