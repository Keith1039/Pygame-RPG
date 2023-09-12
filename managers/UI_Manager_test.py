import pygame as game
from managers import UIManager

game.init()
screen = game.display.set_mode((1422, 800))
font = game.font.Font('font/Pixeltype.ttf', 50)
uiManager = UIManager(font, screen)
keys_dict = {"s": game.K_DOWN, "w": game.K_UP, "a": game.K_LEFT, "d": game.K_RIGHT, "enter": game.K_RETURN,
             "esc": game.K_ESCAPE}
def get_keydown_event(key):
    game.event.post(game.event.Event(game.KEYDOWN, key=keys_dict[key]))  # Create keydown event and add to queue
    return game.event.get()  # Get the event queue also removes all events from queue
def test_init():
   # Starting UI is always "Start" and there are no prevUIs
    assert uiManager.UI == 'Start' and len(uiManager.prevUIs) == 0

def test_cursor_movement_down():
    # Checks if the cursor was successfully moved down twice
    eventList = get_keydown_event("s")  # ensure s is being pressed
    for a in range(2):
        uiManager.draw_UI(eventList)  # Moves cursor down twice
    yPos = uiManager.cursor.pos[1]  # Get the y position of cursor
    assert yPos == (uiManager.constraint_y[1] - 20)  # 20 was the chosen offset

def test_confirmation_input():
    # get the result from pressing enter and save to dict
    eventList = get_keydown_event("enter")  # ensure enter is being pressed
    result = uiManager.draw_UI(eventList)  # get the result from pressing enter
    assert list(result) == ["Start", "Load Game"]

def test_move_to_Load_screen():
    uiManager.change_UI("Load Game")
    # UI should now be Load Game and the prevUIs list should be updated with "Start"
    assert uiManager.UI == "Load Game" and uiManager.prevUIs[0] == "Start"

def test_wrap_around_vertical():
    # Change UI to reset cursor pos and test if wrap around works in both ways
    eventList = get_keydown_event("w")  # ensure w is pressed
    uiManager.draw_UI(eventList)  # move the cursor
    # Now the cursor should be at the lowest position
    flag = uiManager.cursor.pos[1] == (uiManager.constraint_y[1] - 20)  # check if cursor is in proper position
    flag2 = False  # set second flag
    flag3 = False  # set third flag
    if flag:
        eventList = get_keydown_event("w")  # ensure s is pressed
        uiManager.draw_UI(eventList)  # move the cursor
        # checks if moving up works as intended
        # since we're moving up, y is actually subtracted
        flag2 = uiManager.cursor.pos[1] == (
                    uiManager.constraint_y[1] - uiManager.spacing_y - 20)  # 20 was the chosen offset
        if flag2:
            eventList = get_keydown_event("s")  # ensure s is pressed
            for i in range(2):
                uiManager.draw_UI(eventList)  # move the cursor down twice to wrap around
            # Checks if the cursor wrapped around as intended
            flag3 = uiManager.cursor.pos[1] == (uiManager.constraint_y[0] - 20)
    assert flag and flag2 and flag3

def test_back_track():
    # try to go back a UI and save the states
    eventList = get_keydown_event("esc")  # ensure escape is pressed
    uiManager.draw_UI(eventList)  # test to see if the wrap around works
    # Confirms that we went back to start screen and that nothing was added to prevUIs
    assert uiManager.UI == "Start" and len(uiManager.prevUIs) == 0

def test_horizontal_movement():
    # tests the results of all possible horizontal movement
    uiManager.change_UI("Startv2")  # change to a UI that has horizontal UI
    eventList = get_keydown_event("d")    # move to the right once
    uiManager.draw_UI(eventList)
    # check if normal movement is observed when moving to the right
    flag = uiManager.cursor.pos[0] == (uiManager.constraint_x[1] - 80)
    flag2 = False
    flag3 = False
    flag4 = False
    if flag:
        eventList = get_keydown_event("a")  # move to the left once
        uiManager.draw_UI(eventList)
        # see if the cursor position went back to the original spot
        flag2 = uiManager.cursor.pos[0] == (uiManager.constraint_x[0] - 80)
        if flag2:
            # test wrap around left
            eventList = get_keydown_event("a")  # move to the left once
            uiManager.draw_UI(eventList)
            # check if wrap around succeeded
            flag3 = uiManager.cursor.pos[0] == (uiManager.constraint_x[1] - 80)
            if flag3:
                eventList = get_keydown_event("d")  # move to the right once
                uiManager.draw_UI(eventList)
                flag4 = uiManager.cursor.pos[0] == (uiManager.constraint_x[0] - 80)
    assert flag and flag2 and flag3 and flag4

def test_horizontal_confirmation_input():
    uiManager.change_UI("Startv2")  # change to appropriate UI
    eventList = get_keydown_event("d")    # Move right once
    uiManager.draw_UI(eventList)
    eventList = get_keydown_event("s")    # move down once
    uiManager.draw_UI(eventList)
    eventList = get_keydown_event("enter")  # press enter once
    result = uiManager.draw_UI(eventList)  # save result
    assert result[0] == "Startv2" and result[1] == "Optionsv2"

# Checks if we can set the UI to None safely
def test_None_UI():
    uiManager.change_UI(None)
    assert True
