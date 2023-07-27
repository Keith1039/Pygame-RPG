import pygame as game

from managers.Object_Animation_Manager import ObjectAnimationManager

class Event:
    def __init__(self, pos, eventType, path=""):
        self.range = pos
        self.eventType = eventType
        self.activated = False
        self.path = path

    def load(self, infoDict):
        self.range = tuple(infoDict["range"])
        self.eventType = infoDict["eventType"]
        self.activated = infoDict["activated"]
        self.path = infoDict["path"]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

# Screen manager should draw the actual stuff I guess?
# For now there's only going to be two options moving to the left screen and moving to the right screen
# Moving to right screen = 1
# Moving to left screen = -1
chestB1 = Event((500, 600), "Chest")
screen_dict = {("Background1", 1): "Background2", ("Background2", -1): "Background1"}
background_dict ={"Background1": "Background_Art/gothic_chapel_portfolio_1422x800.png",
                  "Background2": "Background_Art/PNG/game_background_1/game_background_1.png"}
interactables_dict = {"Background1": (chestB1, ), "Background2": ()}   # NEEDS TO BE SAVED
objects_dict = {"Background1": ((800, 500), True), "Background2": ()}  # NEEDS TO BE SAVED

class ScreenManager:
    def __init__(self, screen):
        self.interactables = ()
        self.context = "Background1"  # Only thing that I need to keep track of when I do save
        self.screen = screen
        self.objects = ()
        self.objectAni = ObjectAnimationManager()
        self.objectDict = objects_dict
        self.interactablesDict = interactables_dict
        self.apply_context()


    def change_screen(self, pos):
        mover = 0
        if pos > 1000:
            mover = 1
        elif pos < -280:
            mover = -1
        prevContext = self.context
        self.context = screen_dict.get((self.context, mover))
        background = background_dict.get(self.context)
        # Basically if there's not a map value to the right don't let the players go right
        if background is None:
            self.context = prevContext
        else:
            self.screen = game.image.load(background)
            self.apply_context()


    def apply_context(self):
        self.interactables = interactables_dict.get(self.context)
        self.objects = self.objectDict.get(self.context)
        self.objectAni.set_tuple(self.context)

    # Technically speaking this should be null checked
    # However, you shouldn't be able to save in an invalid place to begin with
    def change_context(self, context):
        self.context = context
        self.screen = game.image.load(background_dict.get(self.context))  # Draws the screen based on the new context
        self.apply_context()  # Applies the current context to reload the other things on screen

