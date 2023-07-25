from enum import Enum

# Depending on if this info is saved, Enum might be removed (not parsable by JSON)
class Status(Enum):
    UNACCESSED = 1
    ACCESSED = 2


class MapInfo:
    def __init__(self, event):
        # Indicates whether it's been seen or not. Defaults to not being accessed.
        self.status = Status.UNACCESSED
        self.event = event

    # Called every time the player moves to said space.
    def change_status(self):
        self.status = Status.ACCESSED

# Screen Manager has the background name and these get


minotaurMap = {(0, 0): MapInfo(False), (0, 1): MapInfo(True), (-1, 1): MapInfo(True), (-1, 4):  MapInfo(True),
                (-2, 6):  MapInfo(True), (1, 1):  MapInfo(True), (3, 2):  MapInfo(True), (2, 6):  MapInfo(True),
                (2, 8):  MapInfo(True)}

gargoyleBaseFloorMap = {(0, 0): MapInfo(False), (0, 1): MapInfo(True), (-1, 1): MapInfo(True),
                           (-2, 1): MapInfo(True), (1, 1): MapInfo(True), (2, 1): MapInfo(True), (3, 1): MapInfo(True),
                           (3, 0): MapInfo(True),  (-2, 2): MapInfo(True), (-2, 3): MapInfo(True),
                           (-2, 4): MapInfo(True), (3, 2): MapInfo(True), (3, 3): MapInfo(True), (2, 3): MapInfo(True),
                           (2, 4): MapInfo(True), (1, 4): MapInfo(True), (1, 5): MapInfo(True), (1, 6): MapInfo(True),
                           (0, 2): MapInfo(True)}

gargoyleBasementMap = {(0, 0): MapInfo(False), (-1, 0): MapInfo(True), (1, 0): MapInfo(True), (2, 0): MapInfo(True),
                         (2, 1): MapInfo(True), (2, 2): MapInfo(True), (1, 2): MapInfo(True), (1, 3): MapInfo(True),
                         (1, 4): MapInfo(True), (0, 4): MapInfo(True), (-1, 4): MapInfo(True), (-1, 3): MapInfo(True),
                         (-1, 2): MapInfo(True), (1, 5): MapInfo(True), (2, 5): MapInfo(True)}

gargoyleUpstairsMap = {(0, 0): MapInfo(False), (0, 1): MapInfo(True), (0, 2): MapInfo(True), (0, 3): MapInfo(True),
                         (-1, 3): MapInfo(True), (-1, 4): MapInfo(True), (-1, 5): MapInfo(True), (0, 5): MapInfo(True),
                         (1, 3): MapInfo(True), (2, 3): MapInfo(True), (2, 2): MapInfo(True), (2, 1): MapInfo(True),
                         (2, 0): MapInfo(True)}
dungeonMapDict = {"Cavern": minotaurMap, "Gargoyle Base Floor": gargoyleBaseFloorMap,
                   "Gargoyle Basement": gargoyleBasementMap, "Gargoyle Upstairs": gargoyleUpstairsMap}

# Leaving the events as strings for now. Eventually they will be replaced with functions
minotaurEvents = {(0, 1): "Fight", (-1, 1): "Book#8", (-1, 4): "Book#1", (-2, 6): "Book#3", (1, 1): "Volatile Poison",
                   (3, 2): "Potion", (2, 6): "Rest", (2, 8): "BossFight"}

gargoyleBaseFloorEvents = {(0, 1): "rest", (-1, 1): "Fight", (-2, 1): "Fight", (1, 1): "Fight", (2, 1): "Fight",
                              (3, 1): "Fight", (3, 0): "Downstairs",  (-2, 2): "Book#4", (-2, 3): "Fight",
                              (-2, 4): "Fight", (3, 2): "Potion", (3, 3): "Fight", (2, 3): "Fight", (2, 4): "Fight",
                              (1, 4): "Fight", (1, 5): "Fight", (1, 6): "Basement Key", (0, 2): "BossFight"}

gargoyleBasementEvents = {(-1, 0): "Go back to base floor", (1, 0): "Fight", (2, 0): "Fight", (2, 1): "Fight",
                            (2, 2): "Fight", (1, 2): "Rest", (1, 3): "Book#5", (1, 4): "Fight", (0, 4): "Fight",
                            (-1, 4): "Fight", (-1, 3): "Rest", (-1, 2): "Upstairs Key", (1, 5): "Fight",
                            (2, 5): "Book#6"}

gargoyleUpstairsEvents = {(0, 1): "Fight", (0, 2): "Fight", (0, 3): "Potion", (-1, 3): "Fight", (-1, 4): "Fight",
                            (-1, 5): "Fight", (0, 5): "Fight", (1, 3): "Fight", (2, 3): "Fight", (2, 2): "Fight",
                            (2, 1): "Fight", (2, 0): "Do action"}

eventsDict = {"Cavern": minotaurEvents, "Gargoyle Mansion": gargoyleBaseFloorEvents,
               "Gargoyle Basement": gargoyleBasementEvents, "Gargoyle Upstairs": gargoyleUpstairsEvents }
