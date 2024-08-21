import Utils

class EventManager():
    def __init__(self, knight, dialogueManager, questManager):
        self.eventDict = Utils.get_event_dict()
        self.events = []
        self.knight = knight
        self.dialogueManager = dialogueManager
        self.questManager = questManager

    def push_event(self, eventName):
        # adds the event to the list by using the key for the event
        event = self.eventDict.get(eventName)
        if event is not None:  # only valid events get added to the event queue
            self.events.append(event)

    def process_events(self, context):
        # master dictionary should be automatically updated if events came from it
        unprocessedEvents = []
        for eventInfo in self.events:
            # check if the context matches or doesn't matter
            # check if the knight is in range or if range doesn't matter
            eventType = eventInfo["Event Type"]  # the type of the event
            if (eventInfo["Context"] == "" or eventInfo["Context"] == context) and \
                    (len(eventInfo["Range"]) == 0 or eventInfo["Range"][0] < self.knight.x < eventInfo["Range"][1]):
                if eventType == "Dialogue":
                    self.dialogueManager.nextEvents.append(eventInfo)  # add to the list of events for dialogueManager
                elif eventType == "Quest":
                    if eventInfo["Dialogue Path"] != "":  # check if there is dialogue accompanying this quest event
                        self.dialogueManager.nextEvents.append(eventInfo)  # add the dialogue to the list of events
                    else:
                        eventInfo["Activated"] = True  # set it to true
                    self.questManager.add_quest(eventInfo["Quest"])  # add the quest to the quest manager
                self.knight.add_all_to_inventory(eventInfo["Items Gained"])  # add all the items from the events
                if not eventInfo["Repeatable"]:  # check if this is a repeatable event
                    eventInfo["Items Gained"].clear()  # clear this dictionary (make it one time)
            else:
                # if the event condition isn't triggered, the event is added to the unprocessed list
                unprocessedEvents.append(eventInfo)
        self.events = unprocessedEvents  # set the event list
