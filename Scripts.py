#!/usr/bin/python
import os

from managers import SaveManager
from managers import ScreenManager
from managers import UIManager
import pygame as game
import json
from Knight import Knight
import sys
import keyboard

keys_dict = {"s": game.K_s, "w": game.K_w, "a": game.K_a, "d": game.K_d, "enter": game.K_RETURN, "esc": game.K_ESCAPE}
def ensure_pressed(key):
    while True:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                exit()
        keys = game.key.get_pressed()
        keyboard.press(key)
        if keys[keys_dict.get(key)]:
            return keys
    
def ui_test_1(uiManager, result_dict):
    # move cursor down twice and test if it behaves as expected
    keys = ensure_pressed("s")  # ensure s is being pressed
    for a in range(2):
        uiManager.draw_UI(keys)  # Moves cursor down twice
    keyboard.release("s")        # release s key for future
    result_dict.update({"test1": {
        "pos": uiManager.cursor.pos[1]  # save the y cursor position
    }})

def ui_test_2(uiManager, result_dict):
    # get the result from pressing enter and save to dict
    keys = ensure_pressed("enter")  # ensure enter is being pressed
    result = uiManager.draw_UI(keys)  # get the result from pressing enter
    keyboard.release("enter")  # release enter key
    result_dict.update({"test2": {    # save result list to dict
        "result": tuple(result)
    }})


def ui_test_3(uiManager, result_dict):
    # Change UI to reset cursor pos and test if wrap around works in both ways
    uiManager.change_UI("Load Game")  # change the UI to load game
    keys = ensure_pressed("w")  # ensure w is pressed
    uiManager.draw_UI(keys)  # move the cursor
    keyboard.release("w")    # release w key
    # Now the cursor should be at the lowest position
    flag = uiManager.cursor.pos[1] == (uiManager.constraint_y[1] - 20)  # check if cursor is in proper position
    flag2 = False  # set second flag
    flag3 = False  # set third flag
    if flag:
        keys = ensure_pressed("w")  # ensure s is pressed
        uiManager.draw_UI(keys)  # move the cursor
        keyboard.release("w")    # release s
        # checks if moving up works as intended
        # since we're moving up, y is actually subtracted
        flag2 = uiManager.cursor.pos[1] == (uiManager.constraint_y[1] - uiManager.spacing_y - 20)  # 20 was the chosen offset
        if flag2:
            keys = ensure_pressed("s")  # ensure s is pressed
            for i in range(2):
                uiManager.draw_UI(keys)  # move the cursor down twice to wrap around
            keyboard.release("s")  # release s
            # Checks if the cursor wrapped around as intended
            flag3 = uiManager.cursor.pos[1] == (uiManager.constraint_y[0] - 20)

    result_dict.update({"test3": {  # stores the flag values in the dict 
        "flag": flag,
        "flag2": flag2,
        "flag3": flag3
    }})

def ui_test_4(uiManager, result_dict):
    # try to go back a UI and save the states
    keys = ensure_pressed("esc")  # ensure escape is pressed 
    uiManager.draw_UI(keys)  # test to see if the wrap around works
    keyboard.release("esc")  # release escape key
    # Confirms that we went back to start screen and that nothing was added to prevUIs
    result_dict.update({"test4": {  # store UI and prevUI info in the dict
        "UI": uiManager.UI,
        "prevUIs": tuple(uiManager.prevUIs)
    }})

def ui_test_5(uiManager, result_dict):
    # tests the results of all possible horizontal movement
    uiManager.change_UI("Startv2")  # change to a UI that has horizontal UI
    keys = ensure_pressed("d")    # move to the right once
    uiManager.draw_UI(keys)
    keyboard.release("d")
    # check if normal movement is observed when moving to the right
    flag = uiManager.cursor.pos[0] == (uiManager.constraint_x[1] - 80)
    flag2 = False
    flag3 = False
    flag4 = False
    if flag:
        keys = ensure_pressed("a")  # move to the left once
        uiManager.draw_UI(keys)
        keyboard.release("a")
        # see if the cursor position went back to the original spot
        flag2 = uiManager.cursor.pos[0] == (uiManager.constraint_x[0] - 80)
        if flag2:
            # test wrap around left
            keys = ensure_pressed("a")  # move to the left once
            uiManager.draw_UI(keys)
            keyboard.release("a")
            # check if wrap around succeeded
            flag3 = uiManager.cursor.pos[0] == (uiManager.constraint_x[1] - 80)
            if flag3:
                keys = ensure_pressed("d")  # move to the right once
                uiManager.draw_UI(keys)
                keyboard.release("d")
                flag4 = uiManager.cursor.pos[0] == (uiManager.constraint_x[0] - 80)
    result_dict.update({"test5": {
        "flag": flag,
        "flag2": flag2,
        "flag3": flag3,
        "flag4": flag4
    }})

def ui_test_6(uiManager, result_dict):
    uiManager.change_UI("Startv2")  # change to appropriate UI
    keys = ensure_pressed("d")    # Move right once
    uiManager.draw_UI(keys)
    keyboard.release("d")
    keys = ensure_pressed("s")    # move down once
    uiManager.draw_UI(keys)
    keyboard.release("s")
    keys = ensure_pressed("enter")  # press enter once
    result = uiManager.draw_UI(keys)  # save result
    result_dict.update({"test6": {    # save result list to dict
        "result": tuple(result)
    }})

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

    elif arg == "run-tests":
        uiManager = UIManager(font, screen)
        result_dict = {}
        ui_test_1(uiManager, result_dict)
        ui_test_2(uiManager, result_dict)
        ui_test_3(uiManager, result_dict)
        ui_test_4(uiManager, result_dict)
        ui_test_5(uiManager, result_dict)
        ui_test_6(uiManager, result_dict)
        os.chdir("testDetails/")
        file = open("test_results.json", "w")
        json.dump(result_dict, file,  indent=3)
        file.close()
        os.chdir("../")

    elif arg == "test":
        pass
        #os.chdir("testDetails")
        #print(os.getcwd())
        #os.chdir("../")
        #print(os.getcwd())
    game.quit()
    exit()