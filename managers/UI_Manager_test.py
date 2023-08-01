import pygame as game
from managers import UIManager
import json
game.init()
screen = game.display.set_mode((1422, 800))
font = game.font.Font('font/Pixeltype.ttf', 50)
#keys = game.key.get_pressed()
uiManager = UIManager(font, screen)
test_info = json.load(open("testDetails/test_results.json", "r"))  # because of script, this should always exist
def test_init():
   # Starting UI is always "Start" and there are no prevUIs
    assert uiManager.UI is 'Start' and len(uiManager.prevUIs) == 0

def test_cursor_movement_down():
    # Checks if the cursur was successfully moved down twice
    yPos = test_info["test1"]["pos"]
    assert yPos == (uiManager.constraint_y[1] - 20)  # 20 was the chosen offset

def test_confirmation_input():
    result = test_info["test2"]["result"]
    assert list(result) == ["Start", "Load Game"]

def test_move_to_Load_screen():
    uiManager.change_UI("Load Game")
    # UI should now be Load Game and the prevUIs list should be updated with "Start"
    assert uiManager.UI == "Load Game" and uiManager.prevUIs[0] == "Start"

def test_wrap_around_vertical():
    test_dict = test_info["test3"]
    flag = test_dict["flag"]
    flag2 = test_dict["flag2"]
    flag3 = test_dict["flag3"]
    assert flag and flag2 and flag3

def test_back_track():
    test_dict = test_info["test4"]
    ui = test_dict["UI"]
    prevUIs = test_dict["prevUIs"]
    assert ui == "Start" and len(prevUIs) == 0

def test_horizontal_movement():
    # tests if the horizontal movements are working as intended
    print(test_info)
    test_dict = test_info["test5"]
    flag = test_dict["flag"]
    flag2 = test_dict["flag2"]
    flag3 = test_dict["flag3"]
    flag4 = test_dict["flag4"]
    assert flag and flag2 and flag3 and flag4

def test_horizontal_confirmation_input():
    # Checks if the results dict is accurate even in a 2D plane
    result = test_info["test6"]["result"]
    assert result[0] == "Startv2" and result[1] == "Optionsv2"

# Checks if we can set the UI to None safely
def test_None_UI():
    uiManager.change_UI(None)
    assert True
