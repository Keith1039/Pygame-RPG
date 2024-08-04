from managers.Quest_Manager import *
from managers import Knight

knight = Knight()
questManager = QuestManager(knight)

def test_add_quest():
    invalidName = "esfasfasfas"
    validName = "testQuest"
    questManager.add_quest(invalidName)
    flag = len(questManager.activeQuests) == 0  # confirm that the quest wasn't added
    questManager.add_quest(validName)
    flag2 = len(questManager.activeQuests) == 1  # confirm that the quest was added
    assert flag and flag2

def test_get_all_keys_from_quest_targets():
    # check if the list has the correct size and the only key in there is correct
    relevantKeys = questManager.get_all_keys_from_quest_targets()
    assert len(relevantKeys) == 1 and relevantKeys[0] == "Potion"

def test_remove_unnecessary_keys():
    questManager.enemiesKilled.update({"Ogre": 50})
    questManager.npcsInteractedWith.update({"Lucy": 1})
    questManager.remove_unnecessary_keys()  # remove the unnecessary keys
    # check that the two dictionaries are empty
    assert len(questManager.enemiesKilled) == 0 and len(questManager.npcsInteractedWith) == 0

def test_check_for_completion():
    questManager.check_for_completion("", 0)  # check if quests are completed
    # check to see if the quest wasn't completed
    flag = len(questManager.activeQuests) == 1 and len(questManager.completedQuests) == 0
    knight.Inventory.update({"Potion": 1})  # add the quest item we need
    questManager.check_for_completion("", 0)  # check again
    # check if the quest was completed and a new quest was added
    flag2 = len(questManager.activeQuests) == 1 and len(questManager.completedQuests) == 1
    questManager.check_for_completion("", 0)  # check if quest is completed
    flag3 = len(questManager.activeQuests) == 1 and len(questManager.completedQuests) == 1
    questManager.check_for_completion("Background2", 550)  # check if quest is completed (it should this time)
    # check if knight got the rewards from the quest correctly and if the quest was completed
    flag4 = knight.Lvl == 2 and knight.Bal == 100 and knight.Inventory.get("Potion") == 2 and \
        len(questManager.activeQuests) == 1 and len(questManager.completedQuests) == 2
    questManager.enemiesKilled.update({"Goblin": 0})  # add a goblin entry for enemies killed
    questManager.check_for_completion("", 0)  # check if quest is completed (it shouldn't be)
    # check if the quest was not completed and confirm that the entry for goblin is still there
    flag5 = len(questManager.activeQuests) == 1 and len(questManager.completedQuests) == 2 and \
        questManager.enemiesKilled.get("Goblin") is not None
    questManager.enemiesKilled.update({"Goblin": 1, "Kobald": 40, "Dragon": 50})
    questManager.check_for_completion("", 0)  # check if the quest was completed (it was)
    # check if the quest was completed and added to the completed count and confirm the added keys were deleted
    flag6 = len(questManager.activeQuests) == 0 and len(questManager.completedQuests) == 3 and \
        len(questManager.enemiesKilled) == 0
    assert flag and flag2 and flag3 and flag4 and flag5 and flag6
