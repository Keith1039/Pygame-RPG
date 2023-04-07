from managers.Screen_Manager import ScreenManager
import pygame as game

global screenManager
game.init()
screen = game.display.set_mode((1422, 800))
screenManager = ScreenManager(screen)

def test_Init_Screen():
    assert screenManager.context == "Background1"

def test_Move_To_Screen2():
    screenManager.changeScreen(901)
    assert screenManager.context == "Background2"

def test_Move_To_Screen1_from_2():
    screenManager.changeScreen(-1)
    assert screenManager.context =="Background1"
