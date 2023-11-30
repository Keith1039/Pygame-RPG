#!/usr/bin/python
from managers import SaveManager
from managers import ScreenManager
import pygame as game
from Entity.Knight import Knight
import sys
import json

game.init()

if __name__ == "__main__":
    game.init()
    screen = game.display.set_mode((1422, 800))
    font = game.font.Font('font/Pixeltype.ttf', 50)
    arg = sys.argv[1]

    if arg == "fill-save":
        screenManager = ScreenManager(screen)
        knight = Knight()
        saveManager = SaveManager(knight, vars(), screenManager)
        for i in range(4):
            saveManager.save(i+1)

    if arg == "create-enemy":
        arg2 = sys.argv[2]  # There will a second argument with this
        path = "JSON/Enemies/" + arg2 + ".json"
        file = open(path, "w")  # Create the JSON file
        enemy_dict = {
            "Hp": 1,
            "Hpcap": 1,
            "Name": arg2,
            "Lvl": 1,
            "Str": 1,
            "Vit": 1,
            "Agl": 1,
            "Defence": 1,
            "Exp": 1,
            "Money": 1,
            "Inventory": {},
            "uniqueBuff": "",
            "Weakness": ""
        }
        json.dump(enemy_dict, file, indent=3)  # Dump the JSON info
        file.close()  # Close the file
    game.quit()
    exit()
