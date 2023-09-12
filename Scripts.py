#!/usr/bin/python
from managers import SaveManager
from managers import ScreenManager
import pygame as game
from Knight import Knight
import sys

game.init()

if __name__ == "__main__":
    game.init()
    screen = game.display.set_mode((1422, 800))
    font = game.font.Font('font/Pixeltype.ttf', 50)
    arg = sys.argv[1]
    if arg == "fill-save":
        screenManager = ScreenManager(screen)
        knight = Knight()
        saveManager = SaveManager(knight, vars(), screenManager)
        for i in range(4):
            saveManager.save(i+1)
    game.quit()
    exit()
