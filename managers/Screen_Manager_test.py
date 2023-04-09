from managers.Screen_Manager import ScreenManager
import pygame as game

global screenManager
game.init()
screen = game.display.set_mode((1422, 800))
screenManager = ScreenManager(screen)

def test_init_screen():
    assert screenManager.context == "Background1"

# This should not trigger the move
def test_move_to_screen2F():
    screenManager.change_screen(901)
    assert screenManager.context == "Background1"

def test_move_to_screen2S():
    screenManager.change_screen(1001)
    assert screenManager.context == "Background2"

# Since a screen past screen 2 isn't defined the context should not change
def test_move_to_undefined_from_screen2():
    screenManager.change_screen(1001)
    assert screenManager.context == "Background2"

# Context and screen are intertwined so only testing 1 of them is necessary
def test_move_to_screen1_from_screen2():
    screenManager.change_screen(-300)
    assert screenManager.context == "Background1"

def test_move_to_undefined_from_screen1():
    prev_context = screenManager.context
    screenManager.change_screen(-300)
    assert screenManager.context == prev_context

