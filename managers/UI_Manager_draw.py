import pygame as game
import os
import json
import datetime

# This python file contains all the drawing function that would clutter up the manager file

def draw_save_UI(screen, font):
    saveBackground = game.image.load("UI/UI_Background.png")
    separator = game.image.load("UI/separator.png")
    saves = os.listdir("save/")
    knightPortrait = game.image.load("portraits/mini_knight.png")
    screen.blit(saveBackground, (211, 100))
    screen.blit(separator, (235, 275))
    screen.blit(separator, (235, 450))
    screen.blit(separator, (235, 625))

    for save in saves:  # Iterate through saves and display the information
        if "save_data" in save:  # prev_save_info.json can exist as well
            saveNumber = int(save[9]) - 1
            height = 200 + (160 * saveNumber)
            #print(save)
            file = open("save/" + save, "r")
            saveInfo = json.load(file)
            lvlText = font.render("Lvl: " + str(saveInfo["Knight"]["Lvl"]), False, "Black")
            createTime = os.path.getctime("save/" + save)
            createDate = datetime.datetime.fromtimestamp(createTime)
            dateText = font.render("Date: " + createDate.strftime('%Y-%m-%d %H:%M:%S'), False, "Black")
            screen.blit(knightPortrait, (250, height))
            screen.blit(lvlText, (310, height + 15))
            screen.blit(dateText, (500, height + 15))
            file.close()

def draw_background(screen, font):
    background = game.image.load("UI/Battle_UI/Temp_Background.png")
    screen.blit(background, (100, 550))

