import json

# ObjectAnimationManager's implementation needs to be redone to allow for multiple objects to be
# present on screen.
chestAniL = (4, "Item_Art&Object_Art/Usable/Chest_Opening_L ")
jsonInfo = json.load(open("JSON/Dictionaries/ObjectAnimationManager.json"))
object_ani_dict = jsonInfo.get("object_ani_dict")

class ObjectAnimationManager:
    def __init__(self):
        self.aniTuple = ()

    def set_tuple(self, context):
        if context == "Background1":
            self.aniTuple = chestAniL

    def change_tuple(self, knight, pos, interactable):
        within_range = pos > interactable.range[0] and pos < interactable.range[1]
        if within_range and not interactable.activated:
            self.aniTuple = object_ani_dict.get(interactable.eventType)
            knight.Status = "Opening Chest"
            interactable.activated = True
