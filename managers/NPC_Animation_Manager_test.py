from managers.NPC_Animation_Manager import NPCAnimationManager

npcManager = NPCAnimationManager()

def test_change_tuple_B1A():
    npcManager.apply_context("Background1")
    assert((len(npcManager.aniTuple) == 0 and len(npcManager.NPCs) == 0))

def test_change_tuple_B2A():
    npcManager.apply_context("Background2")
    npcManager.change_tuple(npcManager.NPCs[0])
    assert((len(npcManager.aniTuple) == 2 and len(npcManager.NPCs) == 1))

