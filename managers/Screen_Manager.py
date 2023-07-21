import pygame as game

from managers.Object_Animation_Manager import ObjectAnimationManager

class Event:
    def __init__(self, pos, eventType, path=""):
        self.range = pos
        self.eventType = eventType
        self.activated = False
        self.path = path

#Screen manager should draw the actual stuff I guess?
chestB1 = Event((500, 600), "Chest")
# For now there's only going to be two options moving to the left screen and moving to the right screen
# Moving to right screen = 1
# Moving to left screen = -1
screen_dict = {("Background1", 1): "Background2", ("Background2", -1): "Background1"}
background_dict ={"Background1": "2D_Battle_Art/PNG/Battleground1/Bright/Battleground1.png",
                  "Background2": "Background_Art/PNG/game_background_1/game_background_1.png"}
interactables_dict = {"Background1": (chestB1, ), "Background2": ()}
objects_dict = {"Background1": ((800, 500), True), "Background2": ()}
class ScreenManager:
    def __init__(self, screen):
        self.interactables = ()
        self.context = "Background1"
        self.screen = screen
        self.objects = ()
        self.objectAni = ObjectAnimationManager()
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
        # Basically if there's not a map to the right don't let the players go right
        if background is None:
            self.context = prevContext
        self.screen = game.image.load(background)
        self.apply_context()

    def apply_context(self):
        self.interactables = interactables_dict.get(self.context)
        self.objects = objects_dict.get(self.context)
        self.objectAni.set_tuple(self.context)


# Unnecessary class. I don't know what I was up to when I made this but for now it's useless
# class ObjectManager:
#     def __init__(self):
#         self.objects = ()
