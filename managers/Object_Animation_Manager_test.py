from managers.Object_Animation_Manager import ObjectAnimationManager
from managers.Screen_Manager import Event
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
        mockJson = {"range": (500, 600), "eventType": "Chest"}
        interactable = Event(mockJson)
        pos = 550
        # Clearing the tuple
        objectAnimationManager.aniTuple = ()
        objectAnimationManager.change_tuple(knight, pos, interactable)
        assert tuple(objectAnimationManager.aniTuple) == chestAniL and knight.Status == "Opening Chest"



