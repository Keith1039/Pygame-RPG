from managers.Object_Animation_Manager import ObjectAnimationManager
from Entity.Knight import Knight

objectAnimationManager = ObjectAnimationManager()
chestAniL = (4, "Item_Art&Object_Art/Usable/Chest_Opening_L ")

# Tests to see if the objectAnimationManager has an empty array upon initialization
def test_init_array():
        assert len(objectAnimationManager.aniTuple) == 0

# Test to see if the array required is of an appropriate length
def test_set_Array():
        objectAnimationManager.set_tuple("Background1")
        assert objectAnimationManager.aniTuple == chestAniL

def test_change_tuple():
        knight = Knight()
        mockJson = {"Range": (500, 600), "Event Type": "Chest", "Activated": False}  # minimum viable Event JSON
        pos = 550
        # Clearing the tuple
        objectAnimationManager.aniTuple = ()
        objectAnimationManager.change_tuple(knight, pos, mockJson)
        assert tuple(objectAnimationManager.aniTuple) == chestAniL and knight.fieldStatus == "Opening Chest"



