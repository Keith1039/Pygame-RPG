import os.path
import json
import managers.Save_Manager
import managers.UI_Manager
from Entity import Move
from managers.Submenu import Submenu

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
        self.UIStack = [self.uiManager]
        self.tempStack = []
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
            if choice == "Skills":
                # Get all the skills except for the first one ("Attack")
                # and add it to the new submenu
                self.UIStack.append(Submenu(self.uiManager.UI, self.uiManager.screen, self.knight.moveList[1:]))
                # self.uiManager.subMenuItems = self.knight.moveList[1:]
            elif choice == "Switch Stance":
                stanceList = ["Power", "Defensive", "Nimble",
                                "Power", "Defensive", "Nimble",
                                "Power", "Defensive", "Nimble",
                                "Power"]
                self.UIStack.append(Submenu(self.uiManager.UI, self.uiManager.screen, stanceList))

            elif choice == "Items":
                inventory = self.itemManager.get_usable_items()
                self.UIStack.append(Submenu(self.uiManager.UI, self.uiManager.screen, inventory))
                # self.uiManager.subMenuItems = inventory
        elif context is not None and choice is None:
            if context.find("(S)") != -1:
                self.UIStack.pop(-1)  # remove the submenu from the stack
            else:
                if len(self.tempStack) > 0:
                    self.UIStack.append(self.tempStack.pop())

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
                    targets = []
                    if target == "S":
                        # add the hero to the list of targets
                        targetable.append([self.battleManager.get_adjusted_knight_pos()])
                        targets = [self.battleManager.get_knight_pos()]
                    elif target == "All":
                        # target matrix
                        targetable = self.battleManager.get_enemy_pos_matrix()
                        targetable.insert(0, [self.battleManager.get_adjusted_knight_pos()])
                        # target information
                        targets = [self.battleManager.get_knight_pos()] + self.battleManager.get_enemy_positions()
                    else:
                        # add enemies to the list of targets
                        targetable = self.battleManager.get_enemy_pos_matrix()
                        targets = self.battleManager.get_enemy_positions()
                    self.uiManager.targets = targets
                    self.uiManager.cursor.set_new_positions(targetable)
                    self.tempStack.append(self.UIStack.pop(-1))  # add it to the temp stack
                    self.uiManager.change_UI("Select Target")
                # check if it's an attack of some sort
                elif self.battleManager.moveDict.get(choice) is not None:
                    moveInfo = self.battleManager.moveDict[choice]
                    # Only go to targeting if the move can be used, if not the move cannot be selected
                    if self.battleManager.parse_restriction(self.knight, moveInfo) \
                            and self.knight.Mp >= moveInfo["Cost"]:
                        self.uiManager.targets = self.battleManager.get_enemy_positions()
                        self.uiManager.cursor.set_new_positions(self.battleManager.get_enemy_pos_matrix())
                        if choice != "Attack":
                            self.tempStack.append(self.UIStack.pop(-1))  # add it to the temp stack
                        self.uiManager.change_UI("Select Target")
                #print(self.uiManager.targets)

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
