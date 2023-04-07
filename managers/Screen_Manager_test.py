from managers.Screen_Manager import ScreenManager
import pygame as game

global screenManager
game.init()
screen = game.display.set_mode((1422, 800))
screenManager = ScreenManager(screen)

def test_init_Screen():
    assert screenManager.context == "Background1"

def test_move_to_screen2():
    screenManager.change_screen(901)
    assert screenManager.context == "Background2"

def test_move_to_screen1_from_2():
    screenManager.change_screen(-1)
    assert screenManager.context =="Background1"
