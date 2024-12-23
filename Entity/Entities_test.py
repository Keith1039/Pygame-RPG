import json
import Entity

factory = Entity.EntityFactory()
jsonInfo = json.load(open("JSON/Enemies/dummy.json"))
mockEnemy = Entity.Enemy(jsonInfo)
knight = Entity.Knight()
lootpool = {"Exp": 0, "Money": 0, "Items": {}}

# Entity method tests
################################################################

# we use the knight object for the animation stuff because it has its animations done already
def test_get_max_animation_val():
    knight.maxAniVal = 0  # here to show that the max animation val didn't change
    assert knight.get_max_animation_val() == 10 and knight.maxAniVal == 0

def reset_max_animation_val():
    knight.aniStatus = "Attack1"  # change the animation
    knight.reset_max_animation_val()  # reset the max animation value
    assert knight.maxAniVal == 4

def test_update():
    knight.aniTracker = 0  # set the tracker
    knight.update()  # update
    flag = knight.aniTracker == 1  # confirm the update
    knight.aniTracker = knight.maxAniVal * 10 + 5  # make it surpass the maximum
    knight.update()  # update
    flag2 = knight.aniTracker == knight.maxAniVal * 10 + 6  # confirm that the tracker didn't get reset
    knight.update(True)  # force update
    flag3 = knight.aniTracker == 0  # confirm it reset
    knight.update(True)  # force update again
    flag4 = knight.aniTracker == 0  # confirm forced upadtes don't increment aniTracker
    knight.aniTracker = knight.maxAniVal * 10 + 9  # set it right up until the last interval
    knight.update()  # update normally
    flag5 = knight.aniTracker == 0  # confirm it reset on the interval
    # check to see if the image and rectangle were updated and the animation tracker was reset
    oldRectPos = knight.rect.center  # set the old rectangle position
    knight.x = 999  # set a new position
    knight.y = 999  # set a new position
    knight.update()  # update the knight
    # confirm that the rectangle shifted to the knight's coordinates
    flag6 = knight.rect.center != oldRectPos and knight.rect.midbottom == (knight.x, knight.y)
    assert flag and flag2 and flag3 and flag4 and flag5 and flag6


def test_take_damage():
    mockEnemy.take_damage(-900)
    mockEnemy.Def = 100  # set defence to 100
    mockEnemy.take_damage(20)  # should do no damage because of the high damage
    flag = mockEnemy.Hp == mockEnemy.Hpcap  # Hp shouldn't change
    mockEnemy.take_damage(20, True)
    flag2 = mockEnemy.Hp == mockEnemy.Hpcap - 20  # confirm that the mock enemy actually took damage
    mockEnemy.take_damage(9999)  # kill the mock enemy
    mockEnemy.Def = 1  # reset the defence to 1

    assert flag and flag2 and mockEnemy.Hp == 0 and mockEnemy.Status[0] == "Dead"

def test_apply_bonuses():
    mockEnemy.Bonuses.update({"Str": (50, 3), "Vit": (50, 3), "Agl": (50, -1), "Def": (50, 3)})  # Give enemy buffs
    mockEnemy.apply_bonuses()  # Apply the buffs to the enemy
    flag = True
    for stat, bonuses in mockEnemy.Bonuses.items():
        # Compare the JSON information to buffed Enemy object and confirm the turn count of the bonus has decreased
        # The only exception to this is Agl since infinite duration bonuses do not get decremented.
        flag = jsonInfo[stat] + 50 == mockEnemy.__dict__[stat] and (bonuses[1] == 2 or stat == "Agl" and bonuses[1] == -1)
        if not flag:  # If this is ever untrue, break the loop
            break
    assert flag

def test_remove_bonuses():
    mockEnemy.Bonuses.update({"Vit": (50, 0)})  # Update the bonus counter for Vitality to be 0
    mockEnemy.remove_bonuses()
    flag = True
    for stat, bonuses in mockEnemy.Bonuses.items():
        # In this case the json information and Enemy object attributes should be identical after buffs are removed
        flag = jsonInfo[stat] == mockEnemy.__dict__[stat]
        if not flag:  # if this isn't the case break the loop
            break
    flag2 = mockEnemy.Bonuses["Vit"] == (0, -1)  # The buff should be removed since the counter for it was zero
    assert flag and flag2


################################################################


# Enemy method tests
################################################################

def test_take_attack():
    mockEnemy.take_attack(500, lootpool)
    assert lootpool["Exp"] == 1 and lootpool["Money"] == 1 and lootpool["Items"]["Potion"] == 1

################################################################

# Knight method tests
################################################################

def test_level_up():
    knightLvl = knight.Lvl
    growthsDict = knight.growths.copy()  # copy of the dictionary before level up
    knight.Exp = knight.Expcap
    knight.level_up()
    flag = True
    for stat in growthsDict:
        flag = growthsDict[stat] < knight.growths[stat]  # The stat growth should be higher with each level
        if not flag:
            break  # break early if this is not true
    assert knight.Exp == 0 and flag and knightLvl + 1 == knight.Lvl

def test_get_rewards():
    # Tests if the player character gets rewards from lootpool correctly
    knightLvl = knight.Lvl  # level before the level up
    lootpool["Exp"] = knight.Expcap  # Rig a level up
    knight.get_rewards(lootpool)  # The first should trigger a level up and add potion to inventory
    knight.get_rewards(lootpool)  # Testing to see if a second potion is added
    assert knight.Inventory["Potion"] == 2 and knight.Bal == 2 and knight.Lvl == knightLvl + 1

def test_inventory_to_list():
    # test if the inventory list has the proper elements and has the proper size
    knight.Inventory.update({"Burn Heal": 1})
    inventoryCopy = knight.inventory_to_list().copy()
    assert "Potion x2" in inventoryCopy and "Burn Heal" in inventoryCopy and len(inventoryCopy) == 2

def test_correct_inventory():
    # tests if the function removes the Elixir key
    knight.Inventory.update({"Elixir": 0})
    inventoryDictLen = len(knight.Inventory)
    knight.correct_inventory()
    assert inventoryDictLen == len(knight.Inventory) + 1 and knight.Inventory.get("Elixir") is None

def test_equip():
    # equip and un-equip an item
    # ItemManager tests if the stats change
    # check if the stats are properly corrected after equipment changes
    itemManager = Entity.ItemManager(knight)
    equipmentName = "Leather Cap"
    oldHp = knight.Hp
    equipment = Entity.Equipment(equipmentName, itemManager.equipmentJson[equipmentName])
    knight.equip(equipment)
    knight.Hp = knight.Hpcap  # make Hp equal tot he Hpcap
    flag = knight.equipment[equipment.type] == equipment
    knight.equip(equipment, remove=True)  # remove the equipment
    flag2 = knight.equipment[equipment.type] is None
    assert flag and flag2 and oldHp == knight.Hp

def test_add_to_inventory():
    knight.Inventory.clear()  # remove everything from inventory
    knight.add_to_inventory("Potion")  # add 1 potion to inventory
    knight.add_to_inventory("Bomb")  # add 1 bomb to inventory
    knight.add_to_inventory("Potion", 2)  # add another 2 potions to the inventory
    # check if the inventory is of the right size
    # checks if the inventory has the proper amounts of each item
    assert len(knight.Inventory) == 2 and knight.Inventory["Potion"] == 3 and knight.Inventory["Bomb"] == 1
def test_remove_from_inventory():
    knight.remove_from_inventory("Potion", 2)  # remove 2 Potions from inventory
    knight.remove_from_inventory("Bomb")  # remove 1 bomb from inventory
    # bomb should have been removed from the inventory
    assert len(knight.Inventory) == 1 and knight.Inventory["Potion"] == 1

################################################################

# Entity Factory tests
################################################################

def test_create_entity():
    name = "Goblin"
    entity1 = factory.create_entity(name)
    entity2 = factory.create_entity(name)
    # check the names
    flag = entity1.altName == name and entity2.altName == (name + "2")
    assert flag and factory.createdCount[name] == 2

def test_clear_created_count():
    # test if the clear works
    factory.clear_created_count()
    assert len(factory.createdCount) == 0
