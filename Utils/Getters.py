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

def get_object_def_dict():
    return get_json_from_file_path("JSON/Objects/Object_def.json")

def get_object_dict():
    return get_json_from_file_path("JSON/Objects/Objects.json")

def get_complete_object_dict():
    completeDict = {}
    objectDict = get_object_dict()
    objectDefDict = get_object_def_dict()
    for key, jsonInfo in objectDict.items():
        objectDefInfo = objectDefDict[jsonInfo["Object Type"]]
        jsonInfo.update(objectDefInfo)
        jsonInfo.update({
            "aniStatus": "Idle",
            "aniTracker": 0
        })
        completeDict.update({key: jsonInfo})
    return completeDict

# this function returns the event dictionary with only the priority and if the event is repeatable
def get_cut_event_info():
    completeDict = {}
    eventDict = get_event_dict()  # the event dictionary
    for key, dictionary in eventDict.items():
        completeDict.update({key: {  # we only want the priority and if the event is repeatable
            "Priority": dictionary["Priority"],
            "Repeatable": dictionary["Repeatable"]
        }})
    return completeDict




