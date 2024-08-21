import json

def get_json_from_file_path(filePath):
    file = open(filePath, "r")
    jsonInfo = json.load(file)
    file.close()
    return jsonInfo

def get_quest_dict():
    return get_json_from_file_path("JSON/Quests/Quests.json")

def get_move_dict():
    return get_json_from_file_path("JSON/Moves/Complete_Move_List.json")

def get_status_dict():
    return get_json_from_file_path("JSON/Status/Status.json")

def get_NPC_dict():
    return get_json_from_file_path("JSON/NPCs/NPCs.json")

def get_event_dict():
    return get_json_from_file_path("JSON/Events/Events.json")


def get_item_dict():
    return get_json_from_file_path("JSON/Items/Items.json")

def get_item_effect_dict():
    return get_json_from_file_path("JSON/Items/Item_Effects.json")

def get_item_fusion_dict():
    return get_json_from_file_path("JSON/Items/Item_Fusion.json")

def get_equipment_dict():
    return get_json_from_file_path("JSON/Items/Equipment.json")


