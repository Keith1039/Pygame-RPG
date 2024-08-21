from Entity.NPC_Manager import NPCManager
from Entity.Knight import Knight
import pygame as game

knight = Knight()
npcManager = NPCManager(knight)
npcName = "testNPC"

keys_dict = {"s": game.K_DOWN, "w": game.K_UP, "a": game.K_LEFT, "d": game.K_RIGHT, "enter": game.K_RETURN,
             "esc": game.K_ESCAPE}
def get_keydown_event(key):
    game.event.post(game.event.Event(game.KEYDOWN, key=keys_dict[key]))  # Create keydown event and add to queue
    return game.event.get()  # Get the event queue also removes all events from queue
def test_create_NPC():
    npc = npcManager.create_NPC(npcName)
    className = npc.__class__.__name__
    assert className == "NPC"

def test_get_NPCs():
    npcManager.NPCGroup.add(npcManager.create_NPC(npcName))  # add an NPC to the group
    npcManager.get_NPCs("INVALID")  # pass in a context that doesn't exist
    flag = len(npcManager.NPCGroup.sprites()) == 0  # confirm that the NPC that was in the group was removed
    npcManager.get_NPCs("test")  # pass in a context with NPCs that exist
    flag2 = len(npcManager.NPCGroup.sprites()) == 1
    assert flag and flag2

def test_save_and_empty():
    npc = npcManager.NPCGroup.sprites()[0]
    oldDialogue = npc.Dialogue.copy()  # the old dialogue of the NPC object
    npc.Dialogue = ["newDialogue"]
    npcManager.save_and_empty()  # save and empty the sprite
    #print(npcManager.NPCDict)
    flag = len(npcManager.NPCGroup.sprites()) == 0
    npc = npcManager.create_NPC(npcName)  # creat the new NPC
    npcManager.NPCGroup.add(npc)  # recreate the npc and add it back to the group
    flag2 = npc.Dialogue == ["newDialogue"]   # check the dialogue
    npc.Dialogue = oldDialogue  # set the dialogue back to the old one
    assert flag and flag2


def test_update_NPC():
    npcManager.update_NPC("NONAME", ["stuff", "stuff"])  # try to update an NPC that doesn't exist
    # check to see if no new sprites were added and that the sprite that is in the list doesn't match
    flag = len(npcManager.NPCGroup.sprites()) == 1 and npcManager.NPCGroup.sprites()[0].Name == "testNPC"
    npcManager.update_NPC("testNPC", ["testEvent2", "testEvent3"])
    npc = npcManager.NPCGroup.sprites()[0]  # get the NPC
    flag2 = len(npc.Dialogue) == 3  # we ensure order is maintained on the NPC_test.py file
    assert flag and flag2

def test_get_colliding():
    knight.rect.center = (999, 999)  # put the knight in some random, inaccessible spot
    collidingNPC = npcManager.get_colliding()  # get the colliding NPC
    flag = collidingNPC is None  # confirm that there is nothing colliding with the Knight object
    npc = npcManager.NPCGroup.sprites()[0]  # get the NPC
    knight.rect.center = npc.rect.center  # place the knight at the center of the npc
    collidingNPC = npcManager.get_colliding()  # get the colliding NPC
    flag2 = npc == collidingNPC  # confirm that the npc and the collidingNPC are the same object
    assert flag and flag2

def test_get_interaction_event():
    npc = npcManager.NPCGroup.sprites()[0]  # get the NPC
    npc.Dialogue = ["testEvent"]
    knight.rect.center = (999, 999)  # put the knight in some random, inaccessible spot
    eventKey = npcManager.get_interaction_event(get_keydown_event("s"))  # give the incorrect key and not colliding
    flag = eventKey is None  # confirm that there was no event key returned
    eventKey = npcManager.get_interaction_event(get_keydown_event("w"))  # give the correct key and not colliding
    flag2 = eventKey is None
    knight.rect.center = npc.rect.center  # place the knight at the center of the npc
    eventKey = npcManager.get_interaction_event(get_keydown_event("a"))  # give the incorrect key and we're colliding
    flag3 = eventKey is None
    eventKey = npcManager.get_interaction_event(get_keydown_event("w"))  # give the correct key and we're colliding
    flag4 = eventKey == "testEvent" and len(npc.Dialogue) == 0  # confirm a key was returned and the list shrunk
    eventKey = npcManager.get_interaction_event(get_keydown_event("w"))  # give the correct key and we're colliding
    # confirm that a generic text event key was returned and the dialogue list is still empty
    flag5 = eventKey == "genericDialogue" and len(npc.Dialogue) == 0
    assert flag and flag2 and flag3 and flag4 and flag5

