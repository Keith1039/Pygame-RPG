import os.path
import json
import managers.Save_Manager
import managers.UI_Manager
from Entity import Move

# Class that handles the UI inputs
submenu_choice = ["Skills", "Switch Stance", "Items"]
stances = ["Power", "Defensive", "Nimble"]
items = list(json.load(open("JSON/Items/Items.json")).keys())

jsonInfo = json.load(open("JSON/Dictionaries/UIHandler.json"))
# For UIManager
ui_related_context = jsonInfo.get("ui_related_context")  # Pages who's options go to another UI
screen_flow_dict = jsonInfo.get("screen_flow_dict")

# For SaveManager
save_related_context = jsonInfo.get("save_related_context")

# for Knight
knight_related_context = jsonInfo.get("knight_related_context")

# for localVars
vars_related_context = jsonInfo.get("vars_related_context")

# for Battle related context
battle_related_context = jsonInfo.get("battle_related_context")
class UIHandler():
    # The things UIHandler will need access to for user input
    def __init__(self, uiManager, SaveManager, knight, localVars, battleManager, itemManager):
        # Dialogue Manager might have to be here too
        self.uiManager = uiManager  # For changing the UI
        self.saveManager = SaveManager  # For saving and loading on UI
        self.knight = knight  # For access to inventory as well as battle interaction
        self.localVars = localVars  # For manipulating variables from player interaction
        # Local vars exists in SaveManager, might just reference that one instead
        self.battleManager = battleManager  # For passing the manager player choice and target
        self.itemManager = itemManager  # for managing items
    # Main function of the class
    # Takes in the context and the choice that was made and process it
    def handle_interaction(self, context, choice):
        # submenu for battle
        if context == "Player Select" and choice in submenu_choice:
            self.uiManager.subMenu = True
            if choice == "Skills":
                # Get all the skills except for the first one ("Attack")
                self.uiManager.subMenuItems = self.knight.moveList[1:]
            elif choice == "Switch Stance":
                self.uiManager.subMenuItems = ["Power", "Defensive", "Nimble",
                                                "Power", "Defensive", "Nimble",
                                                "Power", "Defensive", "Nimble",
                                                "Power"]

            elif choice == "Items":
                inventory = self.itemManager.get_usable_items()
                self.uiManager.subMenuItems = inventory

        elif context is not None and choice is not None:
            #print(context)
            #print(choice)
            #print("..........................................")
            if [context, choice] in ui_related_context:
                self.uiManager.change_UI(choice)  # Just change to the new UI

            elif context.find("(S)") != -1 or choice == "Attack":
                if choice in stances:
                    # switch Knight stance and apply the buff
                    pass
                elif choice in items:
                    # get the info from the items dict
                    # see if it's usable on enemies or yourself
                    # if it's usable on enemies go to targeting
                    # if it's usable on enemies AND yourself go to targeting but add knights pos to the list
                    # if the item is only usable on yourself, use it and be done with your turn
                    target = self.itemManager.get_effect_details(choice)["Target"]
                    targetable = []
                    if target == "S":
                        # add the hero to the list of targets
                        targetable.append(self.battleManager.heroPos)
                    elif target == "All":
                        # add everything into the list of targets
                        targetable = self.battleManager.get_enemy_positions()
                        targetable.insert(0, self.battleManager.heroPos)
                    else:
                        # add enemies to the list of targets
                        targetable = self.battleManager.get_enemy_positions()
                    self.uiManager.targets = targetable
                    self.uiManager.targetSlider = 0
                    self.uiManager.change_UI("Select Target")


                # this is an attack of some sort
                else:
                    moveInfo = self.battleManager.moveDict[choice]
                    # Only go to targeting if the move can be used, if not the move cannot be selected
                    if self.battleManager.parse_restriction(self.knight, moveInfo) \
                            and self.knight.Mp >= moveInfo["Cost"]:
                        self.uiManager.targets = self.battleManager.get_enemy_positions()
                        self.uiManager.targetSlider = 0
                        self.uiManager.change_UI("Select Target")

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
                        self.uiManager.change_UI(None)  # Clear UI
                # self.saveManager
                pass
            elif context in knight_related_context:
                #self.knight
                pass
            elif context in battle_related_context:
                #self.battleManager
                pass
            elif [context, choice] in vars_related_context:  # For now
                # There's got to be a better way of dealing with this
                if context == "Start" and choice == "Start Game":
                    self.localVars.update({"start": False})
                    self.uiManager.change_UI(None)  # Clear UI
                elif context == "Start" and choice == "Continue":
                    slot = self.saveManager.saveNumber
                    # Implement a check to see if save has been tampered with for all save file loads
                    flag = os.path.getsize("save/save_data" + str(slot) + ".json") > 0
                    if flag:
                        self.saveManager.quick_load()  # Load the file
                        self.localVars.update({"start": False})  # Leave the Start screen
                        self.uiManager.change_UI(None)  # Clear UI
                    pass
