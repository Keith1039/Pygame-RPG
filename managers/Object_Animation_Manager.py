Chest_Ani_R = 4, "Item_Art&Object_Art/Usable/Chest_Opening_R "
Chest_Ani_L = 4, "Item_Art&Object_Art/Usable/Chest_Opening_L "

#Could be useful

class ObjectAnimationManager:
    def __init__(self):
        self.ani_array = []

    def Set_Array(self, context):
        if context == "Background1":
            self.ani_array = Chest_Ani_L
    def Change_array(self, knight, pos, interactable):
        if pos > interactable[0][0] and pos < interactable[0][1] and interactable[1] == "Chest" and interactable[
            2] == False:
            self.ani_array = Chest_Ani_L
            knight.status = "Opening Chest"
            interactable[2] = True
