import pygame as game
import pygame.display
from sys import exit
import Animation_Manager

game.init()
screen = game.display.set_mode((1000, 800))
clock = game.time.Clock()
game.display.set_caption("Legend of Zeroes, Trails of Cold Meals")
font = game.font.Font('font/Pixeltype.ttf', 50)


temp_screen = game.image.load("2D_Battle_Art/PNG/Battleground1/Bright/Battleground1.png")
text_surface = font.render("Checking", False, "Red")
knight_surface = game.image.load("Knight/Colour1/NoOutline/120x80_PNGSheets/_Attack.png")
knight_surface = game.image.load("Knight/Cut_Sprites/Attack_1 (1).gif")

test = Animation_Manager.AnimationManager()
test.Change_array("Knight Attack")
test_ani = []
animation_tracker = 0
i = 500
while(True):
    for event in game.event.get():
        if event.type == game.QUIT:
            game.quit()
            exit()

    #Changing animations
    keys = game.key.get_pressed()
    test_ani = test.ani_array
    if keys[game.K_RIGHT]:
        test.Change_array("Knight Run R")
        if test_ani != test.ani_array:
            animation_tracker = 0
        else:
            i += 2
    elif keys[game.K_LEFT]:
        test.Change_array("Knight Run L")
        if test_ani != test.ani_array:
            animation_tracker = 0
        else:
            i -= 2
    else:
        test.Change_array("Idle")
        if test_ani != test.ani_array:
            animation_tracker = 0
    screen.blit(temp_screen, (0, 0))
    screen.blit(text_surface, (0, 0))
    screen.blit(knight_surface, (i, 600))

    animation_tracker += 1
    if i > 1000 or i < 0:
        i = 0

    if animation_tracker >= (10*test.ani_array[0]-1):
        animation_tracker = 0
    spot = animation_tracker // 10
    appendable = "("+str(spot+1)+").gif"
    knight_surface = game.image.load(test.ani_array[1]+appendable)

    pygame.display.update()
    clock.tick(60)
