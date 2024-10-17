import pygame as game

class Cursor:
    def __init__(self, positions):
        self.positions = positions  # a matrix of possible coordinates for the cursor to have
        self.rowSlider = 0  # row to look at
        self.columnSlider = 0  # column to look at
        if len(self.positions) > 0:
            self.pos = self.positions[self.columnSlider][self.rowSlider]  # set the first position
        self.cursor = game.image.load("UI/Cursor.png")

    def reset(self):
        # reset the information in the cursor
        self.rowSlider = 0
        self.columnSlider = 0
        self.pos = ()

    def set_new_positions(self, positions):
        if len(positions) > 0:
            self.positions = positions  # reset the positions
            self.rowSlider = 0  # row to look at
            self.columnSlider = 0  # column to look at
            self.pos = self.positions[self.columnSlider][self.rowSlider]  # set the first position

    def get_index_from_cursor(self):
        # returns an index in an equivalent 1 d array
        return self.rowSlider * len(self.positions) + self.columnSlider

    def handle_cursor(self, eventList, correct=True, wraparound=True):
        # if correct is true, the cursor will not allow invalid movements to happen
        select = False
        for event in eventList:
            if event.type == game.KEYDOWN:
                if event.key == game.K_RETURN:
                    select = True
                    break  # Breaks because this indicates a transition to another screen
                elif event.key == game.K_ESCAPE:
                    select = None
                    break  # Breaks because this indicates a transition to another screen
                elif event.key == game.K_RIGHT:
                    if self.columnSlider + 1 < len(self.positions):  # check if it's a valid index)
                        self.columnSlider += 1  # update the slider
                    # check if the next row has "space"
                    elif self.columnSlider == len(self.positions) - 1 and len(self.positions[0]) > self.rowSlider + 1:
                        print(len(self.positions), self.rowSlider)
                        # move over to the first column on the next row
                        self.columnSlider = 0
                        self.rowSlider += 1
                    elif not correct:
                        self.columnSlider += 1
                elif event.key == game.K_LEFT:
                    if self.columnSlider - 1 >= 0:  # check to see if it's a valid index
                        self.columnSlider -= 1  # update the slider
                    elif self.columnSlider == 0 and self.rowSlider - 1 >= 0:
                        self.columnSlider = len(self.positions) - 1  # go to the furthest column
                        self.rowSlider -= 1
                    elif not correct:
                        self.columnSlider -= 1
                elif event.key == game.K_DOWN:
                    if self.rowSlider + 1 < len(self.positions[self.columnSlider]):  # verify index
                        self.rowSlider += 1  # update the slider
                    elif self.rowSlider + 1 > len(self.positions[self.columnSlider]) - 1 and wraparound:
                        self.rowSlider = 0
                    elif not correct:
                        self.rowSlider += 1
                elif event.key == game.K_UP:
                    if self.rowSlider - 1 >= 0:  # validate the index
                        self.rowSlider -= 1  # update the slider
                    elif self.rowSlider - 1 < 0 and wraparound:  # enables wrapping around
                        self.rowSlider = len(self.positions[self.columnSlider]) - 1
                    elif not correct:
                        self.rowSlider -= 1
        # if the correct flag is true, we're guaranteed a valid position
        if correct:
            self.pos = self.positions[self.columnSlider][self.rowSlider]  # get the position
        return select  # return selection