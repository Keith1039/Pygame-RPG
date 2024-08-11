import managers
import pygame as game
from managers.UI_Manager_test import get_keydown_event

game.init()

font = game.font.Font('font/Pixeltype.ttf', 50)
screen = game.display.set_mode((1422, 800))

# Initializing things
screenManager = managers.ScreenManager(screen)
dummyKnight = managers.Knight()
factory = managers.EntityFactory()
itemManager = managers.ItemManager(dummyKnight)
battleManager = managers.BattleManager(dummyKnight, itemManager)
dialogueManager = managers.DialogueManager(font, screen)
questManager = managers.QuestManager(dummyKnight)
eventManager = managers.EventManager(dummyKnight, dialogueManager, questManager)
saveManager = managers.SaveManager(dummyKnight, vars(), screenManager, eventManager, questManager)
UIManager = managers.UIManager(font, screen)
UIHandler = managers.UIHandler(UIManager, saveManager, dummyKnight, vars(), battleManager, itemManager)

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

def test_simulate_targeting_transition():
    battleManager.add_enemy(factory.create_entity("dummy"))
    UIManager.change_UI("Player Select", False)  # change the UI to targeting
    eventList = get_keydown_event("enter")  # press enter
    context, choice = UIManager.draw_UI(eventList)  # process events
    UIHandler.handle_interaction(context, choice)  # handle the interaction
    # check if the UI changed and if the position is the same
    assert UIManager.UI == "Select Target" and UIManager.targets[0] == battleManager.enemies[0][0]

def test_simulate_skill_use():
    dummyKnight.moveList.append("Super Attack")  # give dummy knight an unusable skill
    dummyKnight.moveList.append("Pilfering Strike")  # give dummy knight a usable skill
    eventList = get_keydown_event("esc")  # press escape
    UIManager.draw_UI(eventList)  # process events
    eventList = get_keydown_event("s")  # go down 1
    UIManager.draw_UI(eventList)  # process events
    eventList = get_keydown_event("enter")  # press enter
    context, choice = UIManager.draw_UI(eventList)  # process events
    UIHandler.handle_interaction(context, choice)  # handle the interaction
    flag = UIManager.subMenu  # check if the submenu is active
    eventList = get_keydown_event("enter")  # press enter
    context, choice = UIManager.draw_UI(eventList)  # process events
    UIHandler.handle_interaction(context, choice)  # handle the interaction
    # the UI shouldn't have changed
    flag2 = UIManager.UI == "Player Select" and choice == "Super Attack"
    eventList = get_keydown_event("d")  # move 1 to the right
    UIManager.draw_UI(eventList)  # process events
    eventList = get_keydown_event("enter")  # press enter
    context, choice = UIManager.draw_UI(eventList)  # process events
    UIHandler.handle_interaction(context, choice)  # handle the interaction
    flag3 = UIManager.UI == "Select Target" and choice == "Pilfering Strike"
    assert flag and flag2 and flag3
