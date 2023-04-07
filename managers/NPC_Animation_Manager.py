ShopKeep_Ani = 18, "NPC_Sprites/ShopKeep_idle "


class NPCAnimationManager:
    def __init__(self):
        self.context = ""
        self.NPCs = []
        self.aniArray = []

    def change_array(self, name):
        if name == "ShopKeep":
            self.aniArray = ShopKeep_Ani

    def apply_context(self):
        if self.context == "Background1":
            self.NPCs = []
            
        elif self.context == "Background2":
            self.NPCs = ["ShopKeep"]
            self.change_array("ShopKeep")


