import managers
import pygame as game
from managers.UI_Manager_test import get_keydown_event


game.init()

font = game.font.Font('font/Pixeltype.ttf', 50)
screen = game.display.set_mode((1422, 800))

# Initializing things
screenManager = managers.ScreenManager(screen)
dummyKnight = managers.Knight()
battleManager = managers.BattleManager(dummyKnight)
saveManager = managers.SaveManager(dummyKnight, vars(), screenManager)
UIManager = managers.UIManager(font, screen)
UIHandler = managers.UIHandler(UIManager, saveManager, dummyKnight, vars(), dummyKnight)

# Variables I need for save manager
start = True  # same as the variable that depends
animationTracker = 0
animationTracker2 = 0
animationTracker3 = 0
gameState = ""
x = 0

def test_simulate_start_screen():
    context, choice = UIManager.draw_UI(get_keydown_event("enter"))  # press start
    UIHandler.handle_interaction(context, choice)
    # Start should be false and UIManager vars should be cleared
    assert not start and UIManager.UI is None and len(UIManager.prevUIs) == 0 and choice == "Start Game"

def test_simulate_continue_selection():
    UIHandler.localVars.update({"start": True})  # Reset start to true
    UIManager.change_UI("Start")  # Reset UIManager
    UIManager.draw_UI(get_keydown_event("s"))        # Move down 1
    context, choice = UIManager.draw_UI(get_keydown_event("enter"))  # press start
    UIHandler.handle_interaction(context, choice)
    assert not start and UIManager.UI is None and len(UIManager.prevUIs) == 0 and choice == "Continue"

def test_simulate_move_to_load_screen():
    UIManager.change_UI("Start")  # Reset UIManager
    UIManager.draw_UI(get_keydown_event("s"))        # Move down 1
    UIManager.draw_UI(get_keydown_event("s"))        # Move down 1
    context, choice = UIManager.draw_UI(get_keydown_event("enter"))  # press start
    UIHandler.handle_interaction(context, choice)
    #  UI should change and the previous UI is added to prevUIs
    assert UIManager.UI == "Load Game" and len(UIManager.prevUIs) > 0 and UIManager.prevUIs[0] == "Start"

def test_simulate_load_fail():
    # Assume slot 2 is empty
    UIHandler.localVars.update({"start": True})  # Reset start to true
    UIManager.draw_UI(get_keydown_event("s"))    # Move down 1
    context, choice = UIManager.draw_UI(get_keydown_event("enter"))  # press start
    UIHandler.handle_interaction(context, choice)
    assert start and UIManager.UI == "Load Game"  # We haven't moved screens and start isn't switched off

def test_simulate_load_success():
    # Assume slot 1 isn't empty since save manager tests should fill it
    UIManager.draw_UI(get_keydown_event("w"))        # Move up 1
    context, choice = UIManager.draw_UI(get_keydown_event("enter"))    # Press enter
    UIHandler.handle_interaction(context, choice)
    assert not start and UIManager.UI is None  # Load Succeeds

