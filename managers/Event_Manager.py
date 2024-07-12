import json

class EventManager():
    def __init__(self, knight, dialogueManager):
        self.eventDict = self.get_event_dict()
        self.events = []
        self.knight = knight
        self.dialogueManager = dialogueManager

    def get_event_dict(self):
        file = open("JSON/Events/Events.json", "r")
        d = json.load(file)
        file.close()
        return d
    def push_event(self, eventName):
        # adds the event to the list by using the key for the event
        event = self.eventDict.get(eventName)
        if event is not None:  # only valid events get added to the event queue
            self.events.append(event)

    def process_events(self, context, x):
        # master dictionary should be automatically updated if events came from it
        unprocessedEvents = []
        for eventInfo in self.events:
            # check if the context matches or doesn't matter
            # check if the knight is in range or if range doesn't matter
            if (eventInfo["Context"] == "" or eventInfo["Context"] == context) and \
                    (len(eventInfo["Range"]) == 0 or eventInfo["Range"][0] < x < eventInfo["Range"][1]):
                if eventInfo["Event Type"] == "Dialogue":
                    self.dialogueManager.nextEvents.append(eventInfo)  # add to the list of events for dialogueManager
                self.knight.add_all_to_inventory(eventInfo["Items Gained"])  # add all the items from the events
                if not eventInfo["Repeatable"]:  # check if this is a repeatable event
                    eventInfo["Items Gained"].clear()  # clear this dictionary (make it one time)
            else:
                # if the event condition isn't triggered, the event is added to the unprocessed list
                unprocessedEvents.append(eventInfo)
        self.events = unprocessedEvents  # set the event list



