from Entity.Object import Object
import Utils

objectDict = Utils.get_complete_object_dict()
obj = Object(objectDict["testObject"])

def test_update():
    obj.update()  # update the sprite
    flag = obj.aniTracker == 1
    obj.aniTracker = obj.maxAniVal * 10 + 9
    obj.update()  # update the sprite
    flag2 = obj.aniTracker == 0  # see if the tracker reset
    obj.aniStatus = "Opening"  # change the status
    obj.maxAniVal = obj.get_max_animation_val()  # reset the maximum animation value
    obj.aniTracker = obj.maxAniVal * 10 + 9
    obj.update()  # update the sprite
    # treasure chest specific attribute
    flag3 = obj.aniTracker == obj.maxAniVal * 10 - 10  # should be stuck on this
    assert flag and flag2 and flag3

def test_get_event_key():
    key = obj.get_event_key()
    flag = key == "testEvent" and len(obj.Events) == 0  # check to see if the real key was returned and it was removed
    # check to see if the generic event was returned (treasure chest specific)
    flag2 = obj.get_event_key() == "chestEmpty" and len(obj.Events) == 0
    assert flag and flag2


