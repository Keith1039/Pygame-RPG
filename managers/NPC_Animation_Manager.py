ShopKeepAni = (18, "NPC_Sprites/ShopKeep_idle ")

NPC_tuple_dict = {"Background1": (), "Background2": ("ShopKeep",)}
NPC_ani_tuple_dict = {"ShopKeep": ShopKeepAni}
class NPCAnimationManager:
    def __init__(self):
        self.NPCs = ()
        self.aniTuple = ()

    def apply_context(self, context):
        self.NPCs = NPC_tuple_dict.get(context)

    def change_tuple(self, name):
        self.aniTuple = NPC_ani_tuple_dict.get(name)





