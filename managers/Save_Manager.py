import os, json
from managers.Screen_Manager import ScreenManager
class SaveManager:
    def __init__(self, hero,  localVars, saveNumber=0):
        self.hero = hero
        self.localVars = localVars
        self.saveNumber = saveNumber
        self.limit = 5
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
    def quick_save(self, screenManager=ScreenManager):
        if self.saveNumber <= self.limit and self.saveNumber >= 0:
            # Saves in the most recent slot
            self.file = open(self.file.name, "w")
            gameValues = self.strip_non_json_and_save(screenManager)
            json.dump(gameValues, self.file, indent=3)
            self.file.close()
            self.store_save_info()
        else:
            print("Invalid Slot")

    def save(self, slot=int, screenManager=ScreenManager):
        # Saves in a specified slot
        if slot > 0 and slot <= self.limit:
            self.saveNumber = slot
            self.file = open("save/save_data" + str(slot) + ".json", "w")
            gameValues = self.strip_non_json_and_save(screenManager)
            json.dump(gameValues, self.file, indent=3)
            self.file.close()
        else:
            print("Invalid slot")
        self.store_save_info()

    
    def strip_non_json_and_save(self, screenManager=ScreenManager):
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
        for key in screenManager.interactablesDict:
            eventsVar = []
            eventsTuple = screenManager.interactablesDict[key]
            for i in range(len(eventsTuple)):
                eventsVar.append(vars(eventsTuple[i]))
            interactablesVars.update({key: tuple(eventsVar)})
        screenManagerDict= {"context": screenManager.context, "objectDict": screenManager.objectDict,
                            "interactablesDict": interactablesVars}
        newerdict = {"Knight": dict(vars(self.hero)), "rawVariables": rawVarsDict, "screenManager": screenManagerDict,  "Inventory": inventoryDict}
        return(newerdict)

    def load_data(self, file, screenManager=ScreenManager):
        fileInfo = json.load(file)
        self.hero.load_dict(fileInfo["Knight"])  # Loading knight
        screenManager.objectDict = fileInfo["screenManager"]["objectDict"]
        screenManager.change_context(fileInfo["screenManager"]["context"])
        interactablesInfo = fileInfo["screenManager"]["interactablesDict"]
        # Loads the event objects with the correct values
        for key in interactablesInfo:
            dictArray = interactablesInfo[key]
            for i in range(len(dictArray)):
                eventDict = dictArray[i]
                screenManager.interactablesDict[key][i].load(eventDict)
        for key in screenManager.objectDict:
            tuplefy(screenManager.objectDict[key])
            screenManager.objectDict[key] = tuple(screenManager.objectDict[key])
        for key in self.localVars:  # Fill the local variables
            if fileInfo["rawVariables"].get(key) is not None:
                self.localVars[key] = fileInfo["rawVariables"][key]
        file.close()

    def quick_load(self, screenManager=ScreenManager):
        if self.saveNumber <= self.limit and self.saveNumber >= 0:
            # Loads the most recent save, a 'Continue' option
            # Users will be able to pick the save file graphically (hopefully) so no error checking should be required
            file = open("save/save_data" + str(self.saveNumber) + ".json", "r")
            self.load_data(file, screenManager)
        else:
            print("Invalid file")

    def load(self, slot=int, screenManager=ScreenManager ):
        if slot <= self.limit and slot >= 0:
            file = open("save/save_data" + str(slot) + ".json", "r")
            self.load_data(file, screenManager)
        else:
            print("Invalid file")


def tuplefy(array):
    for i in range(len(array)):
        if type(array[i]) == list:
            array[i] = tuple(array[i])
