import Utils
from Entity.NPC import NPC
from Entity.Interactable_Manager import InteractableManager
import pygame as game


class NPCManager(InteractableManager):

    def __init__(self, knight):
        super().__init__(knight)  # gets us a reference to the knight object
        self.interactableDict = Utils.get_NPC_dict()  # reference to the dictionary of NPCs
        self.interactableGroup = game.sprite.Group()  # NPC group for the sprites

    def create_NPC(self, name):
        # we don't check if the name exists because this is only called from looping through
        # the list of NPCs
        return NPC(self.interactableDict[name])  # return an NPC object

    def get_NPCs(self, context):
        self.save_and_empty()
        npcList = []  # a list of NPCs to be added
        for key, NPCDict in self.interactableDict.items():  # loop through the npc dictionary
            NPCContext = NPCDict["Context"]  # get the context for that key
            if NPCContext == context:  # check to see if the context is the same
                npcList.append(key)  # add that key to the list

        for name in npcList:
            npc = self.create_NPC(name)  # create the NPC
            self.interactableGroup.add(npc)  # add the NPC to the group
