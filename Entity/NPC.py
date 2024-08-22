import pygame as game
import Utils

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
        return Utils.get_max_animation_val(self.Sprite, self.Name, self.aniStatus)  # return the utils function

    # simplified set_image_and_rect function for the NPC class
    def set_image_and_rect(self):
        filePath = self.Sprite + self.Name + "_" + self.aniStatus + "_" + str((self.aniTracker // 10) + 1) + ".png"
        self.image = game.image.load(filePath)  # load the new image
        self.image = game.transform.scale(self.image, self.Scale)  # scale the image to a set value
        self.rect = self.image.get_rect()  # get the new
        self.rect.center = self.Pos  # set the new pos

    # simpler version of the Entity update function
    def update(self, force=False):
        self.aniTracker += 1  # increment the tracker
        if self.aniTracker % 10 == 0 or force:  # every 10 frames we shift the animation or when we force it
            update = False
            if (self.aniTracker // 10) + 1 > self.maxAniVal:
                self.aniTracker = 0  # reset animation timer
                update = True  # indicate that an update is needed
            elif (self.aniTracker // 10) + 1 <= self.maxAniVal:
                update = True  # indicate that an update is needed
            if update:  # check if we need to update
                self.set_image_and_rect()  # if the above condition is triggered we know an update is going to happen

    def add_event_keys(self, events):
        self.Dialogue += events  # add the events to the NPCs dialogue queue

    def get_event_key(self):
        if len(self.Dialogue) > 0:
            return self.Dialogue.pop(0)  # remove and return the first item in the queue
        else:
            # return the genericDialogue if there's no normal dialogue
            return "genericDialogue"
