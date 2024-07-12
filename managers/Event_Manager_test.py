import pygame as game
import managers


screen = game.display.set_mode((1422, 800))
font = game.font.Font('font/Pixeltype.ttf', 50)
knight = managers.Knight()

dialogueManager = managers.DialogueManager(screen, font)
eventManager = managers.EventManager(knight, dialogueManager)

def test_push_event():
    invalidKey = "Whatever"
    validKey = "mockDialogue"
    eventManager.push_event(invalidKey)  # shouldn't add anything
    flag = len(eventManager.events) == 0
    eventManager.push_event(validKey)  # should add an event to the list
    assert flag and len(eventManager.events) == 1

def test_process_events():
    # push more events
    eventManager.push_event("mockDialogue2")
    eventManager.push_event("testEvent")
    eventManager.push_event("testEvent2")
    flag = len(eventManager.events) == 4  # confirm the 3 events went through
    eventManager.process_events("", 0)  # process the events
    # confirm that only 2 events were processed correctly
    flag2 = len(eventManager.dialogueManager.nextEvents) == 2 and len(eventManager.events) == 2
    eventManager.process_events("something", 175)  # give the right range to trigger the event
    # check to see if the knight received the bread and the items gained dictionary for the event wasn't cleared
    flag3 = len(eventManager.events) == 1 and len(eventManager.eventDict["testEvent"]["Items Gained"]) == 1 \
        and eventManager.knight.Inventory.get("Bread") == 1
    eventManager.process_events("Unobtainable", 0)  # give the right context to trigger the event
    # check to see if the knight received the potions and the items gained were cleared
    flag4 = len(eventManager.events) == 0 and len(eventManager.eventDict["testEvent2"]["Items Gained"]) == 0 \
        and eventManager.knight.Inventory.get("Potion") == 999
    assert flag and flag2 and flag3 and flag4

