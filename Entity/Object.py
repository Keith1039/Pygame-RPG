from Entity.Interactable import Interactable
import Utils

class Object(Interactable):

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
        self.genericKey = jsonInfo["Generic Dialogue"]
        self.aniTracker = jsonInfo["aniTracker"]  # set the animation tracker
        self.maxAniVal = self.get_max_animation_val()  # set the max animation value
        self.image = None
        self.rect = None
        self.set_image_and_rect(self.ObjectType)  # set the image and rect variables
    def get_updated_data(self):
        # only thing we care about are the events in this case
        return {
            "aniStatus": self.aniStatus,
            "aniTracker": self.aniTracker,
            "Events": self.Events
        }

    def process_special_criteria(self):
        flag = False
        if self.ObjectType == "Treasure_Chest" and self.aniStatus == "Opening":
            flag = True
        return flag

    def is_colliding(self, knight):
        flag = False
        if self.ObjectType == "Treasure_Chest":  # collision detection for Treasure Chests
            flag = knight.rect.collidepoint(self.rect.midright)
        return flag

    def process_collision(self):
        if self.ObjectType == "Treasure_Chest":
            if self.aniStatus != "Opening":
                self.aniStatus = "Opening"  # change the animation status
                self.aniTracker = 0  # reset ani tracker
                self.maxAniVal = self.get_max_animation_val()  # reset the max animation value

    def get_max_animation_val(self):
        return self.super_get_max_ani_val(self.ObjectType)

    def update(self, force=False):
        self.super_update(self.ObjectType, force)
