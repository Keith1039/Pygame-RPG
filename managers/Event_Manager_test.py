import pygame as game
import managers


screen = game.display.set_mode((1422, 800))
font = game.font.Font('font/Pixeltype.ttf', 50)
knight = managers.Knight()

dialogueManager = managers.DialogueManager(screen, font)
questManager = managers.QuestManager(knight)
eventManager = managers.EventManager(knight, dialogueManager, questManager)

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
    # TEST CASES FOR DIALOGUE MANAGER
    ##########################################################
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
    ##########################################################

    # TEST CASES FOR QUEST MANAGER
    ##########################################################
    eventManager.push_event("testQuestEvent")
    flag5 = len(eventManager.events) == 1  # confirm the event went through
    eventManager.process_events("", 0)
    # check to see if the dialogue event was sent and the quest was received
    flag6 = not eventManager.eventDict["testQuestEvent"]["Activated"] and len(eventManager.events) == 0 \
        and len(dialogueManager.nextEvents) == 3 and len(questManager.activeQuests) == 1
    eventManager.push_event("testQuestEvent2")
    flag7 = len(eventManager.events) == 1  # confirm the event went through
    eventManager.process_events("", 0)
    # check to see if the event was activated and the event was properly processed and the quest was received
    flag8 = eventManager.eventDict["testQuestEvent2"]["Activated"] and len(eventManager.events) == 0 \
        and len(questManager.activeQuests) == 2
    assert flag and flag2 and flag3 and flag4 and flag5 and flag6 and flag7 and flag8

