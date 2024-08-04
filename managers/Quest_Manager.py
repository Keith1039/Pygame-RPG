import json
class QuestManager:
    def __init__(self, knight):
        self.questDict = get_quest_dict()
        self.knight = knight  # reference to the knight object
        self.activeQuests = []  # a list of quests the player is engaging in
        self.completedQuests = []  # a list of quests completed by the player
        self.enemiesKilled = {}  # a dictionary of enemy types mapped to the amount the player has killed them
        self.npcsInteractedWith = {}  # a dictionary of NPCs mapped to how many times the player interacted with them

    def add_quest(self, questName):  # adds a quest to the activeQuest list if the questName exists
        quest = self.questDict.get(questName)
        if quest is not None:
            self.activeQuests.append(quest)

    def get_all_keys_from_quest_targets(self):
        # returns all the relevant keys from the dictionary
        finalList = []
        for d in self.activeQuests:
            finalList += list(d["Target"].keys())
        return finalList

    def remove_unnecessary_keys(self):
        # function that removes the keys that aren't involved in any quest
        # this removes from the enemiesKilled and the npcsInteractedWith dictionaries
        relevantKeys = self.get_all_keys_from_quest_targets()
        deleteList = []  # list of keys we need to delete
        for key in self.enemiesKilled.keys():
            if key not in relevantKeys:
                deleteList.append(key)  # if the key is not relevant add it to the list
        # loop through and delete irrelevant keys
        for key in deleteList:
            self.enemiesKilled.pop(key)
        deleteList.clear()  # clear the delete list
        # do the same but for NPCs that we interact with
        for key in self.npcsInteractedWith:
            if key not in relevantKeys:
                deleteList.append(key)
        # loop through and delete irrelevant keys
        for key in deleteList:
            self.npcsInteractedWith.pop(key)

    def check_for_completion(self, context, x):
        # checks if any active quest has been completed
        # if the quest has been completed, the quest is moved from the
        # active list to the completed list
        newActiveQuests = []  # a list of quests that have yet to be completed
        nextQuests = []  # a list of quests to be added from completed quest
        for quest in self.activeQuests:
            questType = quest["Quest Type"]  # the type of quest
            completed = False  # flag that tells us if the quest is completed
            if questType == "Slay":  # quests about killing monsters
                # check to see if the player has killed the enemies
                if quest["Target"].items()  <= self.enemiesKilled.items():
                    completed = True  # set completed to true
            elif questType == "Obtain":  # quests about getting items
                # checks to see if the target has already been obtained in the player's inventory
                if quest["Target"].items() <= self.knight.Inventory.items():
                    completed = True  # set completed to true
            elif questType == "Arrive":  # quests about reaching a new destination
                x_range = quest["Range"]
                # check if the context and see if the player is within range
                if context == quest["Context"] and x_range[0] < x < x_range[1]:
                    completed = True
            elif questType == "Interact":  # quests about talking to NPCs
                pass
            if completed:
                self.knight.get_rewards(quest["Reward"])  # get the rewards of the fight
                if quest["Next Quest"] != "":  # check if there's a next quest in the chain
                    nextQuests.append(quest["Next Quest"])  # add the quest to a list
                self.completedQuests.append(quest)  # add the completed quest to the list of completed quests
            else:
                newActiveQuests.append(quest)  # add it to the new active quest list
        self.activeQuests = newActiveQuests  # set the new list
        for questName in nextQuests:  # loop through the list
            self.add_quest(questName)  # add the new quests
        self.remove_unnecessary_keys()  # remove unnecessary keys from dictionaries


def get_quest_dict():
    file = open("JSON/Quests/Quests.json", "r")
    questDict = json.load(file)
    file.close()
    return questDict




