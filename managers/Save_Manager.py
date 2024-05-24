from managers.Screen_Manager import ScreenManager
from Entity.Knight import Knight
import os, json
class SaveManager:
    def __init__(self, hero,  localVars, screenManager, saveNumber=1):
        self.hero = hero
        self.localVars = localVars
        self.screenManager = screenManager
        self.saveNumber = saveNumber
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
        if self.saveNumber <= self.limit and self.saveNumber > 0:
            # Saves in the most recent slot
            self.file = open(self.file.name, "w")
            gameValues = self.strip_non_json_and_save()
            json.dump(gameValues, self.file, indent=3)
            self.file.close()
            self.store_save_info()
        else:
            print("Invalid Slot")

    def save(self, slot=int):
        # Saves in a specified slot
        if slot > 0 and slot <= self.limit:
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
        # Animation trackers are saved because I have a feeling removing them is gonna give a scuffed edge case
        allowed = ["animationTracker", "animationTracker2", "animationTracker3", "gameState", "x"]
        rawVarsDict = {}  # The raw values I need for the game (stuff in allowed)
        inventoryDict = {}  # Players inventory
        for key in self.localVars:
            if key in allowed:
                rawVarsDict[key] = self.localVars[key]

        # Here to turn the events from the dict to their dictionary form for JSON serialization
        interactablesVars = {}
        for key in self.screenManager.interactablesDict:
            eventsVar = []
            eventsTuple = self.screenManager.interactablesDict[key]
            for i in range(len(eventsTuple)):
                eventsVar.append(vars(eventsTuple[i]))
            interactablesVars.update({key: tuple(eventsVar)})
        screenManagerDict = {"context": self.screenManager.context, "objectDict": self.screenManager.objectDict,
                            "interactablesDict": interactablesVars}
        newerdict = {"Knight": vars(self.hero), "rawVariables": rawVarsDict, "screenManager": screenManagerDict,  "Inventory": inventoryDict}
        return(newerdict)

    def load_data(self, file):
        fileInfo = json.load(file)
        self.hero.load_dict(fileInfo["Knight"])  # Loading knight
        for stat, bonus in self.hero.Bonuses.items():  # turn all the list bonuses to tuples
            self.hero.Bonuses.update({stat: tuple(bonus)})
        self.hero.Status = tuple(self.hero.Status)  # turn the list for status into a tuple
        self.screenManager.objectDict = fileInfo["screenManager"]["objectDict"]
        self.screenManager.change_context(fileInfo["screenManager"]["context"])
        interactablesInfo = fileInfo["screenManager"]["interactablesDict"]
        # Loads the event objects with the correct values
        for key in interactablesInfo:
            dictArray = interactablesInfo[key]
            for i in range(len(dictArray)):
                eventDict = dictArray[i]
                self.screenManager.interactablesDict[key][i].load(eventDict)
        tuplefy(self.screenManager.objectDict)
        for key in self.localVars:  # Fill the local variables
            if fileInfo["rawVariables"].get(key) is not None:
                self.localVars[key] = fileInfo["rawVariables"][key]
        file.close()

    def quick_load(self):
        if self.saveNumber <= self.limit and self.saveNumber > 0:
            # Loads the most recent save, a 'Continue' option
            # Users will be able to pick the save file graphically (hopefully) so no error checking should be required
            file = open("save/save_data" + str(self.saveNumber) + ".json", "r")
            self.load_data(file)
        else:
            print("Invalid file")

    def load(self, slot=int):
        if slot <= self.limit and slot > 0:  # Verifies if the file exists
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
