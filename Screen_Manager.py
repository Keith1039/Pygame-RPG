import pygame as game

import Object_Animation_Manager


#Screen manager should draw the actual stuff I guess?

chest_1_1 = [(500, 600), "Chest", False]
class ScreenManager:
    def __init__(self, screen):
        self.context = "Background1"
        self.screen = screen
        self.object_manager = ObjectManager()
        self.Object_Ani = Object_Animation_Manager.Object_Animation_Manager()

    def changeScreen(self, pos):
        if self.context == "Background1" and pos > 900:
            self.context = "Background2"
            self.screen = game.image.load("Background_Art/PNG/game_background_1/game_background_1.png")

        elif self.context == "Background2" and pos < 0:
            self.context = "Background1"
            self.screen = game.image.load("2D_Battle_Art/PNG/Battleground1/Bright/Battleground1.png")

        return self.screen

    def Apply_context(self,):
        interactables = []
        if self.context == "Background1":
            #Need to find a better way to deal with this
            interactables = [chest_1_1]
            self.object_manager.Objects = [(800, 500), True]
            self.Object_Ani.Set_Array(self.context)

        return interactables

class ObjectManager:
    def __init__(self):
        self.Objects = []
