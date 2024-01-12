import random
import json
from Entity.Move import Move

class BattleManager:
    def __init__(self, knight):
        self.moveDict = self.get_move_dict()
        self.hero = knight
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

    def do_battle(self):
        # I'll worry about the drawing later
        # One round of battle
        turnObject = self.turnOrder.pop(0)  # Get the first index object
        objectType = turnObject.__class__.__name__

        if objectType == "Knight":
            # let the player control the object
            pass
        else:
            usable = False
            loopNum = 0
            moveObj = Move(turnObject, self.moveDict["Attack"])
            while not usable and loopNum < 20:
                moveNum = random.randint(0, (len(turnObject.moveList) - 1))
                move = turnObject.moveList[moveNum]
                weightNum = random.randint(0, 100)
                moveInfo = self.moveDict[move]
                if weightNum <= moveInfo["Weight"] and self.parse_restriction(turnObject, moveInfo)\
                        and turnObject.Mp >= moveInfo["Cost"]:
                    usable = True
                    moveObj = Move(turnObject, moveInfo)
                loopNum += 1
            self.use_move(turnObject, moveObj, self.hero)



    def use_move(self, turnObject, move,  *targets):
        effectList = self.parse_effects(move)  # the function null checks the effects of the move
        for i in range(len(targets)):
            turnObject.Mp -= move.cost  # lower Mp by the cost of the move
            if move.type == "Attack":  # if this move is an attack, do damage to the target object
                objectType = targets[i].__class__.__name__
                if objectType == "Knight":
                    targets[i].take_damage(move.damage)
                else:
                    targets[i].take_attack(move.damage, self.lootPool)
            self.apply_effects(effectList, turnObject, targets[i])



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
        for i in range(len(effectList)):
            currentEffectTup = effectList[i]
            targetIndicator = currentEffectTup[0]
            if targetIndicator == "T":
                effectTarget = target
            else:
                effectTarget = turnObject
            effect = currentEffectTup[1]
            if effect.__class__ == str:
                effectSplit = effect.split()
                try:
                    # do if the first string is a number
                    # this is a bad idea waiting to happen
                    # checks need to be added
                    num = int(effectSplit[0])
                    stat = effectSplit[1]
                    effectTarget.__dict__[stat] += num
                except:
                    # if the first string isn't a number then do other things
                    # Assume it is applying a status or something
                    word = effectSplit[0]  # Word determines what gets done
                    result = effectSplit[1]
                    if word == "Apply":
                        # Apply a status effect
                        pass
            else:
                # Debuff/buff
                self.apply_effect_buff(effectTarget, effect)
    def apply_effect_buff(self, target, buff):
        target.remove_bonuses(False)  # strip off bonuses but don't remove buffs
        target.Bonuses.update(buff)  # Overwrite the buffs
        target.apply_bonuses(False)  # re-apply the bonuses but don't lower turn count

    def parse_restriction(self, entity, moveInfo):
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
            self.turnOrder.append((self.hero.Agl, self.hero))
            # add the enemy objects to the turn order with the agility stat as the first index of the tuple
            for i in range(len(self.enemies)):
                enemy = self.enemies[i][1]
                self.turnOrder.append((enemy.Agl, enemy))
            # sort the list, since the tuple has a number in the first index in descending order
            self.turnOrder.sort(reverse=True)
        # loop through the turn order and replace each index with the Entity object
            for i in range(len(self.turnOrder)):
                tup = self.turnOrder[i]
                self.turnOrder[i] = tup[1]


    def clear_dead_enemies(self):
        newEnemies = []  # empty list of enemies that aren't dead
        newTurnOrder = []  # empty list of entities that aren't dead
        # Loop through enemies list and append the not dead enemies to the newEnemies list
        for i in range(len(self.enemies)):
            enemy = self.enemies[i][1]
            if enemy.Status != "Dead":
                newEnemies.append(self.enemies[i][1])
        self.enemies = newEnemies  # set the enemies list to the newEnemies list
        # Loop through the turnOrder list and append the not dead entities to the newTurnOrder list
        # turnOrder does not need position of the enemy Object
        for i in range(len(self.turnOrder)):
            enemy = self.turnOrder[i][1]
            if enemy.Status != "Dead":
                newTurnOrder.append(enemy)
        self.turnOrder = newTurnOrder  # set the turnOrder list to the newTurnOrder list

