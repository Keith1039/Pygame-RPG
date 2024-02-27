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

def test_handle_submenu_input():
    # remember that handle_submenu_input() doesn't do any validation
    letters = ["w", "a", "s", "d"]
    flag = True
    # go through all cardinal directions and ensure that flag is always False
    for i in range(len(letters)):
        flag = uiManager.handle_submenu_input(get_keydown_event(letters[i]))
        if flag or flag is None:
            break
    flag2 = uiManager.handle_submenu_input(get_keydown_event("enter"))
    flag3 = uiManager.handle_submenu_input(get_keydown_event("esc"))
    # check the state of all flags and ensure that the slider is 0
    assert not flag and flag2 and flag3 is None and uiManager.subMenuSlider == -1

def test_player_select_UI():
    # This test case effectively checks the desired behavior for a submenu
    uiManager.change_UI("Player Select", False)
    uiManager.subMenu = True
    uiManager.subMenuItems = ["Power", "Defensive", "Nimble",  # fill the items list with content
                                "Power", "Defensive", "Nimble",
                                "Power", "Defensive", "Nimble",
                                "Power"]
    eventList = get_keydown_event("a")
    uiManager.draw_UI(eventList)  # move left 1 (should not be possible)
    flag = uiManager.subMenuSlider == 0 and uiManager.subMenuMinIndex == 0 and uiManager.subMenuMaxIndex == 8
    eventList = get_keydown_event("d")
    uiManager.draw_UI(eventList)  # move 1 to the right of submenu
    flag2 = uiManager.subMenuSlider == 1 and uiManager.subMenuMinIndex == 0 and uiManager.subMenuMaxIndex == 8
    eventList = get_keydown_event("s")
    for i in range(12):
        uiManager.draw_UI(eventList)  # move down 1
    # check if scroll down happened
    flag3 = uiManager.subMenuMinIndex == uiManager.subMenuMaxIndex == uiManager.subMenuSlider == 9
    eventList = get_keydown_event("w")
    uiManager.draw_UI(eventList)  # move up 1
    # check if scroll up happened
    flag4 = uiManager.subMenuSlider == 6 and uiManager.subMenuMinIndex == 0 and uiManager.subMenuMaxIndex == 8
    eventList = get_keydown_event("a")
    for i in range(3):
        uiManager.draw_UI(eventList)  # move left 1
    # see if scroll up can be triggered by moving left
    flag5 = uiManager.subMenuSlider == 3 and uiManager.subMenuMinIndex == 0 and uiManager.subMenuMaxIndex == 8
    eventList = get_keydown_event("d")
    for i in range(50):
        uiManager.draw_UI(eventList)  # move right 1
    # see if scroll down is triggered by moving right
    flag6 = uiManager.subMenuMinIndex == uiManager.subMenuMaxIndex == uiManager.subMenuSlider == 9
    eventList = get_keydown_event("enter")
    context, choice = uiManager.draw_UI(eventList)
    flag7 = context == "Player Select(S)" and choice == "Power"
    eventList = get_keydown_event("esc")
    uiManager.draw_UI(eventList)
    # check if we can exit a submenu via escape and all the values are the correct values
    flag8 = not uiManager.subMenu and \
            uiManager.subMenuMaxIndex == uiManager.subMenuSlider == uiManager.subMenuMinIndex == -1 and \
            len(uiManager.subMenuItems) == 0
    assert flag and flag2 and flag3 and flag4 and flag5 and flag6 and flag7 and flag8

def test_handle_select_input():
    uiManager.targetSlider = 0  # set to default values
    letters = ["w", "a", "s", "d"]
    flag = True
    # go through all cardinal directions and ensure that flag is always False
    for i in range(len(letters)):
        flag = uiManager.handle_select_inputs(get_keydown_event(letters[i]))
        if flag or flag is None:
            break
    flag2 = uiManager.handle_select_inputs(get_keydown_event("enter"))
    flag3 = uiManager.handle_select_inputs(get_keydown_event("esc"))
    # check the state of all flags and ensure that the slider is 0
    assert not flag and flag2 and flag3 is None and uiManager.targetSlider == 0

def test_target_select_UI():
    # set up for the test
    targetable = []
    for i in range(6):
        targetable.append((100 + int(i/3) * 300, 100 + i%3 * 250))
    uiManager.targets = targetable  # set to default values
    uiManager.targetSlider = 0  # set to default values
    uiManager.change_UI("Select Target")  # change the ui to target selection
    eventList = get_keydown_event("d")
    for i in range(2):
        uiManager.draw_UI(eventList)  # move 1 to the right
    flag = uiManager.targetSlider == 3
    eventList = get_keydown_event("w")
    uiManager.draw_UI(eventList)
    flag2 = uiManager.targetSlider == 2
    eventList = get_keydown_event("s")
    uiManager.draw_UI(eventList)
    flag3 = uiManager.targetSlider == 3  # move 1 down
    for i in range(12):
        uiManager.draw_UI(eventList)  # move 1 down
    flag4 = uiManager.targetSlider == 5
    eventList = get_keydown_event("enter")
    context, choice = uiManager.draw_UI(eventList)
    flag5 = context == "Select Target" and choice == (400, 600)
    eventList = get_keydown_event("esc")
    uiManager.draw_UI(eventList)
    flag6 = uiManager.UI == "Player Select"
    assert flag and flag2 and flag3 and flag4 and flag5 and flag6
