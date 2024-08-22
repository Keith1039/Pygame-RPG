import pygame as game
from Entity.Object import Object
import Utils

class ObjectManager:

    def __init__(self, knight):
        self.objectDict = Utils.get_complete_object_dict()  # gets the complete object dictionary with all the info
        self.objectGroup = game.sprite.Group()  # the group for the objects
        self.knight = knight  # reference to the knight class

    def create_object(self, key):
        # we don't check if the key exists because this is only called from looping through
        # the dictionary
        return Object(self.objectDict[key])  # return the Object type object

    def save_and_empty(self):
        # loop through all the objects in the group
        for object in self.objectGroup.sprites():
            objDict = self.objectDict[object.Name]
            # updates the dictionary key/value pairs for the current object
            if (object.aniTracker // 10) + 1 > object.maxAniVal:  # check if the tracker is invalid
                object.update(True)  # force the sprite info to update
            objDict.update({
                "Events": object.Events,
                "aniStatus": object.aniStatus,
                "aniTracker": object.aniTracker
            })
        self.objectGroup.empty()  # remove all sprites from the group

    def get_objects(self, context):
        self.save_and_empty()  # save the changes and clear the sprites
        objList = []  # a list of objects to be added
        for key, objDict in self.objectDict.items():  # loop through the object dictionary
            objContext = objDict["Context"]  # get the context for that key
            if objContext == context:  # check to see if the context is the same
                objList.append(key)  # add that key to the list

        for name in objList:
            obj = self.create_object(name)  # create the Object type object
            self.objectGroup.add(obj)  # add the object to the group

    def get_colliding(self):
        # this is for the symbol that shows that an object can be interacted with
        colliding = None  # the sprite that is colliding with the player
        for sprite in self.objectGroup.sprites():
            # check to see if the sprite is colliding on the furthest possible part
            if self.knight.rect.collidepoint(sprite.rect.midright):
                colliding = sprite  # add the sprite to the list
                break
        return colliding

    def get_interaction_event(self, eventList):
        colliding = self.get_colliding()  # get the NPC the player is colliding with
        if colliding is not None:
            for event in eventList:  # loop through the event list
                if event.type == game.KEYDOWN:
                    if event.key == game.K_UP:  # check if they're pressing the up key
                        if colliding.ObjectType == "Treasure_Chest":
                            if colliding.aniStatus != "Opening":
                                colliding.aniStatus = "Opening"  # change the animation status
                                colliding.aniTracker = 0  # reset ani tracker
                                colliding.maxAniVal = colliding.get_max_animation_val()  # reset the max animation value
                        return colliding.get_event_key()  # return the event key
        return None  # return nothing

