import json
import Entity

jsonInfo = json.load(open("JSON/Enemies/dummy.json"))
mockEnemy = Entity.Enemy(jsonInfo)
knight = Entity.Knight()
lootpool = {"Exp": 0, "Money": 0, "Items": {}}

# Entity method tests
################################################################


def test_take_damage():
    mockEnemy.take_damage(-900)
    flag = mockEnemy.Hp == mockEnemy.Hpcap  # Hp shouldn't change
    mockEnemy.take_damage(9999)
    assert flag and mockEnemy.Hp == 0 and mockEnemy.Status == "Dead"

def test_apply_bonuses():
    mockEnemy.Bonuses.update({"Str": (50, 3), "Vit": (50, 3), "Agl": (50, -1), "Defence": (50, 3)})  # Give enemy buffs
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

################################################################

