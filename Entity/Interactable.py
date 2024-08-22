import pygame as game
import Utils

class Interactable(game.sprite.Sprite):

    def __init__(self):
        super().__init__()  # initiate the sprite class
        self.Name = ""
        self.Sprite = ""
        self.aniStatus = "Idle"
        self.genericKey = ""
        self.Scale = ()
        self.Flipped = False
        self.Context = ""
        self.Pos = ()
        self.Events = []
        self.aniTracker = 0
        self.maxAniVal = 0
        self.image = None
        self.rect = None

    # meant to be overwritten by child classes
    def get_updated_data(self):
        return {}

    # meant to be overwritten by child classes
    def process_special_criteria(self):
        # returns a boolean for the update value
        return False

    # meant to be overwritten by child classes
    def is_colliding(self, knight):
        return False

    # meant to be overwritten by child classes
    def process_collision(self):
        pass

    # what the get_max_ani_val() function is actually going to do
    def super_get_max_ani_val(self, name):
        return Utils.get_max_animation_val(self.Sprite, name, self.aniStatus)

    # what the
    def set_image_and_rect(self, name):
        spot = str((self.aniTracker // 10) + 1)  # the frame of the animation
        if self.aniTracker == -1:  # check if we have a -1
            spot = str(self.maxAniVal)  # set the spot to the max
        filePath = self.Sprite + name + "_" + self.aniStatus + "_" + spot + ".png"  # create the file path
        self.image = game.image.load(filePath)  # load the new image
        self.image = game.transform.scale(self.image, self.Scale)  # scale the image to a set value
        if self.Flipped:  # check if the image is supposed to be flipped
            self.image = game.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()  # get the new
        self.rect.center = self.Pos  # set the new pos

    # what the update function of the child class is actually going to do
    def super_update(self, name, force):
        if self.aniTracker != -1:  # -1 indicates that it can't change
            self.aniTracker += 1  # increment the tracker
        if self.aniTracker % 10 == 0 or force:  # every 10 frames we shift the animation or when we force it
            update = False  # flag for when we should update the image and rect
            if (self.aniTracker // 10) + 1 > self.maxAniVal and self.process_special_criteria():
                self.aniTracker = -1  # make it stuck on the final animation
            elif (self.aniTracker // 10) + 1 > self.maxAniVal:
                self.aniTracker = 0  # reset animation timer
                update = True  # we need to update the sprite
            elif (self.aniTracker // 10) + 1 <= self.maxAniVal:
                update = True  # we need to update the animation
            if update:
                # if the above conditions are triggered we know an update is going to happen
                self.set_image_and_rect(name)

    def add_event_keys(self, events):
        self.Events += events  # add the events to the interactable's dialogue queue

    def get_event_key(self):
        if len(self.Events) > 0:
            return self.Events.pop(0)  # remove and return the first item in the queue
        else:
            # return a key to generic dialogue
            return self.genericKey
