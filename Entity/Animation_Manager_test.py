from Entity.Animation_Manager import AnimationManager
from Entity.Entity_Factory import EntityFactory
from Entity.Move import Move
from Entity.Knight import Knight
import pygame as game
import Utils

game.init()
screen = game.display.set_mode((1422, 800))
factory = EntityFactory()  # Entity manager
moveDict = Utils.get_move_dict()  # move dictionary
animationManager = AnimationManager(screen)  # animation manager

knight = Knight()
knight.x = 500
knight.y = 500
goblin = factory.create_entity("Goblin")  # make a goblin
goblin.x = 431
goblin.y = 500
dummy = factory.create_entity("dummy")  # make a dummy object

def test_set_slope_equation():
    startingPoint = (500, 400)  # start point
    endPoint = (900, 500)  # end point
    animationManager.set_slope_equation(startingPoint, endPoint)  # set the values in the slope equation
    # set values of stuff in the dictionary
    m = animationManager.slopeEquation["m"]
    b = animationManager.slopeEquation["b"]
    x_distance = animationManager.slopeEquation["x_distance"]
    startingPoint2 = animationManager.slopeEquation["Starting Point"]
    # check the variables in the slope dictionary
    flag = m == (1/4) and b == 275 and (endPoint[0] - startingPoint[0]) == x_distance
    flag2 = startingPoint == startingPoint2  # confirm that the two starting points are the same
    assert flag and flag2

def test_use_slope_equation():
    # set the x and y to the starting point
    knight.x = 500
    knight.y = 400
    endPoint = (900, 500)  # point our knight should reach
    animationManager.actor = knight  # set the actor to knight
    animationManager.frameCount = 0  # set the counter to 0
    animationManager.maxFrameCount = 100  # set the maximum
    # set the increment
    animationManager.x_increment = animationManager.slopeEquation["x_distance"] / animationManager.maxFrameCount
    animationManager.use_slope_equation()  # use the slope equation
    # confirm that we get the proper x and y
    flag = knight.x == 500 and knight.y == 400
    animationManager.frameCount = 50  # change the frame count
    animationManager.use_slope_equation()  # use the equation again
    flag2 = knight.x == 700 and knight.y == 450  # confirm that the coordinates are correct
    animationManager.frameCount = animationManager.maxFrameCount  # set it to the max
    animationManager.use_slope_equation()  # use the slope equation
    flag3 = (knight.x, knight.y) == endPoint  # confirm that at the max, the end point is reached
    assert flag and flag2 and flag3

def test_confirm_valid_animation_status():
    # check if the "Attack" animation is present in the folder for knight animations
    flag = animationManager.confirm_valid_animation_status(knight.Sprite, "Attack1")
    # check for an invalid animation status
    flag2 = animationManager.confirm_valid_animation_status(knight.Sprite, "ASDASDACJJIABSHD")
    assert flag and not flag2

def test_fill_sprite_group():
    animationManager.fill_sprite_group([knight, goblin])  # add in two sprites
    flag = len(animationManager.spriteGroup.sprites()) == 2  # check if the length works
    animationManager.spriteGroup.empty()  # remove the sprites
    flag2 = len(animationManager.spriteGroup.sprites()) == 0  # check if the sprites were really cleared
    assert flag and flag2

def test_change_animation_target():
    animationManager.change_targets_animation([knight, goblin], "Run")  # change animation to run
    # confirm that the knight object has the right animation status and the right maximum
    flag = knight.aniStatus == "Run" and knight.maxAniVal == 10
    # confirm that the goblin object has the right animation status and the right maximum
    flag2 = goblin.aniStatus == "Run" and goblin.maxAniVal == 6
    knight.aniStatus = "Death"
    knight.reset_max_animation_val()  # reset the max animation
    knight.aniTracker = 50
    goblin.flipped = True  # set the flipped to true
    goblin.aniTracker = 50
    knight.flipped = True  # set the flipped to true
    # try to change the animation status to idle
    animationManager.change_targets_animation([knight, goblin], "Idle")
    # confirm that the knight object is still dead (confirm that flipped stays the same)
    flag3 = knight.aniStatus == "Death" and knight.maxAniVal == 10 and knight.flipped and knight.aniTracker == 50
    # confirm that the goblin's animation changed and the animation tracker was reset
    flag4 = goblin.aniStatus == "Idle" and goblin.maxAniVal == 6 and not goblin.flipped and goblin.aniTracker == 0
    knight.aniStatus = "Idle"  # set the animation manually
    knight.reset_max_animation_val()  # reset the maximum
    assert flag and flag2 and flag3 and flag4

def test_load_action_queue():
    # set up the moves
    rangedMove = Move("Double Slash", knight, moveDict["Double Slash"]).get_action_details()
    nonAttackMove = Move("Defensive Stance", knight, moveDict["Defensive Stance"]).get_action_details()
    physicalMove = Move("Attack", knight, moveDict["Attack"]).get_action_details()
    aoeMove = Move("Spinning Slash", knight, moveDict["Spinning Slash"]).get_action_details()
    # load the ranged move
    animationManager.load_action_queue(rangedMove, knight, [goblin], [dummy])
    # check the actor details
    flag = animationManager.actor == knight and animationManager.actorStartingPos == (knight.x, knight.y)
    # check if the first action in the queue was preloaded
    flag2 = len(animationManager.actionQueue) == 2 and len(animationManager.targets) == 1 \
           and len(animationManager.spriteGroup.sprites()) == 3 and animationManager.action != {}
    animationManager.reset()  # reset everything
    # load the non-attacking move
    animationManager.load_action_queue(nonAttackMove, knight, [knight], [goblin, dummy])
    flag3 = len(animationManager.actionQueue) == 0 \
        and len(animationManager.targets) == 0 and len(animationManager.spriteGroup.sprites()) == 3 \
        and animationManager.action != {}
    animationManager.reset()  # reset everything
    animationManager.load_action_queue(physicalMove, goblin, [knight], [dummy])
    flag4 = animationManager.actor == goblin and animationManager.actorStartingPos == (goblin.x, goblin.y)
    flag5 = len(animationManager.actionQueue) == 2 and len(animationManager.targets) == 1 \
           and len(animationManager.spriteGroup.sprites()) == 3 and animationManager.action != {}
    animationManager.reset()  # reset everything
    animationManager.load_action_queue(aoeMove, knight, [goblin], [dummy])
    flag6 = len(animationManager.actionQueue) == 2 and len(animationManager.targets) == 1 \
           and len(animationManager.spriteGroup.sprites()) == 3 and animationManager.action != {}
    animationManager.reset()  # reset everything
    assert flag and flag2 and flag3 and flag4 and flag5 and flag6

def test_apply_new_action():
    # set x and y coords for knight
    knight.x = 500
    knight.y = 400
    moveAction = {
            "type": "",
            "aniStatus": "Run",
            "alternative": "Idle",
            "flipped": True,
            "point": (900, 500)
        }

    # an action that doesn't have a valid aniStatus
    invalidAttackAction = {
            "type": "Attack",
            "aniStatus": "ASDFLKNAJFKA",
            "alternative": "Attack1",
            "flipped": False,
            "point": None
        }
    animationManager.actor = knight  # set the actor to the knight object
    animationManager.action = moveAction  # set the action
    animationManager.apply_new_action()  # apply the action
    # confirm that the animation information for Knight has been updated
    flag = knight.aniStatus == "Run" and knight.maxAniVal == 10 and knight.flipped
    slopeDict = animationManager.slopeEquation  # reference to the dict
    # confirm slope information
    flag2 = slopeDict["m"] == (1/4) and slopeDict["b"] == 275 and slopeDict["x_distance"] == 400 and \
        slopeDict["Starting Point"] == (500, 400)
    animationManager.reset()  # rest the manager
    animationManager.actor = knight  # set the actor to the knight object
    animationManager.targets = [goblin]  # set the target to goblin
    animationManager.action = invalidAttackAction  # set the action
    animationManager.apply_new_action()  # apply the action
    # confirm that the knight's status became the alternative
    flag3 = knight.aniStatus == "Attack1" and knight.maxAniVal == 4 and not knight.flipped
    flag4 = goblin.aniStatus == "Hurt" and goblin.maxAniVal == 3
    assert flag and flag2 and flag3 and flag4
