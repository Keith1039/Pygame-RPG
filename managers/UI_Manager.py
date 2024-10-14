import pygame as game
import json
import re
from managers.UI_Manager_draw import *
from managers.Cursor import Cursor
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
portrait = game.image.load("portraits/Knight.png")
portrait = game.transform.scale(portrait, (150, 150))
circle = game.image.load("UI/circle.png")
separator = game.image.load("UI/smaller_separator.png")
semiCircle = game.image.load("UI/semiCircle.png")
smallerSemiCircle = game.image.load("UI/smaller_semiCircle.png")
healthBar = game.image.load("UI/health_bar.png")
redSemiCircle = game.image.load("UI/red_semicircle.png")
manaBar = game.image.load("UI/mana_bar.png")
blueSemiCircle = game.image.load("UI/blue_semicircle.png")
submenu = game.image.load("UI/Battle_UI/sub_menu.png")

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
        self.cursor = Cursor([])
        self.font = font  # Reference to writing surface that I use in Rpg2.py (no point in making a new one)
        self.screen = screen  # Reference to the screen object from ScreenManager
        # targets are a list of coordinates where the enemy objects are
        self.targets = []
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
            if self.displayable is not None and self.UI != "Select Target":  # check if there is a need for the cursor
                self.cursor.set_new_positions(self.create_matrix_from_constraints())  # set the new cursor info
            elif self.UI != "Select Target":
                self.cursor.reset()  # reset the cursor

    def create_matrix_from_constraints(self):
        # offsets for display purposes only
        x_offset = -70
        y_offset = -20
        matrix = []
        columnNum = 1
        rowNum = 1
        if self.spacing_x != 0:
            columnNum = int((self.constraint_x[1] - self.constraint_x[0])/self.spacing_x) + 1

        if self.spacing_y != 0:
            rowNum = int((self.constraint_y[1] - self.constraint_y[0])/self.spacing_y) + 1

        for column in range(columnNum):
            columnPos = self.constraint_x[0] + column * self.spacing_x
            rowValues = []
            for row in range(rowNum):
                rowPos = self.constraint_y[0] + row * self.spacing_y
                rowValues.append((columnPos + x_offset, rowPos + y_offset))
            matrix.append(rowValues)
        return matrix

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
                pos[0] = pos[0] + self.spacing_x  # Increment x's position
                if pos[0] > xMax:
                    pos[0] = xMin  # Reset x position
                    pos[1] += self.spacing_y  # Increment y's position
            else:
                pos[1] += self.spacing_y  # Increment y's position
        # if self.subMenu and self.UI != "Select Target":
        #     self.draw_submenu()
        return self.handle_cursor(eventList)
    
    # Function that handles the position of the cursor
    def handle_cursor(self, eventList):
        result = None, None
        flag = self.cursor.handle_cursor(eventList)
        if flag is None:
            if self.UI == "Select Target":
                self.targets.clear()
            # change_UI() takes care of the cursor stuff
            result = self.UI, None
            if len(self.prevUIs) > 0:
                self.change_UI(self.prevUIs.pop(), False)
        elif flag:
            cursorIndex = self.cursor.get_index_from_cursor()
            if self.UI == "Select Target":
                result = self.UI, self.targets[cursorIndex]
            else:
                result = self.UI, self.displayable[cursorIndex]
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
        self.screen.blit(portrait, (0, -65))

    def draw_menu_and_assets(self, assets):
        # Draw the remaining information
        function = draw_function_dict.get(self.UI)
        if function is not None:
            function(self.screen, self.font)
        # If assets are present draw them as well
        if assets is not None:
            pass