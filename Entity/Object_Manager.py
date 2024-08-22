import pygame as game
from Entity.Object import Object
from Entity.Interactable_Manager import InteractableManager
import Utils

class ObjectManager(InteractableManager):

    def __init__(self, knight):
        super().__init__(knight)  # gets us a reference to the knight object
        self.interactableDict = Utils.get_complete_object_dict()  # gets the complete object dictionary with all the info
        self.interactableGroup = game.sprite.Group()  # the group for the objects


    def create_object(self, key):
        # we don't check if the key exists because this is only called from looping through
        # the dictionary
        return Object(self.interactableDict[key])  # return the Object type object

    def get_objects(self, context):
        self.save_and_empty()  # save the changes and clear the sprites
        objList = []  # a list of objects to be added
        for key, objDict in self.interactableDict.items():  # loop through the object dictionary
            objContext = objDict["Context"]  # get the context for that key
            if objContext == context:  # check to see if the context is the same
                objList.append(key)  # add that key to the list

        for name in objList:
            obj = self.create_object(name)  # create the Object type object
            self.interactableGroup.add(obj)  # add the object to the group


