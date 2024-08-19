from Entity import Knight
from managers import ItemManager
from managers import BattleManager

knight = Knight()

itemManager = ItemManager(knight)


def test_determine_limited():
    # determine if the super bomb item is limited when Knight has no Super Bombs
    flag = itemManager.determine_limited("Super Bomb")
    knight.Inventory.update({"Super Bomb": 1})  # give knight a limited item
    # determine if the super bomb item is limited when Knight has a Super Bomb
    flag2 = itemManager.determine_limited("Super Bomb")
    knight.Inventory.clear()  # remove all items
    assert flag and not flag2

def test_get_all_purchasable():
    tempDict = {}
    # fill the temp dict with all purchasable items
    for item, itemInfo in itemManager.itemJson.items():
        if itemInfo["Purchasable"]:
            tempDict.update({
                item: itemInfo
            })
    # check if the temporary dict matches the dict we get from the function call
    flag = tempDict.keys() == itemManager.get_all_purchasable().keys()
    knight.Inventory.update({"Elixir": 1})  # add a limited item to the knight's inventory
    purchasableItems = itemManager.get_all_purchasable()
    # check if the purchasableItems dict is missing the limited item and only the limited item
    flag2 = len(tempDict) == len(purchasableItems) + 1 and purchasableItems.get("Elixir") is None
    assert flag and flag2

def test_get_all_sellable():
    nonKeyItemsDict = itemManager.get_all_sellable()  # set the value of the dictionary with no key items
    keyItemsDict = {}
    # if the item is a key item, add it to the dictionary for key items
    for item, itemInfo in itemManager.itemJson.items():
        if itemInfo["Type"] == "Key":
            keyItemsDict.update({
                item: itemInfo
            })
    # check to see if the 2 dictionaries are the same length as the dict of all items
    assert len(itemManager.itemJson) == (len(nonKeyItemsDict) + len(keyItemsDict))

def test_get_effect_detail():
    # tests the behavior of the get_effect_details() function
    effectDetail1 = itemManager.get_effect_details("Bomb")
    effectDetail2 = itemManager.get_effect_details("Potion")
    effectList = [effectDetail1, effectDetail2]
    effectDetail3 = itemManager.get_effect_details("Longsword")
    flag = True
    # verifies that, for a valid item with an effect, non-empty key and value pairs are given
    for i in range(len(effectList)):
        effectDetail = effectList[i]
        for item, string in effectDetail.items():
            flag = string != ""
            if not flag:
                break
        if not flag:
            break
    flag2 = True
    # verifies that, for an invalid item, the dictionary only contains empty string values paired to the keys
    for item, string in effectDetail3.items():
        flag2 = string == ""
        if not flag2:
            break
    assert flag and flag2
def test_get_effect():
    # check if the function works by giving it a valid and invalid item
    effectString1 = itemManager.get_effect("Potion")
    effectString2 = itemManager.get_effect("Longsword")
    assert effectString1 != "" and effectString2 == ""

def test_get_parsable_item_info():
    parsableDict = itemManager.get_parsable_item_info("Potion")
    parsableDict2 = itemManager.get_parsable_item_info("Longsword")
    # A list of all values that should be in the returned dictionaries
    values = ["Type", "Effect", "Buy", "Sell", "Description"]
    flag = True
    # go through the first dicts keys and check the keys
    for key in parsableDict:
        if key not in values:
            flag = False
            break
    flag2 = True
    # go through the second dicts keys and check the keys
    for key in parsableDict:
        if key not in values:
            flag2 = False
            break
    # check the flags and check if the effect string for an item with an effect
    assert flag and flag2 and parsableDict["Effect"] != "" and parsableDict2["Effect"] == ""

def test_get_usable_items():
    knight.Inventory.clear()  # get rid of all of Knight's items
    # confirm that Knight object has no usable items
    # this also checks if the function breaks when inventory is empty
    flag = len(itemManager.get_usable_items()) == 0
    # give knight some items
    knight.Inventory.update({
            "Moonstone": 1,  # a limited material
            "Elixir": 1,  # a limited, usable item
            "Gospel Of The Dragons": 1  # a book
    })
    assert flag and len(itemManager.get_usable_items()) == 1

def test_fuse_items():
    knight.Inventory.update({"Old Map": 1})
    flag = itemManager.fuse_items("Elixir", "Moonstone")
    flag2 = itemManager.fuse_items("Moonstone", "Old Map")
    flag3 = knight.Inventory.get("Old Map") is None and knight.Inventory.get("Moonstone") is None
    assert not flag and flag2 and flag3

def test_item_compatibility():
    # this series of tests checks if the item effects can be parsed by battleManager
    battleManager = BattleManager(knight, itemManager)  # init BattleManager
    staticHealingEffect = itemManager.get_effect("Potion")  # get an effect string that heals the user by X amount
    percentageHealingEffect = itemManager.get_effect("Dragon Tear")  # get an effect that heals on a percentage
    burnHealEffect = itemManager.get_effect("Ointment")  # get the effect to heal Burn
    bleedHealEffect = itemManager.get_effect("Bandages")  # get the effect to heal Bleed
    multiEffect = itemManager.get_effect("Elixir")  # get an item that has multiple effects
    # setting up knight object stats
    knight.Status = ("Burn", 0)
    knight.Hpcap = 999
    knight.Hp = 20
    knight.Mpcap = 999

    # set up the effect strings
    healingEffectString = battleManager.parse_effects(staticHealingEffect)
    percentageHealingEffectString = battleManager.parse_effects(percentageHealingEffect)
    burnHealEffectString = battleManager.parse_effects(burnHealEffect)
    bleedHealEffectString = battleManager.parse_effects(bleedHealEffect)
    multiEffectString = battleManager.parse_effects(multiEffect)
    # all effects are self so a target doesn't matter
    battleManager.apply_effects(healingEffectString, knight, None)
    flag = knight.Hp == 120  # knight should have healed 100 Hp from potion effect
    battleManager.apply_effects(bleedHealEffectString, knight, None)
    flag2 = knight.Status[0] == "Burn"  # using bandages on a burn shouldn't cure it
    battleManager.apply_effects(burnHealEffectString, knight, None)
    flag3 = knight.Status[0] == "Normal"  # burn should have been healed by the effect
    battleManager.apply_effects(percentageHealingEffectString, knight, None)
    flag4 = 120 + int(.5 * knight.Hpcap) == knight.Hp  # the knight should have been healed by 50% of their max Hp
    knight.Status = ("Bleed", 0)  # make the knight object have the Bleed status
    battleManager.apply_effects(multiEffectString, knight, None)
    flag5 = knight.Hp == (knight.Hpcap + 120 + int(.5 * knight.Hpcap)) and knight.Status[0] == "Normal" and \
            knight.Mp - 1 == knight.Mpcap
    assert flag and flag2 and flag3 and flag4 and flag5




