import pygame as game
from sys import exit
import os
import Entity
import re

from Entity import Knight
from managers.UI_Manager import submenu


def get_unique_animations_from_dir(path):
    animations = os.listdir(path)  # the animations
    uniqueAnimations = []  # list of unique animations
    for animation in animations:
        testAniName = animation.split('_')[1]
        if testAniName not in uniqueAnimations:
            uniqueAnimations.append(testAniName)
    return uniqueAnimations



class MinCursor:
    def __init__(self):
        self.cursor = game.image.load("UI/Cursor.png")

class MinUIManager:
    def __init__(self, uiFont, uiScreen):
        self.UI = "Entity"
        self.cursor = MinCursor()
        self.font = uiFont  # Reference to writing surface that I use in Rpg2.py (no point in making a new one)
        self.screen = uiScreen  # Reference to the screen object from ScreenManager
        self.submenuImage = game.image.load("UI/Battle_UI/sub_menu.png")
        self.infoDict = {
            "Entity": "",
            "Animation": ""
        }
        self.knight = Knight()
        self.displayedEntity = None
        self.entityGroup = game.sprite.Group()  # entity group
        self.subMenu = True
        self.subMenuItems = os.listdir("Entity_Sprites/")
        self.subMenuMinIndex = -1
        self.subMenuMaxIndex = -1
        self.subMenuSlider = -1

    def draw_background(self):
        background = game.image.load("UI/Battle_UI/Temp_Background.png")
        self.screen.blit(background, (100, 550))

    def draw_submenu(self):
        # checks should be done in this function
        # the values aren't properly set
        subsetItems = []
        if self.subMenuSlider == -1 and self.subMenuMaxIndex == -1 and self.subMenuMinIndex == -1:
            subsetItems = self.subMenuItems[0:9]  # get the first 9 items
            self.subMenuMaxIndex = len(subsetItems) - 1
            if self.subMenuMaxIndex >= 0:  # check if the max number is allowable
                self.subMenuSlider = 0
                self.subMenuMinIndex = 0
        else:
            subsetItems = self.subMenuItems[self.subMenuMinIndex: self.subMenuMaxIndex + 1]
        self.screen.blit(self.submenuImage, (350, 550))
        for i in range(len(subsetItems)):
            x_pos = i % 3 * 400 + 450
            y_pos = int(i / 3) * 75 + 600
            self.screen.blit(self.font.render(subsetItems[i], False, "Black"), (x_pos, y_pos))

    # Function that handles the position of the cursor
    def handle_cursor(self, keys):
        result = None, None
        oldSliderVal = self.subMenuSlider
        flag = self.handle_submenu_input(keys)
        if flag is None:
            # reset values
            if self.UI == "Animation":
                if self.infoDict["Animation"] != "":
                    self.infoDict["Animation"] = ""
                elif self.infoDict["Entity"] != "":
                    self.infoDict["Entity"] = ""
                self.subMenuItems.clear()
                self.subMenuSlider = -1
                self.subMenuMaxIndex = -1
                self.subMenuMinIndex = -1
            result = self.UI + "(S)", None
        elif flag:
            # Append "S" to the UI, so we know this came from a submenu
            item = None
            if len(self.subMenuItems) != 0:
                item = self.subMenuItems[self.subMenuSlider]
            result = self.UI + "(S)", item
        else:
            # check to see if the array is legal to begin with
            if self.subMenuMaxIndex != -1:
                # time to validate slider and the other stuff (simplify expression later)
                if self.subMenuSlider > self.subMenuMaxIndex and int(self.subMenuSlider / 9) <= int(
                        (len(self.subMenuItems) - 1) / 9):
                    # guaranteed to be right by virtue of condition
                    self.subMenuMinIndex = int(self.subMenuSlider / 9) * 9
                    # new max slider index, assuming full row ( 3 x 3, 9 items in total for the screen)
                    self.subMenuMaxIndex = self.subMenuMinIndex + 8
                    # validate theoretical max index
                    if self.subMenuMaxIndex >= len(self.subMenuItems):
                        self.subMenuMaxIndex = len(self.subMenuItems) - 1
                    # correct the slider val
                    if self.subMenuSlider >= len(self.subMenuItems):
                        self.subMenuSlider = len(self.subMenuItems) - 1

                elif self.subMenuMinIndex > self.subMenuSlider > 0:
                    # guaranteed to be right by virtue of the above conditions
                    self.subMenuMaxIndex = self.subMenuMinIndex - 1
                    # new min slider index, assuming full row ( 3 x 3, 9 items in total for the screen)
                    self.subMenuMinIndex = int(self.subMenuSlider / 9) * 9
                    # validate theoretical max index
                    if self.subMenuMaxIndex > len(self.subMenuItems):
                        self.subMenuMaxIndex = len(self.subMenuItems) - 1
                # ensure that slider isn't out of bounds for no reason
                elif self.subMenuSlider > self.subMenuMaxIndex or self.subMenuSlider < self.subMenuMinIndex:
                    self.subMenuSlider = oldSliderVal
            else:
                # reset slider position to a valid one
                self.subMenuSlider = oldSliderVal

            # determining cursor position
            num = (self.subMenuSlider - self.subMenuMinIndex)
            x_pos = num % 3 * 400 + 390
            y_pos = int(num / 3) * 75 + 580
            # drawing cursor
            self.screen.blit(self.cursor.cursor, (x_pos, y_pos))
        return result

    def handle_submenu_input(self, eventList):
        select = False
        for event in eventList:
            if event.type == game.KEYDOWN:
                if event.key == game.K_RETURN:
                    select = True
                    break  # Breaks because this indicates a transition to another screen
                elif event.key == game.K_ESCAPE:
                    select = None
                    break  # Breaks because this indicates a transition to another screen
                if event.key == game.K_RIGHT:
                    self.subMenuSlider += 1
                elif event.key == game.K_LEFT:
                    self.subMenuSlider -= 1
                elif event.key == game.K_DOWN:
                    self.subMenuSlider += 3
                elif event.key == game.K_UP:
                    self.subMenuSlider -= 3
        return select

    # Draws the UI based on current state. Assets are game assets that need to be loaded in for certain UIs
    def draw_UI(self, eventList, assets=None):
        # Function that actually draws what's on screen
        # Assets should be drawn first, so we don't cover up the text
        # title = title_dict.get(self.UI)
        self.draw_background()
        self.entityGroup.update()
        self.entityGroup.draw(self.screen)
        tempFont = game.font.Font('font/Pixeltype.ttf', 100)
        if self.infoDict["Entity"] != "":
            fontRender = tempFont.render(self.infoDict["Entity"], False, "Red")
            self.screen.blit(fontRender, (680, 50))
        self.draw_submenu()
        return self.handle_cursor(eventList)

class MinUIHandler:
    def __init__(self, minUIManager):
        self.entityFactory = Entity.EntityFactory()
        self.minUIManager = minUIManager  # uiManager

    def handle_interaction(self, screen, choice):
        if screen is not None and choice is not None:
            if screen == "Entity(S)":
                self.minUIManager.infoDict["Entity"] = choice
                entityName = self.minUIManager.infoDict["Entity"]
                dirPath = "Entity_Sprites/" + entityName + "/"
                self.minUIManager.subMenuItems = get_unique_animations_from_dir(dirPath)
                self.minUIManager.UI = "Animation"
                if self.minUIManager.infoDict["Entity"] == "Knight":
                    self.minUIManager.displayedEntity = Knight()  # create knight object
                else:
                    self.minUIManager.displayedEntity = self.entityFactory.create_entity(self.minUIManager.infoDict["Entity"])
                self.minUIManager.displayedEntity.x = 711
                self.minUIManager.displayedEntity.y = 550
                self.minUIManager.entityGroup.add(self.minUIManager.displayedEntity)

            elif screen == "Animation(S)":
                self.minUIManager.infoDict["Animation"] = choice  # make the choice
                self.minUIManager.displayedEntity.aniStatus = self.minUIManager.infoDict["Animation"]
                self.minUIManager.displayedEntity.aniTracker = 0  # reset animation
                self.minUIManager.displayedEntity.reset_max_animation_val()
                self.minUIManager.displayedEntity.update(True)

        elif screen is not None and choice is None:
            if screen == "Animation(S)":
                self.minUIManager.UI = "Entity"
                self.minUIManager.infoDict["Animation"] = ""  # clear it
                self.minUIManager.infoDict["Entity"] = ""  # clear it
                self.minUIManager.subMenuItems = os.listdir("Entity_Sprites/")
                self.minUIManager.entityGroup.remove(self.minUIManager.displayedEntity)
                self.minUIManager.displayedEntity = None




# I should have an array of sprite managers and it goes through them
game.init()
screen = game.display.set_mode((1422, 800))
clock = game.time.Clock()
game.display.set_caption("Animation Viewer")
font = game.font.Font('font/Pixeltype.ttf', 50)

# Hero Object
knight = Entity.Knight()

# Think I'll go for the 1422 x 800 route from now on
tempScreen = game.image.load("Background_Art/gothic_chapel_portfolio_1422x800.png")

entities = os.listdir("Entity_Sprites/")

minUIManager = MinUIManager(font, screen)
minUIHandler = MinUIHandler(minUIManager)

while True:

    eventList = game.event.get()
    for event in eventList:
        if event.type == game.QUIT:
            game.quit()
            exit()

    screen.blit(tempScreen, (0, 0))
    context, choice = minUIManager.draw_UI(eventList)
    minUIHandler.handle_interaction(context, choice)
    keys = game.key.get_pressed()

    game.display.update()
    clock.tick(60)