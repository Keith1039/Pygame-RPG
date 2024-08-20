#!/usr/bin/python
from managers import SaveManager
from managers import ScreenManager
from managers import DialogueManager
from managers import EventManager
from managers import QuestManager
import pygame as game
from Entity.Knight import Knight
import sys
import json
import os

if __name__ == "__main__":
    arg = sys.argv[1]

    if arg == "fill-save":
        game.init()
        screen = game.display.set_mode((1422, 800))
        font = game.font.Font('font/Pixeltype.ttf', 50)
        screenManager = ScreenManager(screen)
        knight = Knight()
        dialogueManager = DialogueManager(font, screen)
        eventManager = EventManager(knight, dialogueManager)
        questManager = QuestManager(knight)
        saveManager = SaveManager(knight, vars(), screenManager, eventManager, questManager)
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
        file = open(path, "r")
        jsonInfo = json.load(file)
        file.close()
        file = open(path, "w")
        jsonInfo.update({
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
        json.dump(jsonInfo, file, indent=3)
        file.close()

    elif arg == "create-item":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Items/Items.json"
        file = open(path, "r")
        jsonInfo = json.load(file)
        file.close()
        file = open(path, "w")
        jsonInfo.update({
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
        json.dump(jsonInfo, file, indent=3)
        file.close()

    elif arg == "create-effects":
        path = "JSON/Items/Items.json"
        path2 = "JSON/Items/Item_Effects.json"
        file = open(path, "r")
        file2 = open(path2, "r")
        jsonInfo = json.load(file)
        newJsonInfo = json.load(file2)
        file.close()
        file2.close()
        file = open(path2, "w")
        for item, itemInfo in jsonInfo.items():
            if itemInfo["Effect"] and newJsonInfo.get(item) is None:
                newJsonInfo.update({
                    item: {
                        "Target": "",
                        "Effect": ""
                    }
                })
        json.dump(newJsonInfo, file, indent=3)
        file.close()

    elif arg == "create-equipment":
        path = "JSON/Items/Items.json"
        path2 = "JSON/Items/Equipment.json"
        file = open(path, "r")
        file2 = open(path2, "r")
        jsonInfo = json.load(file)
        newJsonInfo = json.load(file2)
        file.close()
        file2.close()
        file = open(path2, "w")
        for item, itemInfo in jsonInfo.items():
            if itemInfo["Type"] == "Equipment" and newJsonInfo.get(item) is None:
                newJsonInfo.update({
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
        json.dump(newJsonInfo, file, indent=3)
        file.close()

    elif arg == "create-fusions":
        path = "JSON/Items/Items.json"
        path2 = "JSON/Items/Item_Fusion.json"
        file = open(path, "r")
        file2 = open(path2, "r")
        jsonInfo = json.load(file)
        fusionJson = json.load(file2)
        file.close()
        file2.close()
        file = open(path2, "w")
        for item, itemInfo in jsonInfo.items():
            if fusionJson.get(item) is None and itemInfo["Fusion"]:
                fusionJson.update({item: [[""], [""]]})
        json.dump(fusionJson, file, indent=3)
        file.close()

    elif arg == "validate-fusions":
        path = "JSON/Items/Items.json"
        path2 = "JSON/Items/Item_Fusion.json"
        file = open(path, "r")
        file2 = open(path2, "r")
        jsonInfo = json.load(file)
        fusionJson = json.load(file2)
        file.close()
        file2.close()
        wrongKeys = []
        wrongMaterials = []
        wrongMaterialsPair = {}

        for item, fusionItems in fusionJson.items():
            if jsonInfo.get(item) is None:
                wrongKeys.append(item)  # this item doesn't exist in the items dict
            else:
                materialsA = fusionItems[0]
                materialsB = fusionItems[1]
                for i in range(len(materialsA)):
                    material = materialsA[i]
                    if jsonInfo.get(material) is None:
                        wrongMaterials.append(material)
                for i in range(len(materialsB)):
                    material = materialsB[i]
                    if jsonInfo.get(material) is None:
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
        file = open(path, "r")
        effectJson = json.load(file)
        file.close()
        for item, effect in effectJson.items():
            templateDict = {
                "Target": "",
                "AOE": False,
                "Effect": effect
            }
            effectJson.update({item: templateDict})
        file = open(path, "w")
        json.dump(effectJson, file, indent=3)
        file.close()

    elif arg == "add-status":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Status/Status.json"
        file = open(path, "r")
        statusJSON = json.load(file)
        file.close()
        statusJSON.update({
                arg2: {
                    "maxCount": 0,
                    "Effect": "",
                    "Description": ""
                }
            })
        file = open(path, "w")
        json.dump(statusJSON, file, indent=3)
        file.close()

    elif arg == "add-event":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Events/Events.json"
        file = open(path, "r")
        statusJSON = json.load(file)
        file.close()
        statusJSON.update({
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
        json.dump(statusJSON, file, indent=3)
        file.close()

    elif arg == "add-quest":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Quests/Quests.json"
        file = open(path, "r")
        statusJSON = json.load(file)
        file.close()
        statusJSON.update({
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
        json.dump(statusJSON, file, indent=3)
        file.close()

    elif arg == "add-NPC":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/NPCs/NPCs.json"
        file = open(path, "r")
        statusJSON = json.load(file)
        file.close()
        statusJSON.update({
            arg2: {
                "Name": arg2,
                "Sprite": "NPC_Sprites/" + arg2 + "/",
                "Scale": [],
                "Dialogue": [],
                "Context": "",
                "Pos": []
            }
        })
        file = open(path, "w")
        json.dump(statusJSON, file, indent=3)
        file.close()

        #add - NPC


