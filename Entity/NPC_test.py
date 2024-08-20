from Entity.NPC import NPC
import json

file = open("JSON/NPCs/NPCs.json", "r")
npc = NPC(json.load(file)["testNPC"])
file.close()

def test_update():
    npc.update()  # update the sprite
    flag = npc.aniTracker == 1  # check if the
    npc.aniTracker = 9  # set it to 1 tick before the change
    # set rect and image to None to see if they'll be reset
    npc.rect = None
    npc.image = None
    npc.update()
    # check if rect and image were set and confirm this happened on the tenth frame
    flag2 = npc.rect is not None and npc.image is not None and npc.aniTracker == 10
    npc.aniTracker = (npc.maxAniVal * 10) + 9  # a number that exceeds the max and is 1 tick away from an update
    npc.update()  # update the sprite
    flag3 = npc.aniTracker == 0  # check to see if the tracker was reset
    assert flag and flag2 and flag3

def test_add_events():
    oldEvents = npc.Dialogue.copy()  # a copy of the old events
    newEvents = ["testEvent2", "testEvent3"]  # the newer events
    npc.add_event_keys(newEvents)  # add the events to the NPC
    flag = npc.Dialogue == (oldEvents + newEvents)  # checked to see if the old events + new events were added
    flag2 = npc.Dialogue[0] == "testEvent" and npc.Dialogue[1] == "testEvent2" and npc.Dialogue[2] == "testEvent3"
    assert flag and flag2

def test_get_event_key():
    npc.Dialogue = ["testEvent", "testEvent2"]  # set the events
    eventKeys = []  # a list of the event keys returned
    for i in range(3):
        eventKeys.append(npc.get_event_key())  # add the key to the list
    flag = len(eventKeys) == 3
    flag2 = eventKeys[0] == "testEvent" and eventKeys[1] == "testEvent2" and eventKeys[2] == "genericDialogue"
    assert flag and flag2
