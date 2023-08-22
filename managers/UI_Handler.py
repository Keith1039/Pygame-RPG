import os.path

import managers.Save_Manager
import managers.UI_Manager

# Class that handles the UI inputs

# For UIManager
ui_related_context = [("Start", "Load Game")]  # Pages who's options go to another UI
screen_flow_dict = {}

# For SaveManager
save_related_context = ["Save Game", "Load Game"]

# for Knight
knight_related_context = []

# for localVars
vars_related_context = [("Start", "Start Game"), ("Start", "Continue")]

# Battle related context
battle_related_context = []
class UIHandler():
    # The things UIHandler will need access to for user input
    def __init__(self, UIManager, SaveManager, knight, localVars, battleManager=None):
        # Dialogue Manager might have to be here too
        self.UIManager = UIManager  # For changing the UI
        self.saveManager = SaveManager  # For saving and loading on UI
        self.knight = knight  # For access to inventory as well as battle interaction
        self.localVars = localVars  # For manipulating variables from player interaction
        # Local vars exists in SaveManager, might just reference that one instead
        self.battleManager = battleManager  # For passing the manager player choice and target
    # Main function of the class
    # Takes in the context and the choice that was made and process it
    def handle_interaction(self, context, choice):
        if context is not None and choice is not None:
            #print(context)
            #print(choice)
            #print("..........................................")
            if (context, choice) in ui_related_context:
                self.UIManager.change_UI(choice)  # Just change to the new UI
                pass

            elif context in save_related_context:
                slot = choice.find("#")       # Finds the # character because the number is always next to it
                slot = int(choice[slot + 1])  # Finds the slot that the user chose
                if context == "Save Game":
                    self.saveManager.save(slot)
                else:
                    filePath = "save/save_data" + str(slot) + ".json"
                    if os.path.isfile(filePath):
                        self.saveManager.load(slot)
                        self.localVars.update({"start": False})  # Leave the Start screen (probably a better way for this)
                        self.UIManager.change_UI(None)  # Clear UI
                # self.saveManager
                pass
            elif context in knight_related_context:
                #self.knight
                pass
            elif context in battle_related_context:
                #self.battleManager
                pass
            elif (context, choice) in vars_related_context:  # For now
                # There's got to be a better way of dealing with this
                if context == "Start" and choice == "Start Game":
                    self.localVars.update({"start": False})
                    self.UIManager.change_UI(None)  # Clear UI
                elif context == "Start" and choice == "Continue":
                    slot = self.saveManager.saveNumber
                    # Implement a check to see if save has been tampered with for all save file loads
                    flag = os.path.getsize("Save/save_data" + str(slot) + ".json") > 0
                    if flag:
                        self.saveManager.quick_load()  # Load the file
                        self.localVars.update({"start": False})  # Leave the Start screen
                        self.UIManager.change_UI(None)  # Clear UI
                    pass
