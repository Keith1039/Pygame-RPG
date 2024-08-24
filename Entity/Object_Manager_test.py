from Entity.Object_Manager import ObjectManager
from Entity.Knight import Knight
import pygame as game

knight = Knight()
objectManager = ObjectManager(knight)
keys_dict = {"s": game.K_DOWN, "w": game.K_UP, "a": game.K_LEFT, "d": game.K_RIGHT, "enter": game.K_RETURN,
             "esc": game.K_ESCAPE}
def get_keydown_event(key):
    game.event.post(game.event.Event(game.KEYDOWN, key=keys_dict[key]))  # Create keydown event and add to queue
    return game.event.get()  # Get the event queue also removes all events from queue

def test_create_object():
    obj = objectManager.create_object("testObject")  # create a test object
    className = obj.__class__.__name__
    assert className == "Object"

def test_save_and_empty():
    obj = objectManager.create_object("testObject")  # create a test object
    obj.Events = []  # set it to an empty list
    # make it so that it's past the limit but doesn't trigger the interval normally
    obj.aniTracker = obj.maxAniVal * 10 + 1
    objectManager.interactableGroup.add(obj)  # add the object to the group
    objectManager.save_and_empty()  # save and empty the changes
    obj = objectManager.create_object("testObject")  # create a test object
    # aniTracker is 0 because it isn't opening, otherwise it would be -1
    assert obj.Events == [] and obj.aniTracker == 0  # check to see if the changes stayed

def test_get_objects():
    objectManager.get_objects("INVALID")  # give in a context that makes no sense
    flag = len(objectManager.interactableGroup.sprites()) == 0  # check if the list is empty
    objectManager.get_objects("test")  # pass in a context that does work
    flag2 = len(objectManager.interactableGroup.sprites()) == 1  # check to see if the list grew
    assert flag and flag2

def test_get_colliding():
    obj = objectManager.interactableGroup.sprites()[0]  # get the object in the group
    obj.rect.center = (999, 999)  # put the sprite in some random corner
    colliding = objectManager.get_colliding()  # check to see if knight is colliding with anything
    flag = colliding is None  # confirm that the returned value was none (knight isn't colliding)
    obj.rect.center = knight.rect.center  # set the object at the middle of the knight rect
    colliding = objectManager.get_colliding()  # check if knight is colliding with anything
    flag2 = colliding == obj
    assert flag and flag2

def test_get_interaction_event():
    obj = objectManager.interactableGroup.sprites()[0]  # get the object
    obj.Events = ["testEvent2"]
    knight.rect.center = (999, 999)  # put the knight in some random, inaccessible spot
    eventKey = objectManager.get_interaction_event(get_keydown_event("s"))  # give the incorrect key and not colliding
    flag = eventKey is None  # confirm that there was no event key returned
    eventKey = objectManager.get_interaction_event(get_keydown_event("w"))  # give the correct key and not colliding
    flag2 = eventKey is None
    knight.rect.center = obj.rect.center  # place the knight at the center of the object
    eventKey = objectManager.get_interaction_event(get_keydown_event("a"))  # give the incorrect key and we're colliding
    flag3 = eventKey is None
    eventKey = objectManager.get_interaction_event(get_keydown_event("w"))  # give the correct key and we're colliding
    flag4 = eventKey == "testEvent2" and len(obj.Events) == 0  # confirm a key was returned and the list shrunk
    eventKey = objectManager.get_interaction_event(get_keydown_event("w"))  # give the correct key and we're colliding
    # confirm that a generic event key was returned and the event list is still empty
    # also confirm that the animation has changed and the max animation val has changed alongside it
    flag5 = eventKey == "chestEmpty" and len(obj.Events) == 0 and obj.aniStatus == "Opening" and \
        obj.maxAniVal == 4
    assert flag and flag2 and flag3 and flag4 and flag5
