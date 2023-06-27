import os
import pygame as game

# Dict that will point to the files where the dialogue still is
text_dict = {}
# Portrait dict takes in a name and then gets the portrait
portrait_dict = {"Knight": game.image.load("portraits/Knight.png"), "Rion": game.image.load("portraits/Knight.png")}
class DialogueManager: 
    def __init__(self ):
        self.file = None
        self.portrait = None 
        self.name = ""
        self.characterBox = game.image.load("portraits/character_box.png")
        self.textBox = game.image.load("portraits/text_box.png")
        self.event = None
        self.prevText = ""
    
    def load_file(self, event):
        # Loads the file that we read from
        self.event = event
        self.file = open(event.path)
    
    # Returns a single text line. Probably going to have to enforce a char limit too huh...
    def get_text(self):
        text = self.file.readline()
        self.prevText = text
        #Clears file's value if EOF has been reached.
        if text == "":
            self.clear_file()
            self.prevText = "1"
        else:
            text = self.load_portrait(text)
        return text
    
    def clear_file(self):
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
        self.portrait = portrait_dict.get(name) # This can be None btw so there has to be logic checking this
        # Returns text that has name stripped from it
        return text
