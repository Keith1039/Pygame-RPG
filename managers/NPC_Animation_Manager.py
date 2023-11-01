import json

jsonInfo = json.load(open("JSON/Dictionaries/NPCAnimationManager.json"))
NPC_tuple_dict = jsonInfo.get("NPC_tuple_dict")
NPC_ani_tuple_dict = jsonInfo.get("NPC_ani_tuple_dict")
class NPCAnimationManager:
    def __init__(self):
        self.NPCs = ()
        self.aniTuple = ()

    def apply_context(self, context):
        self.NPCs = NPC_tuple_dict.get(context)

    def change_tuple(self, name):
        self.aniTuple = NPC_ani_tuple_dict.get(name)





