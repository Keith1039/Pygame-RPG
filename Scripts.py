#!/usr/bin/python
from managers import SaveManager
from managers import ScreenManager
from managers import DialogueManager
from managers import EventManager
from managers import QuestManager
from Entity.NPC_Manager import NPCManager
import pygame as game
from Entity.Knight import Knight
import sys
import json
import os
import Utils

if __name__ == "__main__":
    arg = sys.argv[1]

    if arg == "fill-save":
        game.init()
        screen = game.display.set_mode((1422, 800))
        font = game.font.Font('font/Pixeltype.ttf', 50)
        screenManager = ScreenManager(screen)
        knight = Knight()
        dialogueManager = DialogueManager(font, screen)
        questManager = QuestManager(knight)
        eventManager = EventManager(knight, dialogueManager, questManager)
        npcManager = NPCManager(knight)
        saveManager = SaveManager(knight, vars(), screenManager, eventManager, questManager, knight)
        for i in range(4):
            saveManager.save(i+1)
        game.quit()
        exit()

    elif arg == "create-enemy":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Enemies/" + arg2 + ".json"
        file = open(path, "w")  # Create the JSON file
        enemy_dict = {
            "Hp": 1,
            "Hpcap": 1,
            "Mp": 1,
            "Mpcap": 1,
            "Name": arg2,
            "Sprite": "Entity_Sprites/",
            "Lvl": 1,
            "Str": 1,
            "Mag": 1,
            "Vit": 1,
            "Agl": 1,
            "Def": 1,
            "Exp": 1,
            "Money": 1,
            "Inventory": {},
            "moveList": ["Attack"],
            "uniqueBuff": "",
            "Weakness": ""
        }
        json.dump(enemy_dict, file, indent=3)  # Dump the JSON info
        file.close()  # Close the file

    elif arg == "create-move":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Moves/Complete_Move_List.json"
        moveDict = Utils.get_move_dict()
        file = open(path, "w")
        moveDict.update({
            arg2: {
                "Damage Calculation": "",
                "Type": "",
                "Cost": 0,
                "Restriction": None,
                "Effect": None,
                "AOE": False,
                "Target Number": 1,
                "Probability": None,
                "Weight": 100,
                "Description": ""
            }
        })
        json.dump(moveDict, file, indent=3)
        file.close()

    elif arg == "create-item":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Items/Items.json"
        itemDict = Utils.get_item_dict()
        file = open(path, "w")
        itemDict.update({
            arg2: {
                "Type": "Consumable",
                "Effect": False,
                "Purchasable": False,
                "Fusion": False,
                "Limited": False,
                "Buy": 0,
                "Sell": 0,
                "Description": ""
            }
        })
        json.dump(itemDict, file, indent=3)
        file.close()

    elif arg == "create-effects":
        path = "JSON/Items/Item_Effects.json"
        itemDict = Utils.get_item_dict()
        itemEffectDict = Utils.get_item_effect_dict()
        file = open(path, "w")
        for item, itemInfo in itemDict.items():
            if itemInfo["Effect"] and itemEffectDict.get(item) is None:
                itemEffectDict.update({
                    item: {
                        "Target": "",
                        "Effect": ""
                    }
                })
        json.dump(itemEffectDict, file, indent=3)
        file.close()

    elif arg == "create-equipment":
        path = "JSON/Items/Equipment.json"
        itemDict = Utils.get_item_dict()
        equipmentDict = Utils.get_equipment_dict()
        file = open(path, "w")
        for item, itemInfo in itemDict.items():
            if itemInfo["Type"] == "Equipment" and equipmentDict.get(item) is None:
                equipmentDict.update({
                    item: {
                        "Attribute": None,
                        "Type": "",
                        "Hpcap": 0,
                        "Mpcap": 0,
                        "Str": 0,
                        "Mag": 0,
                        "Agl": 0,
                        "Def": 0,
                        "Movelist": []
                    }
                })
        json.dump(equipmentDict, file, indent=3)
        file.close()

    elif arg == "create-fusions":
        path = "JSON/Items/Item_Fusion.json"
        itemDict = Utils.get_item_dict()
        fusionDict = Utils.get_item_fusion_dict()
        file = open(path, "w")
        for item, itemInfo in itemDict.items():
            if fusionDict.get(item) is None and itemInfo["Fusion"]:
                fusionDict.update({item: [[""], [""]]})
        json.dump(fusionDict, file, indent=3)
        file.close()

    elif arg == "validate-fusions":
        itemDict = Utils.get_item_dict()
        fusionsDict = Utils.get_item_fusion_dict()
        wrongKeys = []
        wrongMaterials = []
        wrongMaterialsPair = {}

        for item, fusionItems in fusionsDict.items():
            if itemDict.get(item) is None:
                wrongKeys.append(item)  # this item doesn't exist in the items dict
            else:
                materialsA = fusionItems[0]
                materialsB = fusionItems[1]
                for i in range(len(materialsA)):
                    material = materialsA[i]
                    if itemDict.get(material) is None:
                        wrongMaterials.append(material)
                for i in range(len(materialsB)):
                    material = materialsB[i]
                    if itemDict.get(material) is None:
                        wrongMaterials.append(material)
                if len(wrongMaterials) != 0:
                    wrongMaterialsPair.update({item: tuple(wrongMaterials)})
                wrongMaterials.clear()  # clear out the list
        print(wrongMaterialsPair)

    elif arg == "update-saves":
        knight = Knight()
        saveFiles = os.listdir("save/")
        os.chdir("save/")
        for i in range(len(saveFiles)):
            fileName = saveFiles[i]
            if fileName.find("save_data") != -1:
                file = open(fileName, "r")
                saveData = json.load(file)
                file.close()
                file = open(fileName, "w")
                saveData.update({"Knight": vars(knight)})  # update the variables
                json.dump(saveData, file, indent=3)
                file.close()
        os.chdir("../")

    elif arg == "fix-item-effects":
        path = "JSON/Items/Item_Effects.json"
        itemEffectsDict = Utils.get_item_effect_dict()
        for item, effect in itemEffectsDict.items():
            templateDict = {
                "Target": "",
                "AOE": False,
                "Effect": effect
            }
            itemEffectsDict.update({item: templateDict})
        file = open(path, "w")
        json.dump(itemEffectsDict, file, indent=3)
        file.close()

    elif arg == "add-status":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Status/Status.json"
        statusDict = Utils.get_status_dict()
        statusDict.update({
                arg2: {
                    "maxCount": 0,
                    "Effect": "",
                    "Description": ""
                }
            })
        file = open(path, "w")
        json.dump(statusDict, file, indent=3)
        file.close()

    elif arg == "add-event":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Events/Events.json"
        eventDict = Utils.get_event_dict()
        eventDict.update({
            arg2: {
                "Range": [],
                "Event Type": "",
                "Activated": False,
                "Repeatable": False,
                "Dialogue Path": "",
                "Quest": "",
                "Context": "",
                "Items Gained": {

                }
            }
        })
        file = open(path, "w")
        json.dump(eventDict, file, indent=3)
        file.close()

    elif arg == "add-quest":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Quests/Quests.json"
        questDict = Utils.get_quest_dict()
        questDict.update({
            arg2: {
                "Quest Type": "",
                "Next Quest": "",
                "Target": {

                },
                "Context": "",
                "Range": [],
                "Reward": {
                    "Exp": 0,
                    "Money": 0,
                    "Items": {

                    }
                },
                "Description": ""
            }
        })
        file = open(path, "w")
        json.dump(questDict, file, indent=3)
        file.close()

    elif arg == "add-NPC":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/NPCs/NPCs.json"
        npcDict = Utils.get_NPC_dict()
        npcDict.update({
            arg2: {
                "Name": arg2,
                "Sprite": "Object_Sprites/" + arg2 + "/",
                "Scale": [],
                "Dialogue": [],
                "Context": "",
                "Pos": []
            }
        })
        file = open(path, "w")
        json.dump(npcDict, file, indent=3)
        file.close()

    elif arg == "add-object":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Objects/Objects.json"
        npcDict = Utils.get_object_dict()
        npcDict.update({
            arg2: {
                "Name": arg2,
                "Object Type": "",
                "Flipped": False,
                "Context": "",
                "Pos": [],
                "Events": []
            }
        })
        file = open(path, "w")
        json.dump(npcDict, file, indent=3)
        file.close()

    elif arg == "add-object-def":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Objects/Object_def.json"
        npcDict = Utils.get_object_def_dict()
        npcDict.update({
            arg2: {
                "Sprite": "NPC_Sprites/" + arg2 + "/",
                "Scale": []
            }
        })
        file = open(path, "w")
        json.dump(npcDict, file, indent=3)
        file.close()
