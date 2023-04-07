ShopKeep_Ani = 18, "NPC_Sprites/ShopKeep_idle "


class NPCAnimationManager:
    def __init__(self):
        self.context = ""
        self.NPCs = []
        self.ani_array = []

    def Change_array(self, name):
        if name == "ShopKeep":
            self.ani_array = ShopKeep_Ani

    def Apply_context(self):
        if self.context == "Background1":
            self.NPCs = []
        elif self.context == "Background2":
            self.NPCs = ["ShopKeep"]
            self.Change_array("ShopKeep")


