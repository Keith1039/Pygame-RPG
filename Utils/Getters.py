import json

def get_quest_dict():
    file = open("JSON/Quests/Quests.json", "r")
    questDict = json.load(file)
    file.close()
    return questDict

def get_move_dict():
    # Loads the move dictionary from a file
    file = open("JSON/Moves/Complete_Move_List.json", "r")
    jsonInfo = json.load(file)
    file.close()
    return jsonInfo

def get_status_dict():
    # loads the status dictionary from a file
    file = open("JSON/Status/Status.json", "r")
    jsonInfo = json.load(file)
    file.close()
    return jsonInfo

def get_NPC_dict():
    file = open("JSON/NPCs/NPCs.json", "r")  # open the file
    jsonInfo = json.load(file)  # load the file
    file.close()  # close the file
    return jsonInfo  # return JSON dict

def get_event_dict():
    file = open("JSON/Events/Events.json", "r")
    jsonInfo = json.load(file)
    file.close()
    return jsonInfo

def get_item_dict():
    file = open("JSON/Items/Items.json")
    jsonInfo = json.load(file)
    file.close()
    return jsonInfo

def get_item_effect_dict():
    file = open("JSON/Items/Item_Effects.json")
    jsonInfo = json.load(file)
    file.close()
    return jsonInfo

def get_item_fusion_dict():
    file = open("JSON/Items/Item_Fusion.json")
    jsonInfo = json.load(file)
    file.close()
    return jsonInfo

def get_equipment_dict():
    file = open("JSON/Items/Equipment.json")
    jsonInfo = json.load(file)
    file.close()
    return jsonInfo

