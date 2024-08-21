import Utils

def test_get_max_animation_val():
    sprite = "Entity_Sprites/Knight/"
    name = "Knight"
    aniStatus = "Idle"
    assert Utils.get_max_animation_val(sprite, name, aniStatus) == 10
