from Entity.Object import Object
import Utils

objectDict = Utils.get_complete_object_dict()
obj = Object(objectDict["testObject"])

def test_update():
    obj.update()  # update the sprite
    flag = obj.aniTracker == 1  # check to see if it updated
    obj.aniTracker = obj.maxAniVal * 10 + 9  # set it to hit the interval next update
    obj.image = None
    obj.rect = None
    obj.update()  # update the sprite
    # check to see if the image and sprite were updated
    flag2 = obj.aniTracker == 0 and obj.image is not None and obj.rect is not None
    obj.aniStatus = "Opening"  # change the status
    obj.maxAniVal = obj.get_max_animation_val()  # reset the maximum animation value
    obj.aniTracker = obj.maxAniVal * 10 + 5
    obj.update()  # update the sprite
    # tracker got updated but the condition didn't trigger (not in interval)
    flag3 = obj.aniTracker = obj.maxAniVal * 10 + 6  # check if the tracker just updated normally
    obj.update(True)  # force the update
    # treasure chest specific attribute
    flag4 = obj.aniTracker == -1  # should be stuck on this
    obj.update()  # try to update the aniTracker variable
    flag5 = obj.aniTracker == -1
    assert flag and flag2 and flag3 and flag4 and flag5

def test_get_event_key():
    key = obj.get_event_key()
    flag = key == "testEvent" and len(obj.Events) == 0  # check to see if the real key was returned and it was removed
    # check to see if the generic event was returned (treasure chest specific)
    flag2 = obj.get_event_key() == "chestEmpty" and len(obj.Events) == 0
    assert flag and flag2


