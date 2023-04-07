from managers.NPC_Animation_Manager import NPCAnimationManager

global npc_Manager
npc_Manager = NPCAnimationManager()

def test_ChangeArray_B1A():
    npc_Manager.context = "Background1"
    npc_Manager.Apply_context()
    assert((len(npc_Manager.ani_array) == 0 and len(npc_Manager.NPCs) == 0))

def test_ChangeArray_B2A():
    npc_Manager.context = "Background2"
    npc_Manager.Apply_context()
    assert((len(npc_Manager.ani_array) == 2 and len(npc_Manager.NPCs) == 1))

