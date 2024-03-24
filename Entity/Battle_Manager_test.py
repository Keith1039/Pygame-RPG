from Entity.Knight import Knight
from Entity.Entity_Factory import EntityFactory
from Entity.Battle_Manager import BattleManager
from Entity.Move import Move
import pygame as game
from managers.UI_Manager import UIManager

game.init()
screen = game.display.set_mode((1422, 800))
font = game.font.Font('font/Pixeltype.ttf', 50)
uiManager = UIManager(font, screen)

factory = EntityFactory()
knight = Knight()
dummy = factory.create_entity("dummy")
battleManager = BattleManager(knight)
effectListMatrix = []
# creating move objects
attack = Move("Attack", dummy, battleManager.moveDict["Attack"])
buffEffectMove = Move("Angry Shout", dummy, battleManager.moveDict["Angry Shout"])
immediateMove = Move("Pilfering Strike", dummy, battleManager.moveDict["Pilfering Strike"])
healMove = Move("Drink Potion", dummy, battleManager.moveDict["Drink Potion"])

def test_add_enemy():
    flag = False
    for i in range(6):
        battleManager.add_enemy(dummy)
        flag = battleManager.enemies[i][1] == dummy and \
               battleManager.enemies[i][0] == (900 + int(i / 3) * 300, 100 + int(i % 3) * 250)
        if not flag:
            break
    # clear the list and re-add one dummy to the list of enemies
    battleManager.enemies.clear()
    battleManager.add_enemy(dummy)
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
    battleManager.apply_effect_buff(dummy, {"Defence": defBuff})
    # Checks if the defence buff was successfully applied
    # Check if the buffs that were applied before are still applied after the apply_effect_buff() call
    # This implicitly checks if the turn counts were altered
    assert dummy.Bonuses["Str"] == strBuff and dummy.Bonuses["Agl"] and dummy.Bonuses["Defence"] == defBuff

def test_apply_effects():
    knight.Bal = 20  # setting knight Bal attribute
    oldDummyHp = dummy.Hp  # saving the dummy's Hp before it is changed by effect
    eventStrings = []
    for i in range(len(effectListMatrix)):
        effectList = effectListMatrix[i]  # gets the current effect list
        # run apply_effects() and add to the list of event strings
        eventStrings = eventStrings + battleManager.apply_effects(effectList, dummy, knight)
    # Check if all the effects were properly applied
    assert dummy.Bonuses["Str"] == (5, 3) and knight.Bal == 0 and oldDummyHp + 20 == dummy.Hp and len(eventStrings) == 3

def test_use_move():
    # Buffing knight object's stats, so they survive the dummy object's attack
    knight.Bal = 20  # give knight 20 dollar for him to get robbed again
    knight.Hp = 999
    knight.Hpcap = 999
    knight.Defence = 700
    # reset eventStrings and make a new list of event strings
    eventStrings = []
    eventStrings = eventStrings + battleManager.use_move(dummy, attack, [knight])  # this should do exactly 99 damage
    eventStrings = eventStrings + battleManager.use_move(dummy, buffEffectMove, [knight])
    eventStrings = eventStrings + battleManager.use_move(dummy, immediateMove, [knight])  # does 0 damage
    eventStrings = eventStrings + battleManager.use_move(dummy, healMove, [knight])
    # check if the knight's attributes to see if they're affected, check if the dummy's Mp decreased
    assert knight.Bal == 0 and knight.Hp == 900 and dummy.Mp == dummy.Mpcap - 120 and len(eventStrings) == 9

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
    battleManager.enemies[0][1].Status = "Dead"  # Change Dummy status to Dead
    battleManager.clear_dead_enemies()  # clear the dead enemies
    # Check if the enemies list is empty and only the hero object should be in turn order now
    assert len(battleManager.enemies) == 0 and len(battleManager.turnOrder) == 1

def test_fix_entity_stats():
    knight.Hp = 999
    knight.Hpcap = 9
    knight.Bal = - 100
    battleManager.add_enemy(factory.create_entity("dummy"))  # re-add a new dummy to list of enemies
    battleManager.enemies[0][1].Mpcap = 1
    battleManager.turnOrder.clear()  # reset the turnOrder
    battleManager.reset_turn_order()  # Add all alive entities to the turn order
    battleManager.fix_entity_stats()
    # check to see if the health, mana and bal values have been changed
    assert knight.Hp == 9 and knight.Bal == 0 and battleManager.enemies[0][1].Mp == 1

def test_get_entity_from_pos():
    # clear and re-add a dummy object
    battleManager.enemies.clear()
    dummy = factory.create_entity("dummy")
    battleManager.add_enemy(dummy)
    pos = battleManager.heroPos
    entity = battleManager.get_entity_from_pos(pos)
    pos = (900, 100)
    entity2 = battleManager.get_entity_from_pos(pos)
    assert entity == knight and entity2 == dummy

def test_determine_battle_state():
    # kill hero and see if the state is changed appropriately
    knight.Status = "Dead"
    battleManager.determine_battle_state()
    flag = battleManager.battleState == (False, "Hero Loses")
    # revive hero and determine if the state is changed appropriately
    knight.Status = "Normal"
    battleManager.determine_battle_state()
    flag2 = battleManager.battleState == (True, "")
    # get rid of all enemies and determine if the state is changed appropriately
    battleManager.enemies.clear()
    battleManager.determine_battle_state()
    flag3 = battleManager.battleState == (False, "Hero Wins")
    # check all of the flags
    assert flag and flag2 and flag3




