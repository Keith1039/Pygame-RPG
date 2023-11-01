import pygame as game
import json
from managers.Object_Animation_Manager import ObjectAnimationManager

class Event:

    def __init__(self, eventInfo):
        self.range = eventInfo.get("range")
        self.eventType = eventInfo.get("eventType")  # Can't be None
        self.activated = eventInfo.get("activated")  # Can't be None
        self.path = eventInfo.get("path")

    def load(self, infoDict):
        self.range = tuple(infoDict["range"])
        self.eventType = infoDict["eventType"]
        self.activated = infoDict["activated"]
        self.path = infoDict["path"]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

def initiate_variables():
    # Function that pulls JSON information to create dictionaries
    file = open("JSON/Dictionaries/ScreenManager.json", "r")  # Opens the file
    screenManagerInfo = json.load(file)  # Load JSON information
    i_dict = screenManagerInfo["interactables_dict"]  # interactables_dict information
    temp_dict = {}
    for key in i_dict:  # Go through the array and turn the event dictionary information into Event objects
        temp_array = []
        for eventInfo in i_dict[key]:
            temp_array.append(Event(eventInfo))
        temp_dict.update({key: tuple(temp_array)})
    file.close()
    return screenManagerInfo["background_dict"], temp_dict, screenManagerInfo["objects_dict"]  # Return the values

screen_dict = {("Background1", 1): "Background2", ("Background2", -1): "Background1"}  # For now this can't be JSONED
background_dict, interactables_dict, objects_dict = initiate_variables()
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

    # Screen manager should draw the actual stuff I guess?
    # For now there's only going to be two options moving to the left screen and moving to the right screen
    # Moving to right screen = 1
    # Moving to left screen = -1
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

