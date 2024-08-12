import os
import json
import pygame as game
import random
from Entity.Knight import Knight
from managers.Save_Manager import SaveManager, tuplefy, tuplefy2
from managers.Screen_Manager import ScreenManager
from managers.Dialogue_Manager import DialogueManager
from managers.Event_Manager import EventManager
from managers.Quest_Manager import QuestManager
def cleanup():
    os.system("bash script clear-save")

def fill_test_dict():
    test_dict.update({"animationTracker": animationTracker})
    test_dict.update({"animationTracker2": animationTracker2})
    test_dict.update({"animationTracker3": animationTracker3})
    test_dict.update({"dialogueTimer": dialogueTimer})
    test_dict.update({"gameState": gameState})

def fill_screenManager_dict():
    screenManager_dict.update({"context": screenManager.context})
    screenManager_dict.update({"objectDict": screenManager.objectDict})

def fill_event_dict():
    for key, value in screenManager.interactablesDict.items():
        eventDict.update({key: value})


def verify_interactables():
    return tuplefy2(eventDict) == screenManager.interactablesDict
# Replicating an actual game
game.init()
screen = game.display.set_mode((1422, 800))
font = game.font.Font('font/Pixeltype.ttf', 50)
screenManager = ScreenManager(screen)
knight = Knight()
animationTracker = 0
animationTracker2 = 0
animationTracker3 = 0
dialogueTimer = 0
gameState = 0 

min_x = -280
max_x = 1000

test_dict = {}
screenManager_dict = {}
eventDict = {}
localVars = vars()
list = os.listdir("save/")
if len(list) != 0:
    cleanup()

knight2 = Knight()
dialogeManager = DialogueManager(font, screen)
questmanager = QuestManager(knight)
eventManager = EventManager(knight, dialogeManager, questmanager)
saveManager = SaveManager(knight, localVars, screenManager, eventManager, questmanager)
animationTracker = random.randint(1, 100)
animationTracker2 = random.randint(1, 100)
animationTracker3 = random.randint(1, 100)
dialogueTimer = random.randint(1, 180)
gameState = random.randint(1, 5)

screenManager.change_screen(min_x, max_x, 1000)  # Move to right screen
for i in range(random.randint(1, 10)):
    knight.level_up()

def test_quick_save():
    fill_test_dict()
    fill_screenManager_dict()
    fill_event_dict()
    saveManager.eventManager.eventDict["mockDialogue2"]["Activated"] = True  # set this to true
    # change some values to compare with later
    saveManager.questManager.enemiesKilled.update({"Goblin": 1})
    saveManager.questManager.npcsInteractedWith.update({"Lucy": 1})
    saveManager.questManager.add_quest("testQuest")
    saveManager.quick_save()
    knight2.load_dict(knight.__dict__.copy())  # taking the values of the previous knight right after they were saved
    assert saveManager.saveNumber == 1  # Shouldn't change

def test_quick_load():
    saveManager.quick_load()
    flag = True
    for key in test_dict:
        if localVars[key] != test_dict[key]:
            flag = False
            break
    print(knight2.__dict__)
    print(knight.__dict__)
    flag2 = (knight2.equals(knight))
    flag3 = (screenManager.context == screenManager_dict["context"] and screenManager.objectDict == tuplefy(screenManager_dict["objectDict"]))
    flag4 = verify_interactables()
    flag5 = saveManager.eventManager.eventDict["mockDialogue2"]["Activated"]
    # check the values for quest manager and see if they have been updated
    flag6 = len(saveManager.questManager.activeQuests) == 1 and \
        saveManager.questManager.enemiesKilled.get("Goblin") is not None and \
        saveManager.questManager.npcsInteractedWith.get("Lucy") is not None
    assert flag and flag2 and flag3 and flag4 and flag5 and flag6

animationTracker = random.randint(1, 99)   # cap at 99 because 100 breaks the game
animationTracker2 = random.randint(1, 99)
animationTracker3 = random.randint(1, 39)  # Changed to stop the possibility of crash when looking for chest ani
dialogueTimer = random.randint(1, 180)
gameState = random.randint(1, 5)
for i in range(random.randint(1, 10)):
    knight.level_up()
screenManager.change_screen(min_x, max_x, -280)  # Moves back to initial screen
def test_save(): #slot #4
    fill_test_dict()
    fill_screenManager_dict()
    fill_event_dict()
    saveManager.save(4)
    knight2.load_dict(knight.__dict__.copy())  # taking the values of the previous knight before the values are loaded
    assert saveManager.saveNumber == 4  # Should now be 4

def test_load():  # slot #4
    saveManager.load(4)
    flag = True
    for key in test_dict:
        if localVars[key] != test_dict[key]:
            flag = False
            break
    if flag:
        flag = (knight2.equals(knight))
    if flag:
        flag = (screenManager.context == screenManager_dict["context"] and screenManager.objectDict == screenManager_dict["objectDict"])
    if flag:
        flag = verify_interactables()
    assert flag

def test_latest_file():  # check if last save is 4
    newManager = SaveManager(Knight, vars(), screenManager, eventManager, questmanager)
    #cleanup()  # Gets rid of the save files created in the test
    assert newManager.saveNumber == 4  # Should still be 4

