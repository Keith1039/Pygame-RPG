import pygame as game
from Entity.Interactable import Interactable

class InteractableManager():

    def __init__(self, knight):
        self.interactableDict = {}
        self.interactableGroup = game.sprite.Group()  # the group of interactables
        self.knight = knight  # reference to the knight object

    def update_interactable(self, name, newEvents):  # update an interactable
        for npc in self.interactableGroup.sprites():  # loop through the NPCs in the group
            if npc.Name == name:  # check if the name matches
                npc.add_event_keys(newEvents)  # adds the event to the NPC object

    def save_and_empty(self):
        # saves the changed NPC information and then empties the Sprite Group
        for sprite in self.interactableGroup.sprites():
            if (sprite.aniTracker // 10) + 1 > sprite.maxAniVal:  # check if the aniTracker value is valid
                sprite.update(True)  # force update
            interactableDict = self.interactableDict[sprite.Name]  # get the dict for the interactable
            updateDict = sprite.get_updated_data()  # gets the updated information as a dictionary from the object
            interactableDict.update(updateDict)
        self.interactableGroup.empty()  # remove all sprites from the group

    def get_colliding(self):
        # this is for the symbol that shows that something can be interacted with
        colliding = None
        for sprite in self.interactableGroup.sprites():
            if sprite.is_colliding(self.knight):
                colliding = sprite  # set colliding to sprite
                break
        return colliding

    def get_interaction_event(self, eventList):
        colliding = self.get_colliding()  # get the NPC the player is colliding with
        if colliding is not None:
            for event in eventList:  # loop through the event list
                if event.type == game.KEYDOWN:
                    if event.key == game.K_UP:  # check if they're pressing the up key
                        colliding.process_collision()  # process the collision for the sprite
                        return colliding.get_event_key()  # return the event key
        return None  # return nothing
