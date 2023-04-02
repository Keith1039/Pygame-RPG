from Object_Animation_Manager import ObjectAnimationManager

global objectAnimationManager
objectAnimationManager = ObjectAnimationManager()

# Tests to see if the objectAnimationManager has an empty array upon initialization
def test_init_array():
        assert len(objectAnimationManager.ani_array) == 0

#Test to see if the array required is of an appropriate length
def test_Set_Array():
        objectAnimationManager.Set_Array("Background1")
        assert len(objectAnimationManager.ani_array) == 2
