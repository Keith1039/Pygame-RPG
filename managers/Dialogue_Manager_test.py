import pygame

from managers.Dialogue_Manager import DialogueManager
from managers.Screen_Manager import Event
import pygame as game

game.init()
screen = game.display.set_mode((1422, 800))
clock = game.time.Clock()
game.display.set_caption("Legend of Zeroes, Trails of Cold Meals")
font = game.font.Font('font/Pixeltype.ttf', 50)
dialogueManager = DialogueManager(font, screen)
mockDialogEvent = Event(None, "Dialogue","event_text/Test_dialogue.txt")

def get_size_of_file(event):
    i = 0
    file = open(event.path, "r")
    text = file.readline()
    while text != "":
        text = file.readline()
        i += 1
    file.close()
    return i

def mock_draw_dialogue():
    # Version of draw_dialogue that doesn't do any of the drawing.
    actualLen = get_size_of_file(mockDialogEvent)
    len = 1  # Once the file is loaded, the first line is already read
    text = dialogueManager.prevText
    flag = dialogueManager.prevText != ""  # When loading the file prevText should have first line

    return flag
def test_load_file():
    # Load file just uses open() to get a file object. Loading a valid file should 
    # actually load the file thus making file not None
    dialogueManager.load_file(mockDialogEvent)
    assert dialogueManager.file is not None

def test_clear_file():
    # Checks if the file value in the manager is None and the file is cleared properly
    # Also checks if all the lines were properly read.
    # Also checks if the events activated value has been changed. Might need to add a
    # 'repeatable' value to events in the case of repeatable dialogue etc
    fileLength = get_size_of_file(mockDialogEvent)  # Gets the length of the file
    dialogueManager.load_file(mockDialogEvent)  # Loads the event
    file = dialogueManager.file  # Create reference to file to check if closed later
    length = 0
    flag = dialogueManager.prevText != ""
    while flag:
        game.event.post(game.event.Event(pygame.KEYDOWN, key=game.K_RETURN))  # Creates the keydown event
        eventList = game.event.get()  # Returns the list of events
        flag = dialogueManager.draw_dialogue(eventList)  # draw dialogue call
        length += 1  # Increment the size
    assert file.closed and dialogueManager.file is None and mockDialogEvent.activated and length == fileLength
