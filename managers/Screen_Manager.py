import pygame as game

from managers.Object_Animation_Manager import ObjectAnimationManager


#Screen manager should draw the actual stuff I guess?

chestB1 = [(500, 600), "Chest", False]
# For now there's only going to be two options moving to the left screen and moving to the right screen
# Moving to right screen = 1
# Moving to left screen = -1
screen_dict = {("Background1", 1): "Background2", ("Background2", -1): "Background1"}
background_dict ={"Background1": "2D_Battle_Art/PNG/Battleground1/Bright/Battleground1.png",
                  "Background2": "Background_Art/PNG/game_background_1/game_background_1.png"}
class ScreenManager:
    def __init__(self, screen):
        self.context = "Background1"
        self.screen = screen
        self.objectManager = ObjectManager()
        self.objectAni = ObjectAnimationManager()

    def change_screen(self, pos):
        mover = 0
        if pos > 1000:
            mover = 1
        elif pos < -280:
            mover = -1
        prev_context = self.context
        self.context = screen_dict.get((self.context, mover))
        background = background_dict.get(self.context)
        # Basically if there's not a map to the right don't let the players go right
        if background is None:
            self.context = prev_context
            return self.screen
        self.screen = game.image.load(background)
        return self.screen

    def apply_context(self,):
        interactables = []
        if self.context == "Background1":
            #Need to find a better way to deal with this
            interactables = [chestB1]
            self.objectManager.objects = [(800, 500), True]
            self.objectAni.set_tuple(self.context)
        return interactables

class ObjectManager:
    def __init__(self):
        self.objects = []
