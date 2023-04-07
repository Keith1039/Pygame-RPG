from managers.Object_Animation_Manager import ObjectAnimationManager

objectAnimationManager = ObjectAnimationManager()

# Tests to see if the objectAnimationManager has an empty array upon initialization
def test_init_array():
        assert len(objectAnimationManager.aniArray) == 0

#Test to see if the array required is of an appropriate length
def test_set_Array():
        objectAnimationManager.set_array("Background1")
        assert len(objectAnimationManager.aniArray) == 2
