from Entity.Animation_Manager_test import goblin
from Entity.Knight import Knight
from Entity.Entity_Factory import EntityFactory
from Entity.Animation_Manager import AnimationManager
from Entity.Battle_Manager import BattleManager
from Entity.Move import Move
import pygame as game

from managers.UI_Manager import UIManager
from managers.Item_Manager import ItemManager

game.init()
screen = game.display.set_mode((1422, 800))
font = game.font.Font('font/Pixeltype.ttf', 50)
uiManager = UIManager(font, screen)

factory = EntityFactory()
knight = Knight()
dummy = factory.create_entity("dummy")
itemManager = ItemManager(knight)
animationManager = AnimationManager(screen)
battleManager = BattleManager(knight, itemManager, animationManager)
effectListMatrix = []
# creating move objects
attack = Move("Attack", dummy, battleManager.moveDict["Attack"])
statusMove = Move("Venom Strike", dummy, battleManager.moveDict["Venom Strike"])
buffEffectMove = Move("Angry Shout", dummy, battleManager.moveDict["Angry Shout"])
immediateMove = Move("Pilfering Strike", dummy, battleManager.moveDict["Pilfering Strike"])
healMove = Move("Drink Potion", dummy, battleManager.moveDict["Drink Potion"])
hybridMove = Move("Defensive Stance", dummy, battleManager.moveDict["Defensive Stance"])
# AOE moves can only be play tested because they utilise the logic in the do_one_turn function which is play tested

def test_add_enemy():
    flag = False
    for i in range(6):
        battleManager.add_enemy(dummy)
        flag = battleManager.enemies[i] == dummy and \
               battleManager.enemies[i].rect.center == (900 + int(i / 3) * 300, 100 + int(i % 3) * 250)
        if not flag:
            break
    # clear the list and re-add one dummy to the list of enemies
    battleManager.enemies.clear()
    battleManager.add_enemy(dummy)
    # dummy's coords
    x = dummy.rect.center[0]
    y = dummy.rect.center[1]
    flag2 = x == 900 and y == 100  # check if the dummy's coordinates changed
    assert flag and flag2

def test_get_health_dict():
    initial = battleManager.get_health_info()
    # check if the number is correct and that the Hp key is in the dict
    flag = True
    for enemy in battleManager.enemies:
        # confirm all the enemies are represented in the dict
        if enemy.altName not in initial:
            flag = False
            break
        else:
            # check to see if the proper keys are there
            if initial[enemy.altName].get("Hp") is None:
                flag = False
                break
    assert flag

def test_parse_effects():
    # parse a move with no effect
    effectListMatrix.append(battleManager.parse_effects(attack.effect))
    flag = len(effectListMatrix[0]) == 0
    # parse the effects of a move with a buff effect
    effectListMatrix.append(battleManager.parse_effects(buffEffectMove.effect))
    # check if the target is correct and check if the second index of the tuple is of the correct type
    flag2 = effectListMatrix[1][0][0] == "S" and isinstance(effectListMatrix[1][0][1], dict)
    # parse the effects of a move with an immediate effect
    effectListMatrix.append(battleManager.parse_effects(immediateMove.effect))
    # check if the target is correct and check if the second index of the tuple is of the correct type
    flag3 = effectListMatrix[2][0][0] == "T" and isinstance(effectListMatrix[2][0][1], str)
    effectListMatrix.append(battleManager.parse_effects(healMove.effect))  # add the heal move effect list for later test
    effectListMatrix.append(battleManager.parse_effects(statusMove.effect))  # add status move for later test
    effectListMatrix.append(battleManager.parse_effects(hybridMove.effect))  # add the hybrid move for later test
    # Check the flags
    assert flag and flag2 and flag3

def test_apply_effect_buff():
    strBuff = (100, 0)
    aglBuff = (30, 3)
    defBuff = (50, 3)
    # Add the buffs to the dummy object
    dummy.Bonuses.update({"Str": strBuff})
    dummy.Bonuses.update({"Agl": aglBuff})
    # call the apply_effect_buff function
    battleManager.apply_effect_buff(dummy, {"Def": defBuff})
    # Checks if the defence buff was successfully applied
    # Check if the buffs that were applied before are still applied after the apply_effect_buff() call
    # This implicitly checks if the turn counts were altered
    assert dummy.Bonuses["Str"] == strBuff and dummy.Bonuses["Agl"] and dummy.Bonuses["Def"] == defBuff

def test_apply_effects():
    knight.Bal = 20  # setting knight Bal attribute
    oldDummyHp = dummy.Hp  # saving the dummy's Hp before it is changed by effect
    eventStrings = []
    for i in range(len(effectListMatrix)):
        effectList = effectListMatrix[i]  # gets the current effect list
        # run apply_effects() and add to the list of event strings
        eventStrings = eventStrings + battleManager.apply_effects(effectList, dummy, knight)
    # Check if all the effects were properly applied
    flag = dummy.Bonuses["Str"] == (5, 3) and knight.Bal == 0 and oldDummyHp + 40 == dummy.Hp and len(eventStrings) == 6 \
           and dummy.Bonuses["Def"] == (10, 3)
    # check to see if the poison was applied
    flag2 = knight.Status[0] == "Poison" and knight.Status[1] == 0
    assert flag and flag2

def test_use_move():
    # Buffing knight object's stats, so they survive the dummy object's attack
    knight.Bal = 20  # give knight 20 dollar for him to get robbed again
    knight.Hp = 999
    knight.Hpcap = 999
    knight.Def = 700
    # reset eventStrings and make a new list of event strings
    eventStrings = []
    eventStrings = eventStrings + battleManager.use_move(dummy, attack, [knight])  # this should do exactly 99 damage
    eventStrings = eventStrings + battleManager.use_move(dummy, buffEffectMove, [knight])
    eventStrings = eventStrings + battleManager.use_move(dummy, immediateMove, [knight])  # does 0 damage
    eventStrings = eventStrings + battleManager.use_move(dummy, healMove, [knight])
    # check if the knight's attributes to see if they're affected, check if the dummy's Mp decreased
    assert knight.Bal == 0 and knight.Hp == 900 and dummy.Mp == dummy.Mpcap - 120 and len(eventStrings) == 9

def test_use_item():
    knight.Inventory.update({"Potion": 1})  # add potion to Knight's inventory
    knight.Inventory.update({"Bomb": 1})  # add Bomb to Knight's inventory
    potionEffect = itemManager.itemEffectJson["Potion"]["Effect"]  # potion effect string
    bombEffect = itemManager.itemEffectJson["Bomb"]["Effect"]  # bomb effect string
    battleManager.use_item(knight, "Potion", potionEffect, [knight])  # use potion on knight
    battleManager.use_item(knight, "Bomb", bombEffect, [knight])   # illegal use of bomb but who cares right?
    # should be 899 in real game because of how do_one_turn is coded to have Knight fix its stats after every turn
    assert knight.Hp == 900 and len(knight.Inventory) == 0

def test_parse_restrictions():
    # NEEDS MORE TEST CASES
    # see if the dummy can use the move
    flag = battleManager.parse_restriction(dummy, battleManager.moveDict["Wrathful Charge"])
    dummy.Hp = int(dummy.Hpcap * .20)  # lower dummy object's Hp to meet the threshold
    # see if the dummy can use the move again with lower health
    flag2 = battleManager.parse_restriction(dummy, battleManager.moveDict["Wrathful Charge"])
    # see if the dummy can use a move that has no restriction
    flag3 = battleManager.parse_restriction(dummy, battleManager.moveDict["Attack"])
    # check the flags
    assert not flag and flag2 and flag3

def test_reset_turn_order():
    battleManager.reset_turn_order()  # call reset turn order
    # check if the turnOrder list has the proper length and the proper position for the objects
    assert (len(battleManager.turnOrder) == 2 and battleManager.turnOrder[0] == dummy
            and battleManager.turnOrder[1] == knight)

def test_clear_dead_enemies():
    battleManager.enemies[0].Status = ("Dead", -1)  # Change Dummy status to Dead
    returnableStrings = battleManager.clear_dead_enemies()  # clear the dead enemies
    # Check if the enemies list is empty and only the hero object should be in turn order
    # also checks to see if the event string was added
    assert len(battleManager.enemies) == 0 and len(battleManager.turnOrder) == 1 and len(returnableStrings) == 1

def test_fix_entity_stats():
    knight.Hp = 999
    knight.Hpcap = 9
    knight.Bal = - 100
    battleManager.add_enemy(factory.create_entity("dummy"))  # re-add a new dummy to list of enemies
    battleManager.enemies[0].Mpcap = 1
    battleManager.turnOrder.clear()  # reset the turnOrder
    battleManager.reset_turn_order()  # Add all alive entities to the turn order
    battleManager.fix_entity_stats()
    # check to see if the health, mana and bal values have been changed
    assert knight.Hp == 9 and knight.Bal == 0 and battleManager.enemies[0].Mp == 1

def test_get_entity_from_pos():
    # clear and re-add a dummy object
    battleManager.enemies.clear()
    dummy = factory.create_entity("dummy")
    battleManager.add_enemy(dummy)
    pos = battleManager.get_knight_pos()  # center of the knight's rect
    entity = battleManager.get_entity_from_pos(pos)
    pos = (900, 100)
    entity2 = battleManager.get_entity_from_pos(pos)
    assert entity == knight and entity2 == dummy

def test_determine_battle_state():
    animationManager.deadGroup.add(goblin)  # add goblin to the group
    # kill hero and see if the state is changed appropriately also check if the dead group is emptied
    knight.Status = ("Dead", -1)
    battleManager.determine_battle_state()
    flag = battleManager.battleState == (False, "Hero Loses") and len(animationManager.deadGroup.sprites()) == 0
    # revive hero and determine if the state is changed appropriately
    knight.Status = ("Normal", -1)
    battleManager.determine_battle_state()
    animationManager.deadGroup.add(goblin)  # add goblin to the group
    # change the battle state and confirm that the boolean for animationManager has not changed
    flag2 = battleManager.battleState == (True, "") and len(animationManager.deadGroup.sprites()) == 1
    # get rid of all enemies and determine if the state is changed appropriately
    battleManager.enemies.clear()
    animationManager.deadGroup.add(goblin)  # add goblin to the group
    battleManager.determine_battle_state()
    flag3 = battleManager.battleState == (False, "Hero Wins") and len(animationManager.deadGroup.sprites()) == 0
    # check all flags
    assert flag and flag2 and flag3

def test_get_enemy_positions():
    # tests if the list gotten by this function only has tuples
    for i in range(4):
        battleManager.add_enemy(factory.create_entity("Dummy"))  # add 4 dummys
    flag = True
    posList = battleManager.get_enemy_positions()
    for a in range(len(posList)):
        # check if the list is only of tuples and the length of those tuples is 2
        flag = isinstance(posList[a], tuple) and len(posList[a]) == 2
        if not flag:
            break
    assert flag

def test_get_enemy_objects():
    flag = True
    # get a list of enemy objects
    enemyObjList = battleManager.get_enemy_objects()
    for i in range(len(enemyObjList)):
        # check if the object is of the type Enemy
        flag = enemyObjList[i].__class__.__name__ == "Enemy"
        if not flag:
            break
    assert flag

def test_apply_status_effect():
    # change the Hp to something easy to calculate
    knight.Hp = 999
    knight.Hpcap = 999
    returnableStrings = battleManager.apply_status_effect(knight)
    # check the size of returned array
    flag = len(returnableStrings) == 0
    knight.Status = ("Poison", 0)  # poison the knight
    oldCap = knight.Hpcap
    returnableStrings = battleManager.apply_status_effect(knight)
    presumedDamage = int(knight.Hpcap/100 * 10)  # should deal 10% max health damage
    # check the damage dealt and check to see if the counter for the status increased and the size of str array
    flag2 = knight.Hpcap - presumedDamage == knight.Hp and knight.Status[1] == 1 and len(returnableStrings) == 1
    # check to see if the max health damage can kill (it should)
    oldHp = knight.Hp  # store the knight's Hp before the change
    knight.Hp = 1
    returnableStrings = battleManager.apply_status_effect(knight)
    flag3 = knight.Status[0] == "Dead" and knight.Status[1] == -1 and len(returnableStrings) == 1
    knight.Hp = oldHp  # restore the knight's Hp
    knight.Status = ("Burn", 0)  # burn the knight
    oldHp = knight.Hp
    presumedDamage = int(knight.Hp/100 * 15)  # should deal 15% current health damage
    returnableStrings = battleManager.apply_status_effect(knight)
    # check the damage dealt and check to see if the counter for the status increased and the size of str array
    flag4 = oldHp - presumedDamage == knight.Hp and knight.Status[1] == 1 and len(returnableStrings) == 1
    # check to see if current health damage can kill (it shouldn't)
    knight.Hp = 1
    returnableStrings = battleManager.apply_status_effect(knight)
    flag5 = knight.Status[0] == "Burn" and knight.Hp == 1 and len(returnableStrings) == 1
    assert flag and flag2 and flag3 and flag4 and flag5

def test_handle_status_effect():
    # make the knight strong enough to handle the damage
    knight.Hp = 999  # refill Hp
    knight.Def = 700
    # prep work
    knight.Status = ("Paralyze", 0)
    battleManager.enemies.clear()  # remove all enemies
    battleManager.turnOrder.clear()  # remove current turn order
    dummy = factory.create_entity("dummy")  # create a dummy object
    dummy.Status = ("Freeze", 0)  # freeze dummy
    battleManager.add_enemy(dummy)
    # add the objects to the turn order
    battleManager.turnOrder.append(knight)
    battleManager.turnOrder.append(dummy)
    # because of how status that cause people to lose their turns works
    # we can effectively test the handle_status_effect() function by calling
    # do_one_turn, the returned string array will tell us if their turn was properly skipped
    # and the status of the character tells us if the statuses were removed, killing 2 birds with
    # one stone
    returnableStrings, refresh = battleManager.do_one_turn("", ())
    # check size of array, turn order and the status of knight object confirm that animation manager wasn't activated
    flag = len(returnableStrings) == 2 and battleManager.turnOrder[0] == dummy and knight.Status[0] == "Normal" \
        and not animationManager.active
    presumedDamage = int(dummy.Hpcap/100 * 5)  # damage we assume freeze will do
    returnableStrings, refresh = battleManager.do_one_turn("", ())
    # confirm that the animation manager isn't active
    flag2 = len(returnableStrings) == 3 and len(battleManager.turnOrder) == 0 and dummy.Hp == dummy.Hpcap - presumedDamage \
           and dummy.Status[0] == "Normal" and not animationManager.active
    returnableStrings = battleManager.handle_status(knight)
    # check to see if the count for infinite statuses stays the same
    flag3 = len(returnableStrings) == 0 and knight.Status[1] == -1
    assert flag and flag2 and flag3

def test_get_health_difference():
    battleManager.enemies.clear()
    for i in range(2):
        battleManager.add_enemy(factory.create_entity("dummy"))
    initialHp = battleManager.get_health_info()
    testDummy = battleManager.enemies[1]
    testDummy.Hp = 1
    dummyPos = testDummy.rect.midtop
    differences = battleManager.get_health_difference(initialHp)
    # checks if the name exists, there's only 1 entry in differences
    # the correct Hp difference was returned and a proper position tuple was given
    flag = len(differences) == 1 and differences.get(testDummy.altName) is not None and \
           differences[testDummy.altName]["Hp"] == -998 and differences[testDummy.altName]["Pos"] == dummyPos

    # check if increases in health register
    initialHp = battleManager.get_health_info()
    testDummy.Hp = 500
    differences = battleManager.get_health_difference(initialHp)
    flag2 = differences.get(testDummy.altName) is not None and differences[testDummy.altName]["Hp"] == 499 and \
        len(differences) == 1 and differences[testDummy.altName]["Pos"] == dummyPos
    assert flag and flag2


