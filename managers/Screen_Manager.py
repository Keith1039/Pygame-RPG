import pygame as game

from managers.Object_Animation_Manager import ObjectAnimationManager


#Screen manager should draw the actual stuff I guess?

chest_1_1 = [(500, 600), "Chest", False]
class ScreenManager:
    def __init__(self, screen):
        self.context = "Background1"
        self.screen = screen
        self.objectManager = ObjectManager()
        self.objectAni = ObjectAnimationManager()

    def change_screen(self, pos):
        if self.context == "Background1" and pos > 900:
            self.context = "Background2"
            self.screen = game.image.load("Background_Art/PNG/game_background_1/game_background_1.png")

        elif self.context == "Background2" and pos < 0:
            self.context = "Background1"
            self.screen = game.image.load("2D_Battle_Art/PNG/Battleground1/Bright/Battleground1.png")
        return self.screen

    def apply_context(self,):
        interactables = []
        if self.context == "Background1":
            #Need to find a better way to deal with this
            interactables = [chest_1_1]
            self.objectManager.objects = [(800, 500), True]
            self.objectAni.set_array(self.context)

        return interactables

class ObjectManager:
    def __init__(self):
        self.objects = []
