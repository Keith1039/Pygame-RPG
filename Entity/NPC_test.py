from Entity.NPC import NPC
import Utils

jsonInfo = Utils.get_NPC_dict()
npc = NPC(jsonInfo["testNPC"])


def test_update():
    npc.update()  # update the sprite
    flag = npc.aniTracker == 1  # check if the
    npc.aniTracker = 9  # set it to 1 tick before the change
    # set rect and image to None to see if they'll be reset
    npc.rect = None
    npc.image = None
    npc.update()
    # check if rect and image were set and confirm this happened on the tenth frame
    flag2 = npc.rect is not None and npc.image is not None and npc.aniTracker == 10
    npc.aniTracker = (npc.maxAniVal * 10) + 5  # a number that ISN'T going to trigger the update
    npc.update()  # update the sprite
    flag3 = npc.aniTracker == (npc.maxAniVal * 10) + 6  # check to see if aniTracker was upped
    npc.update(True)  # force the update
    flag4 = npc.aniTracker == 0  # check to see if the tracker was reset
    assert flag and flag2 and flag3 and flag4

