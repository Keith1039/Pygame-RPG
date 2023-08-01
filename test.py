import pygame as game
from sys import exit
from managers import UIManager

game.init()
screen = game.display.set_mode((1422, 800))
clock = game.time.Clock()
game.display.set_caption("Legend of Zeroes, Trails of Cold Meals")
font = game.font.Font('font/Pixeltype.ttf', 50)
UIManager = UIManager(font, screen)
while True:
    for event in game.event.get():
        if event.type == game.QUIT:
            game.quit()
            exit()
    keys = game.key.get_pressed()
    UIManager.draw_UI(keys) #Handles which keys were pressed
    game.display.update()
    clock.tick(60)