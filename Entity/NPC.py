from Entity.Interactable import Interactable
import Utils

class NPC(Interactable):

    def __init__(self, jsonInfo):
        super().__init__()
        # unpack the JSON data
        self.Name = jsonInfo["Name"]
        self.Sprite = jsonInfo["Sprite"]
        self.Scale = tuple(jsonInfo["Scale"])
        self.Flipped = jsonInfo["Flipped"]
        self.Events = jsonInfo["Events"]
        self.Context = jsonInfo["Context"]
        self.Pos = tuple(jsonInfo["Pos"])
        self.aniStatus = "Idle"  # set the animation status
        self.genericKey = "genericDialogue"
        self.aniTracker = 0  # initialize the tracker
        self.maxAniVal = self.get_max_animation_val()  # set the max animation value
        self.image = None
        self.rect = None
        self.set_image_and_rect(self.Name)  # set the image and rect variables

    def get_updated_data(self):
        # only thing we care about are the events in this case
        return {"Events": self.Events}

    def is_colliding(self, knight):
        return self.rect.collidepoint(knight.rect.center)

    def get_max_animation_val(self):
        return self.super_get_max_ani_val(self.Name)  # uses the parent class max_ani_val method

    # simpler version of the Entity update function
    def update(self, force=False):
        self.super_update(self.Name, force)

