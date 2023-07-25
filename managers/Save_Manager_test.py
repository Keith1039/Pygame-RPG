import os
import pygame as game
import random

from managers.Dummy_Knight import Knight
from managers.Save_Manager import SaveManager
from managers.Screen_Manager import ScreenManager

# Replicating an actual game
game.init()
screen = game.display.set_mode((1422, 800))
screenManager = ScreenManager(screen)
knight = Knight()
animationTracker = 0
animationTracker2 = 0
animationTracker3 = 0
dialogueTimer = 0
gameState = 0 
x = 500

test_dict = {}
knight_dict = {}
screenManager_dict = {}
localVars = vars()
saveManager = SaveManager(knight, localVars)
Knight2 = Knight()
def fill_test_dict():
    test_dict.update({"animationTracker": animationTracker})
    test_dict.update({"animationTracker2": animationTracker2})
    test_dict.update({"animationTracker3": animationTracker3})
    test_dict.update({"dialogueTimer": dialogueTimer})
    test_dict.update({"gameState": gameState})
    test_dict.update({"x": x})

def fill_knight_dict():
    knight_dict.update({"Hp": knight.Hp})
    knight_dict.update({"Hpcap": knight.Hpcap})
    knight_dict.update({"Name": knight.Name})
    knight_dict.update({"Lvl": knight.Lvl})
    knight_dict.update({"Str": knight.Str})
    knight_dict.update({"Vit": knight.Vit})
    knight_dict.update({"Agl": knight.Agl})
    knight_dict.update({"Status": knight.Status})
    knight_dict.update({"Stance": knight.Stance})
    knight_dict.update({"Defence": knight.Defence})
    knight_dict.update({"Exp": knight.Exp})
    knight_dict.update({"Expcap": knight.Expcap})
    knight_dict.update({"Bal": knight.Bal})

def fill_screenManager_dict():
    screenManager_dict.update({"context": screenManager.context})
    screenManager_dict.update({"objectDict": screenManager.objectDict})
animationTracker = random.randint(1, 100)
animationTracker2 = random.randint(1, 100)
animationTracker3 = random.randint(1, 100)
dialogueTimer = random.randint(1, 180)
gameState = random.randint(1, 5)
x = random.randint(-280, 1000)
screenManager.change_screen(1000)  # Move to right screen
for i in range(random.randint(1, 10)):
    knight.levelup()
def test_quick_save():
    fill_knight_dict()
    fill_test_dict()
    fill_screenManager_dict()
    saveManager.quick_save(screenManager)
    assert saveManager.saveNumber == 0  # Shouldn't change

def test_quick_load():
    Knight2.load_dict(knight_dict)
    saveManager.quick_load(screenManager)
    flag = True
    for key in test_dict:
        if localVars[key] != test_dict[key]:
            flag = False
            break
    if flag:
        flag = (Knight2 == knight)
    if flag:
        flag = (screenManager.context == screenManager_dict["context"] and screenManager.objectDict == screenManager_dict["objectDict"])
    assert flag

animationTracker = random.randint(1, 100)
animationTracker2 = random.randint(1, 100)
animationTracker3 = random.randint(1, 100)
dialogueTimer = random.randint(1, 180)
gameState = random.randint(1, 5)
for i in range(random.randint(1, 10)):
    knight.levelup()
screenManager.change_screen(-280)  # Moves back to initial screen
def test_save(): #slot #4
    fill_knight_dict()
    fill_test_dict()
    fill_screenManager_dict()
    saveManager.save(4, screenManager)
    assert saveManager.saveNumber == 4  # Should now be 4

def test_load():  # slot #4
    Knight2.load_dict(knight_dict)
    saveManager.load(4, screenManager)
    flag = True
    for key in test_dict:
        if localVars[key] != test_dict[key]:
            flag = False
            break
    if flag:
        flag = (Knight2 == knight)
    if flag:
        flag = (screenManager.context == screenManager_dict["context"] and screenManager.objectDict == screenManager_dict["objectDict"])
    assert flag

def test_latest_file():  # check if last save is 4
    newManager = SaveManager(Knight, vars())
    cleanup() # Gets rid of the save files created in the test
    assert newManager.saveNumber == 4  # Should still be 4

def cleanup():
    os.system("bash script save-test")
