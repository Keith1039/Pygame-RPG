import pygame as game
import os
# chooses which text box is in use
text_dict = {False: game.image.load("portraits/text_box.png"), True: game.image.load("portraits/text_box_L.png")}
# Portrait dict takes in a name and then gets the portrait
portraitLocation = "portraits/"

class DialogueManager:
    def __init__(self, font, screen):
        self.name = ""  # name of the character
        self.portrait = None  # Portrait that's displayed on screen
        self.font = font      # Font used to write dialogue
        self.largeFont = game.font.Font('font/Pixeltype.ttf', 100)
        self.screen = screen  # For drawing things
        self.event = None  # reference to the event object
        self.nextEvents = []  # list of unprocessed dialogue events
        self.characterBox = game.image.load("portraits/character_box.png")
        self.textBox = game.image.load("portraits/text_box.png")
        self.dialogue = []  # list of strings to be displayed
        self.backlog = []  # text that's been read (NOT IMPLEMENTED YET)
        self.firstLine = []  # further divided dialogue strings
        self.secondLine = []  # further divided dialogue strings

    def load_file(self, event):
        # Loads the file that we read from if it is repeatable or hasn't been activated
        if not event["Activated"] or event["Repeatable"]:
            self.event = event
            file = open(self.event["Dialogue Path"])  # file that's being accessed
            flag = True
            # adds all text in the file to a list
            while flag:
                text = file.readline()
                if text != "":
                    self.dialogue.append(text)
                else:
                    flag = False
    
    # Returns a single text line. Probably going to have to enforce a char limit too huh...
    def get_new_text(self):
        # moves to next line but removing previous lines
        if len(self.dialogue) > 0:
            text = self.dialogue.pop(0)  # pop the next line from queue
            self.backlog.append(text)  # add popped text to the backlog
        else:
            if self.event is not None:  # None check
                self.event["Activated"] = True  # set the event to true now that we're done with it
                self.event = None  # get rid of reference to the event
            if len(self.nextEvents) > 0:
                self.load_file(self.nextEvents.pop(0))  # load the next dialogue event in the list

    def load_portrait(self, text):
        # Finding the character name
        self.portrait = None  # reset the portrait
        portraitLocation = "portraits/"
        name = ""
        pos = text.find(":")
        if pos != -1:
            # get the name
            name = text[0: pos]
        self.name = name
        filePath = portraitLocation + name + ".png"
        if os.path.exists(filePath):
            # if it is a valid name, change the name to match it
            self.portrait = game.image.load(filePath)  # load the image
            self.portrait = game.transform.scale(self.portrait, (150, 150))
            text = text[pos + 1:]  # split the name from the rest of the text since it is a valid name
        # Returns text that has name stripped from it and strip white space
        return text.strip()

    def draw_dialogue(self, eventList, battle=False):
        if len(self.dialogue) > 0:
            self.textBox = text_dict[battle]
            # TODO Make this able to show previous dialogue when you tab
            # condition for the very first time this function is run
            if len(self.firstLine) == 0:
                self.sub_divide_dialogue(self.dialogue[0])
            # assigning the two lines of text
            text = " ".join(self.firstLine)
            text2 = " ".join(self.secondLine)
            for event in eventList:
                if event.type == game.KEYDOWN:
                    if event.key == game.K_RETURN:
                        self.get_new_text()
                        # clear the two line lists
                        self.firstLine.clear()
                        self.secondLine.clear()
                        # subdivide the new dialogue into individual lines
                        if len(self.dialogue) > 0:
                            self.sub_divide_dialogue(self.dialogue[0])
                        break  # loop should end here
            # sets the portrait and gives us the text without the characters name
            # we assume the name for portrait is always in the first line
            text = self.load_portrait(text)
            text = text.replace(" ", "   ")  # adds proper spacing
            text = text.replace("\n", "")  # removes new line symbol
            text2 = text2.replace(" ",  "   ")  # adds proper spacing
            text2 = text2.replace("\n", "")  # removes new line symbol
            if not battle:
                textSurface = self.font.render(text, False, "Red")
                textSurface2 = self.font.render(text2, False, "Red")
            else:
                textSurface = self.largeFont.render(text, False, "Red")
                textSurface2 = self.largeFont.render(text2, False, "Red")
            if self.portrait is not None:
                nameSurface = self.font.render(self.name, False, "Red")
                self.screen.blit(self.characterBox, (0, 650))
                self.screen.blit(self.portrait, (0, 600))
                self.screen.blit(nameSurface, (20, 620))
                self.screen.blit(self.textBox, (120, 650))
                self.screen.blit(textSurface, (140, 670))
                self.screen.blit(textSurface2, (140, 720))

            else:
                # we have to consider two possibilities here
                if not battle:
                    self.screen.blit(self.textBox, (0, 650))
                    self.screen.blit(textSurface, (20, 670))
                    self.screen.blit(textSurface2, (20, 720))
                else:
                    self.screen.blit(self.textBox, (0, 580))
                    self.screen.blit(textSurface, (50, 650))
                    self.screen.blit(textSurface2, (50, 700))
        else:
            self.get_new_text()  # reset things

    def load_dialogue_list(self, dialogueList):
        # just sets the dialogue list
        self.dialogue = dialogueList

    def sub_divide_dialogue(self, text):
        # splits the dialogue string into 2 lines
        # any extra dialogue is inserted back into the queue to be processed
        textList = text.split()
        count = 0
        onSecondLine = False
        maxPos = 50  # largest position we have available
        for i in range(len(textList)):
            tempText = textList[i]
            if count + len(tempText) <= maxPos:
                # add to the count
                count += len(tempText)
                if not onSecondLine:
                    self.firstLine.append(tempText)
                else:
                    self.secondLine.append(tempText)
            elif count + len(tempText) > maxPos:
                if not onSecondLine:
                    # insert into the copy of the list
                    # set the counter to the new first word
                    count = len(tempText)
                    # indicate that we're on the second line
                    onSecondLine = True
                    # add to the second list
                    self.secondLine.append(tempText)
                else:
                    # if the line is still too long, shove it into the first position of the dialogue
                    # queue and process it again, end the loop here
                    # we put it right before the text that is going to get consumed by get_new_text
                    self.dialogue.insert(1, " ".join(textList[i: len(textList)]))
                    break
            count += 3  # adjust for the 3 spaces we add later
        # print("First line: " + str(self.firstLine))
        # print("Second line: " + str(self.secondLine))
