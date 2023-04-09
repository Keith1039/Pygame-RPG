chestAniR = (4, "Item_Art&Object_Art/Usable/Chest_Opening_R ")
chestAniL = (4, "Item_Art&Object_Art/Usable/Chest_Opening_L ")

object_ani_dict = {"Chest": chestAniL}
#Could be useful

class ObjectAnimationManager:
    def __init__(self):
        self.aniTuple = ()

    def set_tuple(self, context):
        if context == "Background1":
            self.aniTuple = chestAniL

    def change_tuple(self, knight, pos, interactable):
        within_range = pos > interactable[0][0] and pos < interactable[0][1]
        print(within_range)
        if within_range and not interactable[2]:
            self.aniTuple = object_ani_dict.get(interactable[1])
            knight.status = "Opening Chest"
            interactable[2] = True
