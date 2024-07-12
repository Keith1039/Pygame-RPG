import pygame

from managers.Dialogue_Manager import DialogueManager
import pygame as game

game.init()
screen = game.display.set_mode((1422, 800))
clock = game.time.Clock()
game.display.set_caption("Legend of Zeroes, Trails of Cold Meals")
font = game.font.Font('font/Pixeltype.ttf', 50)
dialogueManager = DialogueManager(font, screen)
mockJson = {"EventType": "Dialogue", "Path": "event_text/Test_dialogue.txt", "Activated": False}

def get_size_of_file(event):
    i = 0
    file = open(event["Path"], "r")
    text = file.readline()
    while text != "":
        text = file.readline()
        i += 1
    file.close()
    return i

def test_load_file():
    # check to see if the file loaded and that there is no missing lines
    # also confirm that the event is activated
    dialogueManager.load_file(mockJson)
    assert len(dialogueManager.dialogue) == get_size_of_file(mockJson) and \
        mockJson["Activated"]

def test_get_new_text():
    dialogueCopy = dialogueManager.dialogue.copy()
    initialLen = len(dialogueManager.dialogue)
    dialogueManager.get_new_text()
    # check to see if the length changed and see if what was lost was added to backlog
    flag = initialLen == len(dialogueManager.dialogue) + 1 and len(dialogueManager.backlog) == 1
    # clear the dialogue
    dialogueManager.dialogue.clear()
    # check if this can run on an empty list
    dialogueManager.get_new_text()
    # insert the copy into the object
    dialogueManager.dialogue = dialogueCopy
    assert flag

def test_load_portrait():
    text = "Knight: I see, move"
    returnText = dialogueManager.load_portrait(text)
    # verify that there is a portrait and the returned text was not modified while confirming the name is correct
    flag = dialogueManager.portrait is not None and text == returnText and dialogueManager.name == "Knight"
    text = "IDK"
    returnText = dialogueManager.load_portrait(text)
    # check to see if the portrait is none, the name is reset and the returned text wasn't modified
    flag2 = dialogueManager.portrait is None and text == returnText and dialogueManager.name == ""
    assert flag and flag2

def test_load_dialogue_list():
    # check to see if the array was accepted
    longText = "This is a really long sentence and I can't be bothered to trim it"
    dialogueManager.load_dialogue_list([longText])
    assert dialogueManager.dialogue == [longText]

def test_sub_divide_dialogue():
    longerText = "This is a really long sentence and I can't be bothered to trim it so deal with it how you will because I'm him"
    # subdivide the long text
    dialogueManager.sub_divide_dialogue(dialogueManager.dialogue[0])
    # verify that there is indeed 2 lines for this
    flag = len(dialogueManager.firstLine) > 0 and len(dialogueManager.secondLine) > 0
    dialogueManager.sub_divide_dialogue(longerText)
    # verify that there is indeed 2 lines for this and verify that the rest was appended to the dialogue list
    flag2 = len(dialogueManager.firstLine) > 0 and len(dialogueManager.secondLine) > 0 \
        and len(dialogueManager.dialogue) == 2
    assert flag and flag2
