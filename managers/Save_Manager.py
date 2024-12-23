from managers.Screen_Manager import ScreenManager
from Entity.Knight import Knight
from Entity.NPC_Manager import NPCManager
from Entity.Object_Manager import ObjectManager
import os
import json
class SaveManager:
    def __init__(self, knight,  localVars, screenManager, eventManager, questManager, npcManager, objectManager,
                 saveNumber=1):
        self.knight = knight
        self.localVars = localVars
        self.screenManager = screenManager
        self.saveNumber = saveNumber
        self.eventManager = eventManager
        self.questManager = questManager
        self.npcManager = npcManager
        self.objectManager = objectManager
        self.limit = 4
        # Makes the initial save file
        
        if "prev_save_info.json" not in os.listdir("save/"):
            self.file = open("save/save_data" + str(self.saveNumber) + ".json", "w")
            
        else:
            file = open("save/prev_save_info.json", "r")
            info = json.load(file)
            self.saveNumber = info["lastSave"]
            self.file = open("save/save_data" + str(self.saveNumber) + ".json", "r")
            file.close()
            self.file.close()
        
        
    def store_save_info(self):
        file = open("save/prev_save_info.json", "w")
        json.dump({"lastSave": self.saveNumber}, file, indent=3)
        file.close()
    
    # REMEMBER TO ERROR PROOF THIS. MAYBE OVERWRITE SLOT 0 OR READ FROM SLOT 0 IF AN INVALID SLOT IS GIVEN
    # The above is if someone edits file data
    def quick_save(self):
        if 0 < self.saveNumber <= self.limit:
            # Saves in the most recent slot
            self.file = open(self.file.name, "w")
            gameValues = self.strip_non_json_and_save()
            json.dump(gameValues, self.file, indent=3)
            self.file.close()
            self.store_save_info()
        else:
            print("Invalid Slot")

    def save(self, slot):
        # Saves in a specified slot
        if 0 < slot <= self.limit:
            self.saveNumber = slot
            self.file = open("save/save_data" + str(slot) + ".json", "w")
            gameValues = self.strip_non_json_and_save()
            json.dump(gameValues, self.file, indent=3)
            self.file.close()
        else:
            print("Invalid slot")
        self.store_save_info()

    def strip_non_json_and_save(self):
        # Creates a dict with the local variables that are json serializeable. Also formats object data
        # Animation trackers are saved because removing them might cause a weird edge case
        allowed = ["animationTracker", "animationTracker2", "animationTracker3", "gameState"]
        rawVarsDict = {}  # The raw values I need for the game (stuff in allowed)
        if (self.knight.aniTracker // 10 + 1) > self.knight.maxAniVal:  # check to see if Knight has an illegal value
            self.knight.update(True)  # force the update
        knightDict = {
            "fieldStatus": self.knight.fieldStatus,
            "aniStatus": self.knight.aniStatus,
            "aniTracker": self.knight.aniTracker,
            "x": self.knight.x,
            "y": self.knight.y,
            "flipped": self.knight.flipped,
            "Name": self.knight.Name,
            "Sprite": self.knight.Sprite,
            "Status": self.knight.Status,
            "Lvl": self.knight.Lvl,
            "Hpcap": self.knight.Hpcap,
            "Hp": self.knight.Hp,
            "Mpcap": self.knight.Mpcap,
            "Mp": self.knight.Mp,
            "Exp": self.knight.Exp,
            "Bal": self.knight.Bal,
            "Str": self.knight.Str,
            "Mag": self.knight.Mag,
            "Vit": self.knight.Vit,
            "Agl": self.knight.Agl,
            "Def": self.knight.Def,
            "moveList": tuple(self.knight.moveList),
            "equipment": self.knight.equipment,
            "Inventory": self.knight.Inventory
        }
        for key in self.localVars:
            if key in allowed:
                rawVarsDict[key] = self.localVars[key]
        screenManagerDict = {"context": self.screenManager.context, "objectDict": self.screenManager.objectDict,
                            "interactablesDict": self.screenManager.interactablesDict}
        questManagerDict = {
            "activeQuests": self.questManager.activeQuests,
            "completedQuests": self.questManager.completedQuests,
            "enemiesKilled": self.questManager.enemiesKilled,
            "npcsInteractedWith": self.questManager.npcsInteractedWith
        }
        self.npcManager.save_and_empty()  # save current changes to the dictionary
        self.npcManager.get_NPCs(self.screenManager.context)  # get the NPCs back
        self.objectManager.save_and_empty()  # save current changes to the dictionary
        self.objectManager.get_objects(self.screenManager.context)  # get the objects back
        newerdict = {"Knight": knightDict, "questManager": questManagerDict, "rawVariables": rawVarsDict,
                     "screenManager": screenManagerDict, "eventDict": self.eventManager.eventDict,
                     "NPCDict": self.npcManager.interactableDict,
                     "objectDict": self.objectManager.interactableDict}
        return newerdict

    def load_data(self, file):
        fileInfo = json.load(file)
        self.knight.load_dict(fileInfo["Knight"])  # Loading knight
        self.questManager.__dict__.update(fileInfo["questManager"])  # load questManager
        for stat, bonus in self.knight.Bonuses.items():  # turn all the list bonuses to tuples
            self.knight.Bonuses.update({stat: tuple(bonus)})
        self.screenManager.objectDict = fileInfo["screenManager"]["objectDict"]
        self.screenManager.change_context(fileInfo["screenManager"]["context"])
        interactablesInfo = fileInfo["screenManager"]["interactablesDict"]
        self.npcManager.interactableDict = fileInfo["NPCDict"]  # set the NPC dict
        self.npcManager.get_NPCs(self.screenManager.context)  # reset the NPCs
        self.objectManager.interactableDict = fileInfo["objectDict"]  # set the Object dict
        self.objectManager.get_objects(self.screenManager.context)  # reset the objects
        self.eventManager.eventDict = fileInfo["eventDict"]
        # convert all lists to tuples in the dict

        # Loads the event objects with the correct values
        self.screenManager.interactablesDict = tuplefy2(interactablesInfo)
        tuplefy(self.screenManager.objectDict)
        for key in self.localVars:  # Fill the local variables
            if fileInfo["rawVariables"].get(key) is not None:
                self.localVars[key] = fileInfo["rawVariables"][key]
        file.close()

    def quick_load(self):
        if 0 < self.saveNumber <= self.limit:
            # Loads the most recent save, a 'Continue' option
            # Users will be able to pick the save file graphically (hopefully) so no error checking should be required
            file = open("save/save_data" + str(self.saveNumber) + ".json", "r")
            self.load_data(file)
        else:
            print("Invalid file")

    def load(self, slot):
        if 0 < slot <= self.limit:  # Verifies if the file exists
            file = open("save/save_data" + str(slot) + ".json", "r")
            self.load_data(file)
        else:
            print("Invalid file")


def tuplefy(arrayDict):
    for key in arrayDict:
        array = arrayDict[key]
        for i in range(len(array)):
            if type(array[i]) == list:
                array[i] = tuple(array[i])
        arrayDict[key] = tuple(arrayDict[key])
    return arrayDict

def tuplefy2(dictionaryDict):
    # this is for event dictionaries
    newDict = dictionaryDict.copy()
    for context in dictionaryDict:
        tmpList = newDict[context]
        for i in range(len(tmpList)):  # iterate through the list
            tmpDict = tmpList[i]
            for key, value in tmpDict.items():
                if type(value) == list:
                    tmpDict.update({key: tuple(value)})  # turn all lists values into tuple
        newDict.update({context: tuple(tmpList)})  # make the list a tuple
    return newDict

