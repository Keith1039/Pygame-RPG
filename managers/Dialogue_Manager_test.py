import json
from managers.Dialogue_Manager import DialogueManager
import pygame as game

game.init()
screen = game.display.set_mode((1422, 800))
clock = game.time.Clock()
game.display.set_caption("Legend of Zeroes, Trails of Cold Meals")
font = game.font.Font('font/Pixeltype.ttf', 50)
dialogueManager = DialogueManager(font, screen)
masterEventDict = json.load(open("JSON/Events/Events.json", "r"))  # load the master dictionary for events
mockJson = masterEventDict["mockDialogue"]
mockJson2 = masterEventDict["mockDialogue2"]

def get_size_of_file(event):
    i = 0
    file = open(event["Dialogue Path"], "r")
    text = file.readline()
    while text != "":
        text = file.readline()
        i += 1
    file.close()
    return i

def test_load_file():
    # check to see if the file loaded and that there is no missing lines
    # also confirm that the event is not activated and the event is set
    dialogueManager.load_file(mockJson)
    assert len(dialogueManager.dialogue) == get_size_of_file(mockJson) and \
        not mockJson["Activated"] and dialogueManager.event == mockJson

def test_get_new_text():
    initialLen = len(dialogueManager.dialogue)
    dialogueManager.get_new_text()
    # check to see if the length changed and see if what was lost was added to backlog
    flag = initialLen == len(dialogueManager.dialogue) + 1 and len(dialogueManager.backlog) == 1
    # clear the dialogue
    dialogueManager.dialogue.clear()
    # check to see what happens when we run get_new_text on an empty dialogue list
    dialogueManager.get_new_text()
    flag2 = mockJson["Activated"] and dialogueManager.event is None
    dialogueManager.load_file(mockJson)
    # check to see if the manager still accepts the event even if it was previously activated
    # this is a check for repeatable dialogue
    flag3 = dialogueManager.event is not None and dialogueManager.event["Activated"]
    dialogueManager.nextEvents = [mockJson2, mockJson2]  # add two non-repeatable events to the list
    dialogueManager.dialogue.clear()  # clear the list
    dialogueManager.get_new_text()
    # check to see if the new event was successfully processed
    flag4 = dialogueManager.event == mockJson2 and len(dialogueManager.nextEvents) == 1
    dialogueManager.dialogue.clear()  # clear the list
    dialogueManager.get_new_text()
    # check to see if the non-repeatable event was rejected
    flag5 = dialogueManager.event is None and len(dialogueManager.nextEvents) == 0

    dialogueManager.load_file(mockJson)  # insert the old dialogue event back in
    assert flag and flag2 and flag3 and flag4 and flag5

def test_load_portrait():
    text = "Knight: I see, move"
    returnText = dialogueManager.load_portrait(text)
    # verify that there is a portrait and the returned text was stripped of it's name and the name is stored
    flag = dialogueManager.portrait is not None and returnText == "I see, move" and dialogueManager.name == "Knight"
    text = "IDK"
    returnText = dialogueManager.load_portrait(text)
    # check to see if the portrait is none, the name is reset and the returned text wasn't modified (in this case)
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
