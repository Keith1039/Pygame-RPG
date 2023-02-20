from enum import Enum


class Status(Enum):
    UNACCESSED = 1
    ACCESSED = 2


class MapInfo:
    def __init__(self, event):
        # Indicates whether it's been seen or not. Defaults to not being accessed.
        self.status = Status.UNACCESSED
        self.event = event

    # Called every time the player moves to said space.
    def changeStatus(self):
        self.status = Status.ACCESSED

# Screen Manager has the background name and these get


Minotaur_map = {(0, 0): MapInfo(False), (0, 1): MapInfo(True), (-1, 1): MapInfo(True), (-1, 4):  MapInfo(True),
                (-2, 6):  MapInfo(True), (1, 1):  MapInfo(True), (3, 2):  MapInfo(True), (2, 6):  MapInfo(True),
                (2, 8):  MapInfo(True)}

Gargoyle_base_floor_Map = {(0, 0): MapInfo(False), (0, 1): MapInfo(True), (-1, 1): MapInfo(True),
                           (-2, 1): MapInfo(True), (1, 1): MapInfo(True), (2, 1): MapInfo(True), (3, 1): MapInfo(True),
                           (3, 0): MapInfo(True),  (-2, 2): MapInfo(True), (-2, 3): MapInfo(True),
                           (-2, 4): MapInfo(True), (3, 2): MapInfo(True), (3, 3): MapInfo(True), (2, 3): MapInfo(True),
                           (2, 4): MapInfo(True), (1, 4): MapInfo(True), (1, 5): MapInfo(True), (1, 6): MapInfo(True),
                           (0, 2): MapInfo(True)}

Gargoyle_basement_map = {(0, 0): MapInfo(False), (-1, 0): MapInfo(True), (1, 0): MapInfo(True), (2, 0): MapInfo(True),
                         (2, 1): MapInfo(True), (2, 2): MapInfo(True), (1, 2): MapInfo(True), (1, 3): MapInfo(True),
                         (1, 4): MapInfo(True), (0, 4): MapInfo(True), (-1, 4): MapInfo(True), (-1, 3): MapInfo(True),
                         (-1, 2): MapInfo(True), (1, 5): MapInfo(True), (2, 5): MapInfo(True)}

Gargoyle_upstairs_map = {(0, 0): MapInfo(False), (0, 1): MapInfo(True), (0, 2): MapInfo(True), (0, 3): MapInfo(True),
                         (-1, 3): MapInfo(True), (-1, 4): MapInfo(True), (-1, 5): MapInfo(True), (0, 5): MapInfo(True),
                         (1, 3): MapInfo(True), (2, 3): MapInfo(True), (2, 2): MapInfo(True), (2, 1): MapInfo(True),
                         (2, 0): MapInfo(True)}
DungeonMap_Dict = {"Cavern": Minotaur_map, "Gargoyle Base Floor": Gargoyle_base_floor_Map,
                   "Gargoyle Basement": Gargoyle_basement_map, "Gargoyle Upstairs": Gargoyle_upstairs_map}

# Leaving the events as strings for now. Eventually they will be replaced with functions
Minotaur_events = {(0, 1): "Fight", (-1, 1): "Book#8", (-1, 4): "Book#1", (-2, 6): "Book#3", (1, 1): "Volatile Poison",
                   (3, 2): "Potion", (2, 6): "Rest", (2, 8): "BossFight"}

Gargoyle_base_floor_events = {(0, 1): "rest", (-1, 1): "Fight", (-2, 1): "Fight", (1, 1): "Fight", (2, 1): "Fight",
                              (3, 1): "Fight", (3, 0): "Downstairs",  (-2, 2): "Book#4", (-2, 3): "Fight",
                              (-2, 4): "Fight", (3, 2): "Potion", (3, 3): "Fight", (2, 3): "Fight", (2, 4): "Fight",
                              (1, 4): "Fight", (1, 5): "Fight", (1, 6): "Basement Key", (0, 2): "BossFight"}

Gargoyle_Basement_events = {(-1, 0): "Go back to base floor", (1, 0): "Fight", (2, 0): "Fight", (2, 1): "Fight",
                            (2, 2): "Fight", (1, 2): "Rest", (1, 3): "Book#5", (1, 4): "Fight", (0, 4): "Fight",
                            (-1, 4): "Fight", (-1, 3): "Rest", (-1, 2): "Upstairs Key", (1, 5): "Fight",
                            (2, 5): "Book#6"}

Gargoyle_Upstairs_events = {(0, 1): "Fight", (0, 2): "Fight", (0, 3): "Potion", (-1, 3): "Fight", (-1, 4): "Fight",
                            (-1, 5): "Fight", (0, 5): "Fight", (1, 3): "Fight", (2, 3): "Fight", (2, 2): "Fight",
                            (2, 1): "Fight", (2, 0): "Do action"}

events_Dict = {"Cavern": Minotaur_events, "Gargoyle_Mansion": Gargoyle_base_floor_events,
               "Gargoyle_Basement": Gargoyle_Basement_events, "Gargoyle_Upstairs": Gargoyle_Upstairs_events }
