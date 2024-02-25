import os
import pygame as game
import random
from Entity.Knight import Knight
from managers.Save_Manager import SaveManager, tuplefy
from managers.Screen_Manager import ScreenManager
from managers.Screen_Manager import Event

def cleanup():
    os.system("bash script clear-save")

def fill_test_dict():
    test_dict.update({"animationTracker": animationTracker})
    test_dict.update({"animationTracker2": animationTracker2})
    test_dict.update({"animationTracker3": animationTracker3})
    test_dict.update({"dialogueTimer": dialogueTimer})
    test_dict.update({"gameState": gameState})
    test_dict.update({"x": x})

def fill_screenManager_dict():
    screenManager_dict.update({"context": screenManager.context})
    screenManager_dict.update({"objectDict": screenManager.objectDict})

def fill_event_dict():
    interactablesVars = {}
    for key in screenManager.interactablesDict:
        eventsVar = []
        eventsTuple = screenManager.interactablesDict[key]
        for i in range(len(eventsTuple)):
            eventsVar.append(vars(eventsTuple[i]))
        interactablesVars.update({key: tuple(eventsVar)})
    eventDict.update(interactablesVars)

def verify_interactables():
    flag = True
    mockJson = {"Range": (300, 400)}
    event = Event(mockJson)  # Just for init. These values mean nothing
    for key in screenManager.interactablesDict:
        i = 0
        dictVals = eventDict[key]
        while i < len(dictVals) and flag:
            event.load(dictVals[i])
            flag = event == screenManager.interactablesDict[key][i]
            i += 1
    return flag
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
screenManager_dict = {}
eventDict = {}
localVars = vars()
list = os.listdir("save/")
if len(list) != 0:
    cleanup()
saveManager = SaveManager(knight, localVars, screenManager)
knight2 = Knight()


animationTracker = random.randint(1, 100)
animationTracker2 = random.randint(1, 100)
animationTracker3 = random.randint(1, 100)
dialogueTimer = random.randint(1, 180)
gameState = random.randint(1, 5)
x = random.randint(-280, 1000)
screenManager.change_screen(1000)  # Move to right screen
for i in range(random.randint(1, 10)):
    knight.level_up()

def test_quick_save():
    fill_test_dict()
    fill_screenManager_dict()
    fill_event_dict()
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
    flag2 = (knight2 == knight)
    flag3 = (screenManager.context == screenManager_dict["context"] and screenManager.objectDict == tuplefy(screenManager_dict["objectDict"]))
    flag4 = verify_interactables()
    assert flag and flag2 and flag3 and flag4

animationTracker = random.randint(1, 99)   # cap at 99 because 100 breaks the game
animationTracker2 = random.randint(1, 99)
animationTracker3 = random.randint(1, 39)  # Changed to stop the possibility of crash when looking for chest ani
dialogueTimer = random.randint(1, 180)
gameState = random.randint(1, 5)
for i in range(random.randint(1, 10)):
    knight.level_up()
screenManager.change_screen(-280)  # Moves back to initial screen
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
        flag = (knight2 == knight)
    if flag:
        flag = (screenManager.context == screenManager_dict["context"] and screenManager.objectDict == screenManager_dict["objectDict"])
    if flag:
        flag = verify_interactables()
    assert flag

def test_latest_file():  # check if last save is 4
    newManager = SaveManager(Knight, vars(), screenManager)
    #cleanup()  # Gets rid of the save files created in the test
    assert newManager.saveNumber == 4  # Should still be 4

