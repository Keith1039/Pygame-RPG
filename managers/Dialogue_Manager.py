import os
import pygame as game
import time

# Dict that will point to the files where the dialogue still is
text_dict = {}
# Portrait dict takes in a name and then gets the portrait
portrait_dict = {"Knight": game.image.load("portraits/Knight.png"), "Rion": game.image.load("portraits/Knight.png")}
class DialogueManager: 
    def __init__(self, font, screen):
        self.file = None      # File that's being read from
        self.portrait = None  # Portrait that's displayed on screen
        self.font = font      # Font used to write dialogue
        self.screen = screen  # For drawing things
        self.name = ""
        self.characterBox = game.image.load("portraits/character_box.png")
        self.textBox = game.image.load("portraits/text_box.png")
        self.event = None     # Event that's currently loaded
        self.prevText = ""    # Previous text
    
    def load_file(self, event):
        # Loads the file that we read from
        self.event = event  # Stored event
        self.file = open(event.path)  # file that's being accessed
        self.prevText = self.get_text()  # Sets previous text by default
    
    # Returns a single text line. Probably going to have to enforce a char limit too huh...
    def get_text(self):
        text = self.file.readline()
        self.prevText = text
        # Clears file's value if EOF has been reached.
        if text == "":
            self.clear_file()
        else:
            text = self.load_portrait(text)
        return text
    
    def clear_file(self):
        # Clears the file and the event associated with it
        self.file.close()
        self.event.activated = True
        self.event = None
        self.file = None

    def load_portrait(self, text):
        # Finding the character name
        name = ""
        i = 0
        for i in range(len(text)):
            if text[i] == ":":
                text = text[i+1: len(text)]
                break
            else:
                name += text[i]
        self.name = name
        self.prevText = text
        self.portrait = portrait_dict.get(name)  # This can be None btw so there has to be logic checking this
        # Returns text that has name stripped from it
        return text
    def draw_dialogue(self, eventList):  # For stuff like this reading from event list might be better
        # Make this able to show previous dialogue when you tab

        text = self.prevText
        for event in eventList:
            if event.type == game.KEYDOWN:
                if event.key == game.K_RETURN:
                    text = self.get_text()
                    break  # Should break after
        textSurface = self.font.render(text, False, "Red")
        if self.portrait is not None:
            nameSurface = self.font.render(self.name, False, "Red")
            self.screen.blit(self.characterBox, (0, 650))
            self.screen.blit(self.portrait, (15, 670))
            self.screen.blit(nameSurface, (20, 620))
            self.screen.blit(self.textBox, (120, 650))
            self.screen.blit(textSurface, (140, 670))
        else:
            # This way there's no awkward space where the portrait used to be.
            self.screen.blit(self.textBox, (0, 650))
            self.screen.blit(textSurface, (20, 670))
        # There is an easier way to do this, but it makes my eyes bleed so no :)
        return text != ""
