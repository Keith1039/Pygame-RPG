#!/usr/bin/python
from managers import SaveManager
from managers import ScreenManager
import pygame as game
from Entity.Knight import Knight
import sys
import json

game.init()

if __name__ == "__main__":
    arg = sys.argv[1]

    if arg == "fill-save":
        game.init()
        screen = game.display.set_mode((1422, 800))
        font = game.font.Font('font/Pixeltype.ttf', 50)
        screenManager = ScreenManager(screen)
        knight = Knight()
        saveManager = SaveManager(knight, vars(), screenManager)
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
            "Lvl": 1,
            "Str": 1,
            "Vit": 1,
            "Agl": 1,
            "Defence": 1,
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

