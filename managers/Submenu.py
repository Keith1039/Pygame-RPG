import pygame as game
from managers.Cursor import Cursor
import Utils
import re

class Submenu:
    def __init__(self, UI, screen, items):
        self.UI = UI
        self.screen = screen
        self.font = game.font.Font('font/Pixeltype.ttf', 50)
        if len(items) == 0:
            self.items = [""]
        else:
            self.items = items
        self.page = 0  # keeps a track of which 'page' we're on
        self.maxPage = int(len(self.items) / 9)  # how many pages we can have (accurate cuz we start at page 0)
        self.minIndex = 0
        self.maxIndex = 8  # because we start at 0
        if self.maxIndex >= len(self.items):
            self.maxIndex = len(self.items) - 1
        self.constraints = {
            "x_constraints": (380, 1180),
            "y_constraints": (580, 805),
            "x_spacing": 400,
            "y_spacing": 75
        }
        self.submenu = game.image.load("UI/Battle_UI/sub_menu.png")
        # construct the matrix
        matrix = Utils.construct_matrix_given_parameters(self.constraints, self.items[self.minIndex:self.maxIndex + 1])
        self.cursor = Cursor(matrix)  # set the matrix

    def handle_cursor(self, eventList):
        # handle cursor but don't autocorrect the position and value
        prevState = self.cursor.__dict__.copy()  # make a copy of data beforehand
        select = self.cursor.handle_cursor(eventList, False, False)  # run handle_cursor without autocorrect
        flag = self.update_page()  # update the pages
        if not flag:  # check to see if I need to do a reset
            self.cursor.__dict__ = prevState  # return the cursor to its previous state
            # re-run the code and have autocorrect enabled but with wraparound disabled
            select = self.cursor.handle_cursor(eventList, correct=True, wraparound=False)
        if select:
            # return the UI and the selection
            return self.UI + "(S)", self.get_item()
        elif select is None:
            # return the UI and the None
            return self.UI + "(S)", None
        else:
            return None, None

    def get_item(self):
        # uses the fact that this is a 3x3 matrix (if this changes my life gets harder)
        # gets the index from the item list based off of information from cursor and other stuff.
        return self.items[self.minIndex + (self.cursor.rowSlider * 3) + self.cursor.columnSlider]


    def update_page(self):
       # this is the case where you're trying to go back from the first row
       # indicates if an update to the page happened
       # False means an update is needed but failed to happen (i.e. no next or previous page)
       # True means that an update happened successfully
       # None means that no updates occurred
       update = None
       index = self.minIndex + (self.cursor.rowSlider * 3) + self.cursor.columnSlider
       page = int(index / 9)
       # check if the index page matches with current page and if it's an allowed page
       if page != self.page and page <= self.maxPage:
           self.move_to_page(page)
           # minIndex is updated in move_to_page() so it should be accurate
           relativeIndex = index - self.minIndex
           self.cursor.rowSlider = int(relativeIndex / 3)  # each row is 3
           self.cursor.columnSlider = relativeIndex % 3  # the column is the leftover part of the index
           update = True
       elif page > self.maxPage:  # we have an invalid page
            update = False
       return update

    def move_to_page(self, page):
        # setting up the page information
        self.page = page
        self.minIndex = self.page * 9
        self.maxIndex = self.minIndex + 8
        # check to see if max index is still valid
        if self.maxIndex >= len(self.items):
            self.maxIndex = len(self.items) - 1  # correct maxIndex
        # reconstruct the matrix for the cursor
        matrix = Utils.construct_matrix_given_parameters(self.constraints, self.items[self.minIndex:self.maxIndex + 1])
        self.cursor.set_new_positions(matrix)  # reset the cursor
        print(self.items[self.minIndex:self.maxIndex + 1])
        print(matrix)

    def draw_submenu_items(self):
        for i in range(len(self.items[self.minIndex:self.maxIndex + 1])):
            x_pos = i % 3 * 400 + 450
            y_pos = int(i / 3) * 75 + 600
            self.screen.blit(self.font.render(self.items[i], False, "Black"), (x_pos, y_pos))

    def draw_UI(self, eventList):
        self.screen.blit(self.submenu, (350, 550))  # draw the physical submenu
        UI, choice = self.handle_cursor(eventList)  # handle the cursor events
        self.draw_submenu_items()  # draw the submenu items
        self.screen.blit(self.cursor.cursor, self.cursor.pos)
        # strip the amount part from the item
        if choice is not None:
            match = re.search("x[1-9]+", choice)
            if match:  # check if there's a match
                choiceArr = choice.split()  # convert it into an array
                choiceArr.pop(len(choiceArr) - 1)  # get rid of the amount part of the string
                choice = " ".join(choiceArr)  # rejoin the array
                choice.strip()  # get rid of useless white space
        return UI, choice  # return everything
