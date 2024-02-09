import pygame as game
import json
from managers.UI_Manager_draw import *
# File responsible for drawing UI

# example of start screen UI
#
# Name of game
#
# Start Game
# Continue (If a save file is found with SaveManager)
# Load Game (Will just show no save slots if they don't exist)
# Options (Not sure if I'll add this part)

jsonInfo = json.load(open("JSON/Dictionaries/UIManager.json"))

# Dictionaries for the titles of games
title_dict = jsonInfo.get("title_dict")
title_location_dict = jsonInfo.get("title_location_dict")
# Displayables is only for displayable text. Not UI assets
displayables = jsonInfo.get("displayables")
# I need to be VERY precise with these restraints or else everything breaks
# Dictionary that shows the constraints for the pointer in the x direction
constraints_x = jsonInfo.get("constraints_x")
# Dictionary that shows the constraints for the pointer in the y direction
constraints_y = jsonInfo.get("constraints_y")

# Global spacing
# Responsible for dictating the spacing between the items in the UI for the x direction
spacings_x = jsonInfo.get("spacings_x")
# Responsible for dictating the spacing between the items in the UI for the y direction
spacings_y = jsonInfo.get("spacings_y")

draw_function_dict = {"Load Game": draw_save_UI, "Player Select": draw_background}

portraitOrb = game.image.load("UI/Orb.png")
portrait = game.image.load("portraits/small_knight.png")
circle = game.image.load("UI/circle.png")
separator = game.image.load("UI/smaller_separator.png")
semiCircle = game.image.load("UI/semiCircle.png")
smallerSemiCircle = game.image.load("UI/smaller_semiCircle.png")
healthBar = game.image.load("UI/health_bar.png")
redSemiCircle = game.image.load("UI/red_semicircle.png")
manaBar = game.image.load("UI/mana_bar.png")
blueSemiCircle = game.image.load("UI/blue_semicircle.png")
submenu = game.image.load("UI/Battle_UI/sub_menu.png")
class Cursor:
    def __init__(self):
        self.xConstraints = ()
        self.yConstraints = ()
        self.pos = ()
        self.cursor = game.image.load("UI/Cursor.png")
        self.spacingX = 0
        self.spacingY = 0

    def set_cursor_info(self, xSpacing, ySpacing, x_constraints, y_constraints):
        self.spacingX = xSpacing
        self.spacingY = ySpacing
        # none of the given parameters ever be None in an active UI so this means there is no active UI
        if xSpacing is not None:
            self.xConstraints = (x_constraints[0] - 80, x_constraints[1] - 80)
            self.yConstraints = (y_constraints[0] - 20, y_constraints[1] - 20)
            self.pos = (self.xConstraints[0], self.yConstraints[0])


    def handle_cursor(self, eventList):
        select = False
        xMin = self.xConstraints[0]  # Starting point for x btw
        xMax = self.xConstraints[1]

        yMin = self.yConstraints[0]  # Starting point for y btw
        yMax = self.yConstraints[1]

        xPos = self.pos[0]
        yPos = self.pos[1]

        # For readability
        for event in eventList:
            if event.type == game.KEYDOWN:
                if event.key == game.K_RETURN:
                    select = True
                    break  # Breaks because this indicates a transition to another screen
                elif event.key == game.K_ESCAPE:
                    select = None
                    break  # Breaks because this indicates a transition to another screen
                elif event.key == game.K_RIGHT and self.spacingX != 0:
                    xPos += self.spacingX
                    if xPos > xMax:
                        xPos = xMin
                elif event.key == game.K_LEFT and self.spacingX != 0:
                    xPos -= self.spacingX
                    if xPos < xMin:
                        xPos = xMax
                elif event.key == game.K_DOWN:
                    # Inverted because Pygame is weird
                    yPos += self.spacingY
                    if yPos > yMax:
                        yPos = yMin
                elif event.key == game.K_UP:
                    # Inverted because Pygame is weird
                    yPos -= self.spacingY
                    if yPos < yMin:
                        yPos = yMax
        self.pos = (xPos, yPos)
        return select

class UIManager:

    # Might need a reference to the players inventory
    def __init__(self, font, screen):
        self.UI = None
        self.prevUIs = []  # List of previously viewed UIs so that the player can backtrack
        self.displayable = ()   # Text to display on screen
        self.constraint_x = ()  # Constraints for the x axis
        self.constraint_y = ()  # Constraints for the y axis
        self.spacing_x = 0      # Spacing for the x axis
        self.spacing_y = 0      # Spacing for the y axis
        
        # Continue will be added to displayable AFTER SaveManager confirms that a prev_save does exist
        self.cursor = Cursor()
        self.font = font  # Reference to writing surface that I use in Rpg2.py (no point in making a new one)
        self.screen = screen  # Reference to the screen object from ScreenManager
        # targets are a list of coordinates where the enemy objects are
        self.targets = []
        # targetSlider indicates where the cursor is pointing
        self.targetSlider = -1
        # indicates if the subMenu is active
        self.subMenu = False
        self.subMenuItems = []
        self.subMenuMinIndex = -1
        self.subMenuMaxIndex = -1
        self.subMenuSlider = -1
        self.change_UI("Start")  # Sets the value of everything
        
    def change_UI(self, UI, flag=True):
        # Unlike other managers, None should never be able to occur in this function
        if displayables.get(UI) is not None or UI is None:  # Ignore the change if there's no UI for the given UI
            # Only exception is when we pass null to get rid of UI
            if self.UI is not None and flag:  # flag determines if a page is added to stack
                self.prevUIs.append(self.UI)
            if UI is None:
                self.prevUIs.clear()  # Clear the prev UIs
            self.UI = UI
            self.displayable = displayables.get(self.UI)
            self.constraint_x = constraints_x.get(self.UI)
            self.constraint_y = constraints_y.get(self.UI)
            self.spacing_x = spacings_x.get(self.UI)
            self.spacing_y = spacings_y.get(self.UI)
            self.cursor.set_cursor_info(self.spacing_x, self.spacing_y, self.constraint_x, self.constraint_y)

        
    # Draws the UI based on current state. Assets are game assets that need to be loaded in for certain UIs
    def draw_UI(self, eventList, assets=None):
        # Function that actually draws what's on screen
        # Assets should be drawn first, so we don't cover up the text
        title = title_dict.get(self.UI)
        self.draw_menu_and_assets(assets)
        if title is not None:
            tempFont = game.font.Font('font/Pixeltype.ttf', 100)
            displayableText = tempFont.render(title, False, "Red")
            location = title_location_dict.get(self.UI)
            self.screen.blit(displayableText, location)

        # Purely for readability
        xMin = self.constraint_x[0]  # Starting point for x btw
        xMax = self.constraint_x[1]

        yMin = self.constraint_y[0]  # Starting point for y btw

        pos = [xMin, yMin]  # Position of the drawn object
        for item in self.displayable:
            displayableText = self.font.render(item, False, "Red")
            self.screen.blit(displayableText, pos)
            if self.spacing_x != 0:  # If there's a need to space X position then do this
                # Draw what needs to be drawn.
                pos[0] += self.spacing_x  # Increment x's position
                if pos[0] > xMax:
                    pos[0] = xMin  # Reset x position
                    pos[1] += self.spacing_y  # Increment y's position

            else:
                pos[1] += self.spacing_y  # Increment y's position
        if self.subMenu and self.UI != "Select Target":
            self.draw_submenu()
        return self.handle_cursor(eventList)
    
    # Funtion that handles the position of the cursor
    def handle_cursor(self, keys):
        result = None, None
        if self.subMenu and self.UI != "Select Target":
            oldSliderVal = self.subMenuSlider
            flag = self.handle_submenu_input(keys)
            if flag is None:
                # reset values
                self.subMenu = False
                self.subMenuItems.clear()
                self.subMenuSlider = -1
                self.subMenuMaxIndex = -1
                self.subMenuMinIndex = -1
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
                        if self.subMenuMaxIndex > len(self.subMenuItems):
                            self.subMenuMaxIndex = len(self.subMenuItems) - 1
                        # correct the slider val
                        if self.subMenuSlider >= len(self.subMenuItems):
                            self.subMenuSlider = len(self.subMenuItems) - 1
                    elif self.subMenuSlider < self.subMenuMinIndex and self.subMenuSlider > 0:
                        # guaranteed to be right by virtue of the above conditions
                        self.subMenuMinIndex = int(self.subMenuSlider / 9) * 9
                        # new min slider index, assuming full row ( 3 x 3, 9 items in total for the screen)
                        self.subMenuMaxIndex = self.subMenuMinIndex - 8
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
        elif self.UI == "Select Target":
            oldSliderVal = self.targetSlider
            flag = self.handle_select_inputs(keys)
            if flag is None:
                # go to the previous UI and reset values
                self.targets.clear()
                self.targetSlider = -1
                self.change_UI(self.prevUIs.pop(), False)
            elif flag:
                # return the location of your target
                result = self.UI, self.targets[self.targetSlider]
            else:
                # validate targetSlider pos and draw cursor
                if self.targetSlider > len(self.targets) - 1 or self.targetSlider < 0:
                    self.targetSlider = oldSliderVal
                self.screen.blit(self.cursor.cursor, self.targets[self.targetSlider])
        else:
            flag = self.cursor.handle_cursor(keys)
            # If a selection is made, find out which option was selected
            if flag is None:
                # Return to the previous UI if the array contains an item
                if len(self.prevUIs) != 0:  # Technically speaking this can be simplified to if self.prevUIs
                    self.change_UI(self.prevUIs.pop(), False)  # Setting flag to false means don't add to stack

            elif flag:
                pos = self.cursor.pos
                if self.spacing_x != 0:
                    # maxSpacing is the amount of movements in the array to represent 1 Y transition
                    # We get this value by getting the difference between the max X restraint and the min X restraint
                    # We then divide the difference by the spacing
                    maxSpacing = (self.cursor.xConstraints[1] - self.cursor.xConstraints[0]) / self.spacing_x + 1

                    # We then add the amount of movements in the x direction
                    # to the movement in they y direction using maxSpacing to translate it to
                    # a position in the 1D array
                    xDistance = ((pos[0] - self.cursor.xConstraints[0]) / self.spacing_x)
                    yDistance = ((pos[1] - self.cursor.yConstraints[0]) / self.spacing_y)
                    listPos = (xDistance + yDistance * maxSpacing)

                else:
                    # If there's no x spacing then only y spacing matters
                    listPos = ((pos[1] - self.cursor.yConstraints[0]) / self.spacing_y)
                item = self.displayable[int(listPos)]
                result = self.UI, item
            else:
                self.screen.blit(self.cursor.cursor, self.cursor.pos)
        return result

    def draw_health_bar(self, knight):
        # drawing red and blue bars
        loopVal = (knight.Hp/knight.Hpcap) * 300  # How many times the loop should run
        for barPos in range(int(loopVal)):
            self.screen.blit(healthBar, (barPos + 66, 6))
            if barPos == loopVal - 1:
                self.screen.blit(redSemiCircle, (barPos + 52, -15))

        loopVal = (knight.Mp / knight.Mpcap) * 234  # 234 because 300-66 = 234
        for barPos in range(int(loopVal)):
            self.screen.blit(manaBar, (barPos + 66, 44))
            if barPos == loopVal - 1:
                self.screen.blit(blueSemiCircle, (barPos + 54, 30))

        # drawing health and mana bars
        self.screen.blit(separator, (66, 5))
        self.screen.blit(semiCircle, (340, 0))
        self.screen.blit(separator, (66, 43))
        self.screen.blit(separator, (0, 66))
        self.screen.blit(smallerSemiCircle, (280, 40))

        # drawing values in the health bars
        hpText = self.font.render(str(knight.Hp)+"/"+str(knight.Hpcap), False, "White")
        mpText = self.font.render(str(knight.Mp)+"/"+str(knight.Mpcap), False, "White")
        self.screen.blit(hpText, (200, 15))
        self.screen.blit(mpText, (180, 43))

        # Drawing portrait circle
        self.screen.blit(circle, (0, 0))
        self.screen.blit(portraitOrb, (0, 0))
        self.screen.blit(portrait, (5, 0))

    def draw_menu_and_assets(self, assets):
        # Draw the remaining information
        function = draw_function_dict.get(self.UI)
        if function is not None:
            function(self.screen, self.font)
        # If assets are present draw them as well
        if assets is not None:
            pass

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
        self.screen.blit(submenu, (350, 550))
        for i in range(len(subsetItems)):
            x_pos = i % 3 * 400 + 450
            y_pos = int(i / 3) * 75 + 600
            self.screen.blit(self.font.render(subsetItems[i], False, "Black"), (x_pos, y_pos))

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

    def handle_select_inputs(self, eventList):
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
                    self.targetSlider += 3
                elif event.key == game.K_LEFT:
                    self.targetSlider -= 3
                elif event.key == game.K_DOWN:
                    self.targetSlider += 1
                elif event.key == game.K_UP:
                    self.targetSlider -= 1
        return select