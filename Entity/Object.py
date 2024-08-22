import pygame as game
import Utils

class Object(game.sprite.Sprite):

    def __init__(self, jsonInfo):
        super().__init__()
        # the object manager adds the extra keys in
        self.Name = jsonInfo["Name"]
        self.ObjectType = jsonInfo["Object Type"]
        self.Sprite = jsonInfo["Sprite"]
        self.Scale = tuple(jsonInfo["Scale"])  # turn it into a tuple
        self.Flipped = jsonInfo["Flipped"]
        self.Context = jsonInfo["Context"]
        self.Pos = tuple(jsonInfo["Pos"])  # turn this into a tuple as well
        self.Events = jsonInfo["Events"]
        self.aniStatus = jsonInfo["aniStatus"]  # set the animation status
        self.aniTracker = jsonInfo["aniTracker"]  # set the animation tracker
        self.maxAniVal = self.get_max_animation_val()  # set the max animation value
        self.image = None
        self.rect = None
        self.set_image_and_rect()  # set the image and rect variables

    def get_max_animation_val(self):
        return Utils.get_max_animation_val(self.Sprite, self.ObjectType, self.aniStatus)

    def set_image_and_rect(self):
        spot = str((self.aniTracker // 10) + 1)  # the frame of the animation
        if self.aniTracker == -1:  # check if we have a -1
            spot = str(self.maxAniVal)  # set the spot to the max
        filePath = self.Sprite + self.ObjectType + "_" + self.aniStatus + "_" + spot + ".png"  # create the file path
        self.image = game.image.load(filePath)  # load the new image
        self.image = game.transform.scale(self.image, self.Scale)  # scale the image to a set value
        if self.Flipped:  # check if the image is supposed to be flipped
            self.image = game.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()  # get the new
        self.rect.center = self.Pos  # set the new pos

    def update(self, force=False):
        if self.aniTracker != -1:  # -1 indicates that it can't change
            self.aniTracker += 1  # increment the tracker
        if self.aniTracker % 10 == 0 or force:  # every 10 frames we shift the animation or when we force it
            update = False  # flag for when we should update the image and rect
            if (self.aniTracker // 10) + 1 > self.maxAniVal and self.aniStatus == "Opening":
                self.aniTracker = -1  # make it stuck on the final animation
            elif (self.aniTracker // 10) + 1 > self.maxAniVal:
                self.aniTracker = 0  # reset animation timer
                update = True  # we need to update the sprite
            elif (self.aniTracker // 10) + 1 <= self.maxAniVal:
                update = True  # we need to update the animation
            if update:
                self.set_image_and_rect()  # if the above condition is triggered we know an update is going to happen

    def get_event_key(self):
        if len(self.Events) > 0:
            return self.Events.pop(0)
        else:
            # set of conditions depending on the object
            key = ""
            if self.ObjectType == "Treasure_Chest":
                key = "chestEmpty"
            return key
