import Utils
from Entity.NPC import NPC
import pygame as game


class NPCManager:

    def __init__(self, knight):
        self.NPCDict = Utils.get_NPC_dict()  # reference to the dictionary of NPCs
        self.NPCGroup = game.sprite.Group()  # NPC group for the sprites
        self.knight = knight  # reference to the knight object
        #self.eventManager = eventManager  # reference to the event manager

    def create_NPC(self, name):
        # we don't check if the name exists because this is only called from looping through
        # the list of NPCs
        return NPC(self.NPCDict[name])  # return an NPC object

    def save_and_empty(self):
        # saves the changed NPC information and then empties the Sprite Group
        for sprite in self.NPCGroup.sprites():
            if (sprite.aniTracker // 10) + 1 > sprite.maxAniVal:  # check if the aniTracker value is valid
                sprite.update(True)  # force update
            self.NPCDict[sprite.Name]["Dialogue"] = sprite.Dialogue  # update the dialogue list
        self.NPCGroup.empty()  # remove all sprites from the group

    def get_NPCs(self, context):
        self.save_and_empty()
        npcList = []  # a list of NPCs to be added
        for key, NPCDict in self.NPCDict.items():  # loop through the npc dictionary
            NPCContext = NPCDict["Context"]  # get the context for that key
            if NPCContext == context:  # check to see if the context is the same
                npcList.append(key)  # add that key to the list

        for name in npcList:
            npc = self.create_NPC(name)  # create the NPC
            self.NPCGroup.add(npc)  # add the NPC to the group

    def update_NPC(self, name, newEvents):
        for npc in self.NPCGroup.sprites():  # loop through the NPCs in the group
            if npc.Name == name:  # check if the name matches
                npc.add_event_keys(newEvents)  # adds the event to the NPC object

    def get_colliding(self):
        # this is for the symbol that shows that an NPC can be spoken to
        colliding = None  # the sprite that is colliding with the player
        for sprite in self.NPCGroup.sprites():
            if sprite.rect.collidepoint(self.knight.rect.center):  # check if the sprite is colliding
                colliding = sprite  # add the sprite to the list
                break
        return colliding

    def get_interaction_event(self, eventList):
        colliding = self.get_colliding()  # get the NPC the player is colliding with
        if colliding is not None:
            for event in eventList:  # loop through the event list
                if event.type == game.KEYDOWN:
                    if event.key == game.K_UP:  # check if they're pressing the up key
                        return colliding.get_event_key()  # return the event key
        return None  # return nothing
