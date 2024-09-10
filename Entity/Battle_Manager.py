import random
import Utils
from Entity.Move import Move

class BattleManager:
    def __init__(self, knight, itemManager, animationManager):
        # First value in tuple is whether there's a battle going on, second value is the victor
        self.battleState = (False, "")
        self.moveDict = Utils.get_move_dict()  # fills up the move dictionary
        self.statusDict = Utils.get_status_dict()  # retrieves the effect information
        self.knight = knight  # the hero dict
        self.itemManager = itemManager  # the item manager
        self.animationManager = animationManager  # the animation manager
        self.targetNum = -1  # the amount of targets that need to be selected
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
        enemy.rect.center = (x, y)  # center the object first
        enemy.x = enemy.rect.center[0]  # set the x value
        enemy.y = enemy.rect.bottom  # set the y value
        self.enemies.append(enemy)  # add the enemy to the list

    def do_one_turn(self, move, target):
        # I'll worry about the drawing later
        # One round of battle
        refresh = False  # indicator that we should refresh the items inventory
        returnable_strings = []
        turnObject = self.turnOrder[0]  # Get the first index object but don't remove it
        objectType = turnObject.__class__.__name__
        statusEffect = self.statusDict[turnObject.Status[0]]["Effect"]  # get the effect for the status
        if statusEffect.find("Lose turn") != -1:  # condition to see if the entity loses their turn
            # this is done so that the player character doesn't have to select a move and target an enemy
            # only to be told that they can't move anyway
            statusStrings = self.handle_status(turnObject)
            returnable_strings += statusStrings
            self.turnOrder.pop(0)  # remove the user from turn order
        else:
            # handle the status effects
            statusStrings = self.handle_status(turnObject)
            returnable_strings += statusStrings
            targets = []  # list of entity objects
            # Note that the move that is given is assumed to have been validated
            if objectType == "Knight" and move != "" and len(target) == self.targetNum:
                # print(target)
                actionInfo = {}  # the action information we need
                actionTargets = []
                for i in range(len(target)):
                    # get a list of Entity objects from the positions
                    targets.append(self.get_entity_from_pos(target[i]))
                # we're using an item
                if move in self.itemManager.itemJson.keys():
                    refresh = True  # set refresh equal to true
                    actionInfo = self.itemManager.get_action_details(move)  # get the action information
                    itemDetails = self.itemManager.get_effect_details(move)  # getting information about the item
                    if itemDetails["AOE"]:
                        actionTargets = self.get_enemy_objects()  # set the action targets to every enemy
                        returnable_strings += self.use_item(self.knight, move, itemDetails["Effect"], self.get_enemy_objects())
                    else:
                        actionTargets = targets
                        returnable_strings += self.use_item(self.knight, move, itemDetails["Effect"], targets)
                # if we aren't using an item we're using a move of some sort
                else:
                    moveObj = Move(move, self.knight, self.moveDict[move])  # make the move object
                    actionInfo = moveObj.get_action_details()  # get the action details for the move
                    if moveObj.AOE:  # if the move is an AOE move, target all enemies
                        actionTargets = self.get_enemy_objects()  # set the action targets to all enemies
                        returnable_strings += self.use_move(self.knight, moveObj, self.get_enemy_positions())
                    else:
                        actionTargets = targets
                        returnable_strings += self.use_move(self.knight, moveObj, targets)
                # get the list of uninvolved actors
                others = Utils.get_others(self.knight, actionTargets, self.get_enemy_objects())
                # load the manager with information
                self.animationManager.load_action_queue(actionInfo, self.knight, actionTargets, others)
                self.turnOrder.pop(0)  # after the player has moved, kick them from turn order
                # self.print_all_statuses()  ######## DEBUG
            elif objectType == "Enemy":
                # handle the status effects
                statusStrings = self.handle_status(turnObject)
                returnable_strings += statusStrings
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
                for z in range(moveObj.targetNumber):
                    targets.append(self.knight)
                actionInfo = moveObj.get_action_details()  # get the move information
                returnable_strings += self.use_move(turnObject, moveObj, targets)
                others = Utils.get_others(turnObject, targets, self.get_enemy_objects())  # get the others
                self.targetNum = -1  # reset the target number since the move was done successfully
                self.animationManager.load_action_queue(actionInfo, turnObject, targets, others)
                self.turnOrder.pop(0)  # remove the enemy entity from turnOrder
                # self.print_all_statuses()  ######## DEBUG
        # clear dead enemies should return a string of people who died to returnable strings
        returnable_strings += self.clear_dead_enemies()  # removes dead entities and add event strings
        self.fix_entity_stats()  # correct the stats of all entities that are still alive
        return returnable_strings, refresh

    def use_move(self, turnObject, move,  targets):
        returnableStrings = []
        effectList = self.parse_effects(move.effect)  # the function null checks the effects of the move
        for i in range(len(targets)):
            returnableStrings.append(turnObject.altName + " used " + move.name + "!")
            turnObject.Mp -= move.cost  # lower Mp by the cost of the move
            if move.type == "Attack":  # if this move is an attack, do damage to the target object
                # text outputted for attack type moves
                objectType = targets[i].__class__.__name__
                damageVal = 0
                if objectType == "Knight":
                    damageVal = targets[i].take_damage(move.damage)
                else:
                    damageVal = targets[i].take_attack(move.damage, self.lootPool)
                battleText = targets[i].altName + " took " + str(damageVal) + " damage!"
                returnableStrings.append(battleText)
            # merge the 2 lists of move strings together
            returnableStrings = returnableStrings + self.apply_effects(effectList, turnObject, targets[i])
        return returnableStrings

    def use_item(self, turnObject, itemName, itemEffect, targets):
        # function for when an item is used
        returnableStrings = []
        returnableStrings.append(turnObject.altName + " Used " + itemName + "!")
        self.knight.remove_from_inventory(itemName)
        effectList = self.parse_effects(itemEffect)
        for i in range(len(targets)):
            returnableStrings = returnableStrings + self.apply_effects(effectList, turnObject, targets[i])
        return returnableStrings

    def parse_effects(self, effectString):
        effectList = []
        if effectString is not None:
            splitEffects = effectString.split("|")
            for i in range(len(splitEffects)):
                effects = splitEffects[i].split(",")
                lastVal = effects[-1]  # get the last value in the last
                lastVal = lastVal.strip()  # strip white space
                if lastVal != "S" and lastVal != "T":
                    # implied self effect
                    effects.append("S")
                if len(effects) == 2:
                    # immediate effect
                    effect = effects[0]
                    target = effects[1].strip()
                    effectList.append((target, effect))

                elif len(effects) == 3:
                    # Debuff/buff effect
                    buffAndStat = effects[0].split()
                    buff = int(buffAndStat[0])
                    stat = buffAndStat[1]
                    target = effects[2].strip()
                    buffDuration = effects[1]
                    buff = {stat: (buff, int(buffDuration))}
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
                targetName = target.altName
            else:
                effectTarget = turnObject
                targetName = turnObject.altName
            effectString = targetName + " "
            effect = currentEffectTup[1]
            if effect.__class__ == str:
                effectSplit = effect.split()
                testString = effect.replace("+", "")  # remove +
                testString = testString.replace("-", "")  # remove -
                testString = testString.replace("%", "")  # remove %
                #print(testString)
                if testString.split()[0].isnumeric():
                    # do if the first string is a number
                    # this is a bad idea waiting to happen if a stat gets hit with this
                    # checks need to be added
                    # This is for immediate effects (healing, fixed damage, etc.)
                    percentagePos = effect.find("%")
                    num = 0
                    if percentagePos != -1:  # healing/damage dealt with percentages
                        statCap = testString.split()[1] + "cap"  # make the stat we care about
                        # the numerical equivalent to the percentage we wanted
                        num = int(effectTarget.__dict__[statCap] * (int(effect[0: percentagePos]) / 100))
                    else:
                        num = int(effectSplit[0])
                    stat = effectSplit[1]
                    # condition so that people die when they are killed
                    if stat == "Hp" and num < 0:
                        damageVal = 0
                        if effectTarget.__class__.__name__ == "Enemy":
                            damageVal = effectTarget.take_attack(abs(num), self.lootPool, True)
                        else:
                            damageVal = effectTarget.take_damage(abs(num), True)
                        effectString += "took " + str(damageVal) + " damage!"
                    else:
                        # since we're not taking damage, directly add to the stat
                        effectTarget.__dict__[stat] += num
                    # all cases for the effect string except for taking damage
                    if stat == "Hp" and num > 0:
                        effectString += "recovered " + str(num) + " Hp!"
                    elif stat == "Bal" and num < 0:
                        effectString += "lost " + str(abs(num)) + " Gold!"
                    elif stat == "Bal" and num > 0:
                        effectString += "gained " + str(num) + " Gold!"
                else:
                    # if the first string isn't a number then do other things
                    # Assume it is applying a status or something
                    word = effectSplit[0]  # Word determines what gets done
                    result = effectSplit[1]
                    if word == "Apply":
                        # Apply a status effect
                        effectTarget.Status = (result, 0)  # set the status
                        effectString += "is " + result + "ed !"  # burn-ed, poison-ed, shock-ed, missing one for bleed
                    elif word == "Cure":
                        # cure a status effect if the right item was used
                        if result == effectTarget.Status[0] or result == "All":
                            effectTarget.Status = ("Normal", -1)
                            effectString += effectTarget.altName + " is back to Normal!"
                        else:
                            effectString += "it wasn't effective!"
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
            # add the hero object
            self.turnOrder.append(self.knight)
            # add the enemy objects
            for i in range(len(self.enemies)):
                enemy = self.enemies[i]
                self.turnOrder.append(enemy)
            # sort the list, since the tuple has a number in the first index in descending order
            self.turnOrder.sort(reverse=True)

    def clear_dead_enemies(self):
        returnableStrings = []
        newEnemies = []  # empty list of enemies that aren't dead
        newTurnOrder = []  # empty list of entities that aren't dead
        # Loop through enemies list and append the not dead enemies to the newEnemies list
        for i in range(len(self.enemies)):
            enemy = self.enemies[i]
            if enemy.Status[0] != "Dead":
                newEnemies.append(enemy)
            else:
                returnableStrings.append(enemy.altName + " died!")
        self.enemies = newEnemies  # set the enemies list to the newEnemies list
        # Loop through the turnOrder list and append the not dead entities to the newTurnOrder list
        # turnOrder does not need position of the enemy Object
        for i in range(len(self.turnOrder)):
            enemy = self.turnOrder[i]
            if enemy.Status[0] != "Dead":
                newTurnOrder.append(enemy)
        self.turnOrder = newTurnOrder  # set the turnOrder list to the newTurnOrder list
        return returnableStrings

    def fix_entity_stats(self):
        # Goes through all Entities and fixes their stats
        for i in range(len(self.turnOrder)):
            entity = self.turnOrder[i]
            entity.correct_stats()

    def get_entity_from_pos(self, pos):
        # find out the entity that this position is mapped to and return it
        if pos == self.get_knight_pos():
            return self.knight  # return hero
        else:
            for i in range(len(self.enemies)):
                enemy = self.enemies[i]  # enemy object
                if pos == enemy.rect.center:  # check the position
                    return enemy  # return enemy

    def determine_battle_state(self):
        if len(self.enemies) == 0 and self.knight.Status[0] != "Dead":
            self.battleState = (False, "Hero Wins")  # Battle ended, hero wins
            self.animationManager.reset_action()  # reset the animation manager
        elif self.knight.Status[0] == "Dead":
            self.battleState = (False, "Hero Loses")  # Battle ended, hero lost
            self.animationManager.reset_action()  # reset the animation manager
        elif len(self.enemies) != 0 and self.knight.Status[0] != "Dead":  # Battle is on going
            self.battleState = (True, "")

    def get_enemy_positions(self):
        # function that returns a list of enemy positions
        targetable = []
        for i in range(len(self.enemies)):
            # getting the positions of the enemies (center of the sprite)
            targetable.append(self.enemies[i].rect.center)
        return targetable

    def get_enemy_objects(self):
        # function that returns a list of enemy objects
        return self.enemies

    def get_knight_pos(self):
        # returns the position of the knight (specifically the center)
        return self.knight.rect.center

    def apply_status_effect(self, entity):
        returnableStrings = []
        if entity.Status[1] != -1:
            # increase the count for the status
            entity.Status = (entity.Status[0], entity.Status[1] + 1)
        statusEffect = self.statusDict[entity.Status[0]]["Effect"]
        if statusEffect != "":
            effectList = statusEffect.split(",")  # split by
            for i in range(len(effectList)):
                effectString = " Because of " + entity.Status[0] + ", " + entity.altName + " "
                effect = effectList[i]  # the effect we parse
                effectSplit = effect.split()
                # REPLACE LATER ON WHEN DOING YOUR FINAL REVISIONS
                testString = effect.replace("+", "")  # remove +
                testString = testString.replace("-", "")  # remove -
                testString = testString.replace("%", "")  # remove %
                if testString.split()[0].isnumeric():
                    # do if the first string is a number
                    # this is a bad idea waiting to happen if a stat gets hit with this
                    # checks need to be added
                    # This is for immediate effects (healing, fixed damage, etc.)
                    percentagePos = effect.find("%")
                    num = 0
                    if percentagePos != -1:  # healing/damage dealt with percentages
                        statName = testString.split()[1]
                        # the numerical equivalent to the percentage we wanted
                        num = int(entity.__dict__[statName] * (int(effect[0: percentagePos]) / 100))
                    else:
                        num = int(effectSplit[0])

                    stat = effectSplit[1]
                    capPos = stat.find("cap")
                    if capPos != -1:  # max it so that we inflict damage to Hp instead of Hpcap
                        stat = stat[0:capPos]
                    # condition so that people die when they are killed
                    if stat == "Hp" and num < 0:
                        # status effect damage counts as effect damage
                        damageVal = 0
                        if entity.__class__.__name__ == "Enemy":
                            damageVal = entity.take_attack(abs(num), self.lootPool, True)
                        else:
                            damageVal = entity.take_damage(abs(num), True)
                        effectString += "took " + str(damageVal) + " damage!"
                    else:
                        # since we're not taking damage, directly add to the stat
                        entity.__dict__[stat] += num
                    # all cases for the effect string except for taking damage
                    if stat == "Hp" and num > 0:
                        effectString += "recovered " + str(num) + " Hp!"
                    ##### MOST LIKELY USELESS
                    # elif stat == "Bal" and num < 0:
                    #     effectString += "lost " + str(abs(num)) + " Gold!"
                    # elif stat == "Bal" and num > 0:
                    #     effectString += "gained " + str(num) + " Gold!"
                else:
                    if effect == "Lose turn":
                        effectString += "lost their turn!"  # appends the status string
                returnableStrings.append(effectString)
        return returnableStrings
    def handle_status(self, entity):
        returnableStrings = self.apply_status_effect(entity)
        maxCount = self.statusDict[entity.Status[0]]["maxCount"]
        # checks to see if the status effect has faded away assuming it isn't infinite
        if entity.Status[1] == maxCount and maxCount != -1:
            returnableStrings.append(entity.altName + " is back to Normal!")
            entity.Status = ("Normal", -1)
        return returnableStrings  # return all status strings

    def set_target_number(self, move):
        # set the target number based off of the move
        moveInfo = self.moveDict[move]
        self.targetNum = moveInfo["Target Number"]


    ########## DEBUG FUNCTIONS (NO TESTING REQUIRED)

    def print_all_statuses(self):
        self.knight.print_status()
        d = self.get_enemy_objects()
        for i in range(len(d)):
            d[i].print_status()
