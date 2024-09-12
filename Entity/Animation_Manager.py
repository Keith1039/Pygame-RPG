import pygame as game
import re
import Utils
import os


schema = {
    "aniStatus": "",
    "alternative": "Attack",
    "frames": None,
    "point": None,
    "flipped": False
}
class AnimationManager:

    def __init__(self, screen):
        self.screen = screen  # screen for animating
        self.active = False  # boolean that tells us if the manager is to be used
        self.spriteGroup = game.sprite.Group()  # the group of sprites getting animated
        self.actor = None  # main entity
        self.targets = []  # a list of entities getting hit or something
        self.others = []  # list of the other entities
        self.actorStartingPos = ()  # position actor starts at
        self.actionQueue = []  # a list of actions the Entities have to do
        self.frameCount = -1  # way we check if the animation manager is active
        self.maxFrameCount = -1  # maximum amount of time before we need to pop from queue
        self.action = {}  # a dictionary that's talking about the action we're doing
        self.slopeEquation = {
            "m": 0,
            "b": 0,
            "Starting Point": (),
            "x_distance": 0
        }
        self.x_increment = 0

    def set_slope_equation(self, startingPoint, endPoint):
        # print(startingPoint, endPoint)
        # slope line equation
        x_diff = endPoint[0] - startingPoint[0]  # difference in the x-axis
        y_diff = endPoint[1] - startingPoint[1]  # difference in the y-axis
        slope = y_diff/x_diff  # the slope of the equation
        b = startingPoint[1] - (slope * startingPoint[0])  # get the y intercept
        self.slopeEquation.update({  # update the equation
            "m": slope,
            "b": b,
            "Starting Point": startingPoint,
            "x_distance": x_diff
        })

    def use_slope_equation(self):
        m = self.slopeEquation["m"]
        b = self.slopeEquation["b"]
        x_distance = self.slopeEquation["x_distance"]
        startingPoint = self.slopeEquation["Starting Point"]
        # check if the equation is set
        properEquation = startingPoint != ()
        if properEquation:
            # find the new x and y values
            self.actor.x = int(startingPoint[0] + (self.frameCount * self.x_increment))  # update x
            self.actor.y = int((self.actor.x * m) + b)  # update y

    def confirm_valid_animation_status(self, sprite, aniStatus):
        flag = False
        fileList = os.listdir(sprite)  # get the list of files
        regexString = r'.*_' + aniStatus + r'_\d+\.png'  # has to be raw strings
        for fileName in fileList:  # loop through file names
            if re.search(regexString, fileName):  # check if there's a match
                flag = True  # set the flag to true
                break  # end loop
        return flag

    def fill_sprite_group(self, entities):
        for entity in entities:
            if entity not in self.spriteGroup.sprites():  # only allow unique entries
                self.spriteGroup.add(entity)  # add the entity

    def change_targets_animation(self, sprites, aniStatus):
        for entity in sprites:
            # confirm that the entity isn't dead and that the animation status given is different
            if entity.aniStatus != "Death" and entity.aniStatus != aniStatus:
                entity.aniTracker = 0  # reset the animation tracker
                entity.flipped = False  # reset flipped
                entity.aniStatus = aniStatus  # change the animation
                entity.reset_max_animation_val()  # reset the max animation for the new animation
                entity.update(True)  # force the sprite to update

    def load_action_queue(self, actionInfo, actor, targets, others):
        self.active = True  # set the active attribute to true
        self.actor = actor  # main actor
        if len(targets) == 1 and targets[0] == actor:
            self.targets = []  # if the target is actor there's no real target
        else:
            self.targets = targets  # set the targets
        self.others = others  # everyone else
        self.fill_sprite_group(others)  # add in the others
        self.fill_sprite_group(targets)  # add in the targets
        self.fill_sprite_group([self.actor])  # add in the actor
        self.actorStartingPos = (self.actor.x, self.actor.y)  # starting position for actor
        attackType = actionInfo.pop("attack type")  # get the type of attack and remove it from the dict
        if attackType != "":  # confirm that there is movement
            runningToDict = {
                "type": "",
                "aniStatus": "Run",
                "alternative": "Idle",
                "flipped": False,
                "point": (self.actor.x, self.actor.y)
            }
            runningBackDict = runningToDict.copy()  # copy the running to dict
            point = ()
            if attackType == "Physical":  # physical attacks go up to one Entity and smack them
                if self.actor.x > targets[0].x:
                    point = (targets[0].x + 100, targets[0].y)
                else:
                    point = (targets[0].x - 100, targets[0].y)

            elif attackType == "Ranged":  # ranged attacks walk up forward and hit people
                point = (self.actor.x + 100, self.actor.y)

            elif attackType == "AOE":
                point = (711, 400)  # some defined midpoint
            runningToDict.update({"point": point})  # update the point key
            self.actionQueue.append(runningToDict)  # add this to the queue
            self.actionQueue.append(actionInfo)  # the actual attack animation
            runningBackDict.update({  # update the running back dict
                "flipped": True,
                "point": self.actorStartingPos
            })
            self.actionQueue.append(runningBackDict)  # add the running back to the queue
        else:
            self.actionQueue.append(actionInfo)  # add the actual attack animation
        self.action = self.actionQueue.pop(0)  # load the first action
        self.apply_new_action()

    def apply_new_action(self):
        # check if the animation we want to set it to is available
        if self.confirm_valid_animation_status(self.actor.Sprite, self.action["aniStatus"]):
            self.actor.aniStatus = self.action["aniStatus"]
        else:
            # if not set it to the generic alternative
            self.actor.aniStatus = self.action["alternative"]
        self.actor.reset_max_animation_val()  # reset the maximum
        self.actor.flipped = self.action["flipped"]  # set the flipped value for entity

        self.frameCount = 0  # set the frameCount to 0
        self.maxFrameCount = self.actor.get_max_animation_val() * 10  # get our limit

        if self.action["point"] is not None:  # check if we're moving to a point
            # if we are, set the slope equation

            self.set_slope_equation((self.actor.x, self.actor.y), self.action["point"])
            self.x_increment = self.slopeEquation["x_distance"] / self.maxFrameCount

        if self.action["type"] == "Attack":  # check if the action is an attack
            # change the animation of all targets to hurt
            self.change_targets_animation(self.targets, "Hurt")

    def partial_reset(self):
        tempList = self.targets + [self.actor]  # a list of all the notable entities
        self.change_targets_animation(tempList, "Idle")  # change the animation for all back to Idle
        self.action = {}  # reset the action dictionary
        # reset the slope equation
        self.slopeEquation = {
            "m": 0,
            "b": 0,
            "Starting Point": (),
            "x_distance": 0
        }
        self.x_increment = 0  # reset the increment

    def reset(self):
        # null check the actor
        tempList = self.targets
        if self.actor is not None:
            tempList = tempList + [self.actor]  # a list of all the notable entities
        self.change_targets_animation(tempList, "Idle")  # change the animation for all back to Idle
        # reset everything essentially
        self.active = False  # boolean that tells us if the manager is to be used
        self.spriteGroup.empty()  # clear all sprites
        self.actor = None  # main entity
        self.targets = []  # a list of entities getting hit or something
        self.others = []  # list of the other entities
        self.actorStartingPos = ()  # position actor starts at
        self.actionQueue = []  # a list of actions the Entities have to do
        self.frameCount = -1  # way we check if the animation manager is active
        self.maxFrameCount = -1  # maximum amount of time before we need to pop from queue
        self.action = {}  # a dictionary that's talking about the action we're doing
        self.slopeEquation = {
            "m": 0,
            "b": 0,
            "Starting Point": (),
            "x_distance": 0
        }
        self.x_increment = 0

    def process_action(self):
        if self.action != {}:  # check if the action dictionary isn't empty
            self.frameCount += 1  # increment the frame counter
            if self.action["point"] is not None:
                self.use_slope_equation()
            self.spriteGroup.update()  # update the sprites
            self.spriteGroup.draw(self.screen)
            # # draw the rectangle behind entities
            # for sprite in self.spriteGroup.sprites():
            #     print(sprite.altName)
            #     print(sprite.rect.center)
            #     print(".....................")
            #     self.screen.set_at(sprite.rect.center, (255, 0, 0))
                #game.draw.rect(self.screen, (255, 0, 0), sprite.rect)
            if self.frameCount == self.maxFrameCount:
                if len(self.actionQueue) > 0: # check if we can load a new action
                    self.partial_reset()  # partially reset things
                    self.action = self.actionQueue.pop(0)  # get the latest action in the queue
                    self.apply_new_action()  # apply the action
                else:
                    self.reset()  # reset everything, this also deactivates the manager
