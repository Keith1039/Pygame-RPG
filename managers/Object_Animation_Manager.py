chestAniR = 4, "Item_Art&Object_Art/Usable/Chest_Opening_R "
chestAniL = 4, "Item_Art&Object_Art/Usable/Chest_Opening_L "

#Could be useful

class ObjectAnimationManager:
    def __init__(self):
        self.aniArray = []

    def set_array(self, context):
        if context == "Background1":
            self.aniArray = chestAniL
    def change_array(self, knight, pos, interactable):
        if pos > interactable[0][0] and pos < interactable[0][1] and interactable[1] == "Chest" and interactable[
            2] == False:
            self.aniArray = chestAniL
            knight.status = "Opening Chest"
            interactable[2] = True
