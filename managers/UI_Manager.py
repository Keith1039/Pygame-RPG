import pygame as game
import time
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

# Dictionaries for the titles of games
title_dict = {"Start": "Legend of Zeroes, Trails of Cold Meals", "Load Game": "Choose Your Save File"}
title_location_dict = {"Start": (200, 200), "Load Game": (350, 50)}
# Displayables is only for displayable text. Not UI assets
displayables = {"Start": ("Start Game", "Continue", "Load Game"), "Startv2": ("Start Gamev2", "Continuev2", "Load Gamev2", "Optionsv2"),
                "Load Game": ("Save Slot #1", "Save Slot #2", "Save Slot #3", "Save Slot #4")}
# I need to be VERY precise with these restraints or else everything breaks
# Dictionary that shows the constraints for the pointer in the x direction
constraints_x = {"Start": (660, 1000), "Startv2": (660, 960), "Load Game": (250, 1000)}
# Dictionary that shows the constraints for the pointer in the y direction
constraints_y = {"Start": (500, 600), "Startv2": (500, 550), "Load Game": (150, 630)}

# Global spacing
# Responsible for dictating the spacing between the items in the UI for the x direction
spacings_x = {"Start": 0, "Startv2": 300, "Load Game": 0}
# Responsible for dictating the spacing between the items in the UI for the y direction
spacings_y = {"Start": 50, "Startv2": 50, "Load Game": 160}

draw_function_dict = {"Load Game": draw_save_UI}


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


    def handle_cursor(self, keys):
        select = False
        # For readability
        xMin = self.xConstraints[0]  # Starting point for x btw
        xMax = self.xConstraints[1]

        yMin = self.yConstraints[0]  # Starting point for y btw
        yMax = self.yConstraints[1]

        xPos = self.pos[0]
        yPos = self.pos[1]
        if (keys[game.K_RIGHT] or keys[game.K_d]) and self.spacingX != 0:
            xPos += self.spacingX
            if xPos > xMax:
                xPos = xMin
        elif (keys[game.K_LEFT] or keys[game.K_a]) and self.spacingX != 0:
            xPos -= self.spacingX
            if xPos < xMin:
                xPos = xMax
        elif keys[game.K_DOWN] or keys[game.K_s]:
            # Inverted because Pygame is weird
            yPos += self.spacingY
            if yPos > yMax:
                yPos = yMin
        elif keys[game.K_UP] or keys[game.K_w]:
            # Inverted because Pygame is weird
            yPos -= self.spacingY
            if yPos < yMin:
                yPos = yMax
        elif keys[game.K_RETURN]:
            select = True
        elif keys[game.K_ESCAPE]:
            # Backtrack time
            select = None
            pass
        self.pos = (xPos, yPos)
        time.sleep(0.08)  # Adding a delay to make the UI feel smoother otherwise
        # The UI is too responsive
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
        self.change_UI("Start")  # Sets the value of everything
        
    def change_UI(self, UI, flag=True):
        # Unlike other managers, None should never be able to occur in this function
        if displayables.get(UI) is not None or UI is None:  # Ignore the change if there's no UI for the given UI
            # Only exception is when we pass null to get rid of UI
            if self.UI is not None and flag:  # flag determines if a page is added to stack
                self.prevUIs.append(self.UI)
            self.UI = UI
            self.displayable = displayables.get(self.UI)
            self.constraint_x = constraints_x.get(self.UI)
            self.constraint_y = constraints_y.get(self.UI)
            self.spacing_x = spacings_x.get(self.UI)
            self.spacing_y = spacings_y.get(self.UI)
            self.cursor.set_cursor_info(self.spacing_x, self.spacing_y, self.constraint_x, self.constraint_y)

        
    # Draws the UI based on current state. Assets are game assets that need to be loaded in for certain UIs
    def draw_UI(self, keys, assets=None):  
        # Function that actually draws what's on screen
        # Assets should be drawn first so we don't cover up the text
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

        return self.handle_cursor(keys)
    
    # Funtion that handles the position of the cursor
    def handle_cursor(self, keys):
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
                #print(xDistance)
                #print(yDistance)
                #print(listPos)
            else:
                # If there's no x spacing then only y spacing matters
                listPos = ((pos[1] - self.cursor.yConstraints[0]) / self.spacing_y)
            item = self.displayable[int(listPos)]
            return [self.UI, item]
        else:
            self.screen.blit(self.cursor.cursor, self.cursor.pos)
            return None

    def draw_menu_and_assets(self, assets):
        # Draw the remaining information
        function = draw_function_dict.get(self.UI)
        if function is not None:
            function(self.screen, self.font)
        # If assets are present draw them as well
        if assets is not None:
            pass

