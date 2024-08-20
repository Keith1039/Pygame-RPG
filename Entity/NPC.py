import pygame as game
import os

class NPC(game.sprite.Sprite):

    def __init__(self, jsonInfo):
        super().__init__()
        # unpack the JSON data
        self.Name = jsonInfo["Name"]
        self.Sprite = jsonInfo["Sprite"]
        self.Scale = tuple(jsonInfo["Scale"])
        self.Dialogue = jsonInfo["Dialogue"]
        self.Context = jsonInfo["Context"]
        self.Pos = tuple(jsonInfo["Pos"])
        self.aniStatus = "Idle"  # set the animation status
        self.aniTracker = 0  # initialize the tracker
        self.maxAniVal = self.get_max_animation_val()  # set the max animation value
        self.image = None
        self.rect = None
        self.set_image_and_rect()  # set the image and rect variables

    def get_max_animation_val(self):
        # gets the maximum number for the animation in use
        fileList = os.listdir(self.Sprite)  # get the list of files in the given sprite directory
        referenceString = self.Name + "_" + self.aniStatus + "_"  # what we use to match
        matchingFiles = []  # a list of all the file names that match the reference string
        for fileName in fileList:  # loop through the file names
            if referenceString in fileName:  # if the name matches the reference string, add it to the list
                matchingFiles.append(fileName)
        matchingFiles.sort(key=sort_func)  # sort the list
        final = matchingFiles.pop()  # get the last item in the sortest list (the biggest)
        final = final.replace(".png", "")  # get rid of the png portion of the file name
        finalNum = int(final.split("_").pop())  # get the maximum number
        return finalNum

    # simplified set_image_and_rect function for the NPC class
    def set_image_and_rect(self):
        filePath = self.Sprite + self.Name + "_" + self.aniStatus + "_" + str((self.aniTracker // 10) + 1) + ".png"
        self.image = game.image.load(filePath)  # load the new image
        self.image = game.transform.scale(self.image, self.Scale)  # scale the image to a set value
        self.rect = self.image.get_rect()  # get the new
        self.rect.center = self.Pos  # set the new pos

    # simpler version of the Entity update function
    def update(self):
        self.aniTracker += 1  # increment the tracker
        if self.aniTracker % 10 == 0:  # every 10 frames we shift the animation
            if (self.aniTracker // 10) + 1 > self.maxAniVal:
                self.aniTracker = 0  # reset animation timer
            self.set_image_and_rect()  # if the above condition is triggered we know an update is going to happen

    def add_event_keys(self, events):
        self.Dialogue += events  # add the events to the NPCs dialogue queue

    def get_event_key(self):
        if len(self.Dialogue) > 0:
            return self.Dialogue.pop(0)  # remove and return the first item in the queue
        else:
            # return the genericDialogue if there's no normal dialogue
            return "genericDialogue"


def sort_func(e):  # same sort function
    final = e.replace(".png", "")  # get rid of the png portion of the file name
    return int(final.split("_").pop())  # get the maximum number
