from managers.NPC_Animation_Manager import NPCAnimationManager

global npc_Manager
npcManager = NPCAnimationManager()

def test_change_array_B1A():
    npcManager.context = "Background1"
    npcManager.apply_context()
    assert((len(npcManager.aniArray) == 0 and len(npcManager.NPCs) == 0))

def test_change_array_B2A():
    npcManager.context = "Background2"
    npcManager.apply_context()
    assert((len(npcManager.aniArray) == 2 and len(npcManager.NPCs) == 1))

