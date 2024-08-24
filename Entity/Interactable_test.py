from Entity.Interactable import Interactable

interactable = Interactable()  # make a basic interactable
interactable.genericKey = "genericDialogue"  # set the generic dialogue

def test_add_events():
    interactable.Events = ["testEvent"]  # set the events list
    oldEvents = interactable.Events.copy()  # a copy of the old events
    newEvents = ["testEvent2"]  # the new event
    interactable.add_event_keys(newEvents)  # add the events to the NPC
    flag = interactable.Events == (oldEvents + newEvents)  # checked to see if the old events + new events were added
    flag2 = interactable.Events[0] == "testEvent" and interactable.Events[1] == "testEvent2"
    assert flag and flag2

def test_get_event_key():
    interactable.Events = ["testEvent", "testEvent2"]  # set the events
    eventKeys = []  # a list of the event keys returned
    for i in range(3):
        eventKeys.append(interactable.get_event_key())  # add the key to the list
    flag = len(eventKeys) == 3
    # confirm that the repeatable event doesn't get removed
    flag2 = eventKeys[0] == "testEvent" and eventKeys[1] == "testEvent" and eventKeys[2] == "testEvent"
    interactable.Events = ["testEvent2"]  # reset events list
    eventKeys.clear()  # clear the list
    # get the 3 event keys
    for i in range(3):
        eventKeys.append(interactable.get_event_key())
    # check if the list is empty
    flag3 = len(interactable.Events) == 0
    # check if the proper keys were returned
    flag4 = eventKeys[0] == "testEvent2" and eventKeys[1] == "genericDialogue" and eventKeys[2] == "genericDialogue"
    assert flag and flag2 and flag3 and flag4

def test_sort_events():
    interactable.Events = ["mockDialogue", "mockDialogue2"]  # set the events
    interactable.sort_events()  # sort the event keys
    # check if the keys were sorted
    assert interactable.Events[0] == "mockDialogue2" and interactable.Events[1] == "mockDialogue"
