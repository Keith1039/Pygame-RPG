import pygame as game
import pygame.display
from sys import exit
import Animation_Manager
import Knight
from Knight import KStatus
from NPC_Animation_Manager import NPC_Animation_Manager
from Object_Animation_Manager import Object_Animation_Manager
from Screen_Manager import ScreenManager
from Map import DungeonMap_Dict
#I should have an array of sprite managers and it goes through them
game.init()
screen = game.display.set_mode((1422, 800))
clock = game.time.Clock()
game.display.set_caption("Legend of Zeroes, Trails of Cold Meals")
font = game.font.Font('font/Pixeltype.ttf', 50)

#Hero Object
knight = Knight.Knight("Rion", 1, 2, "sword", 1, 1, 1, 1, 1, 1, 1, 1)

#Think I'll go for the 1422 x 800 route from now on
temp_screen = game.image.load("Background_Art/gothic_chapel_portfolio_1422x800.png")
text_surface = font.render("Checking", False, "Red")
knight_surface = game.image.load("Knight/Cut_Sprites/Attack_1 (1).png")

Knight_ani = Animation_Manager.AnimationManager()
Knight_ani.Change_array("Knight Attack")
NPC_Manager = NPC_Animation_Manager()
prev_Knight_ani = []


animation_tracker = 0
animation_tracker2 = 0
animation_tracker3 = 0

#An array filled with spots where the treasure chests are. Dictated by Screen Manager
#Interactable also applies to npcs so yeah.

x = 500

Screen_Manager = ScreenManager(temp_screen)

interactables = Screen_Manager.Apply_context()



while True:
    print(x)
    spot = animation_tracker // 10
    spot2 = animation_tracker2 // 10
    spot3 = animation_tracker3 // 10
    if knight.status == KStatus.DEAD:
        Knight_ani.Change_array("Death")


    for event in game.event.get():
        if event.type == game.QUIT:
            game.quit()
            exit()

    # Changing animations

    # Get's the players key input
    keys = game.key.get_pressed()

    # Determines players overworld movement
    if knight.status != KStatus.IN_COMBAT:
        prev_Knight_ani = Knight_ani.ani_array
        if knight.status == KStatus.NORMAL:
            if keys[game.K_RIGHT]:
                Knight_ani.Change_array("Knight Run R")
                if prev_Knight_ani != Knight_ani.ani_array:
                    animation_tracker = 0
                else:
                    x += 4
            elif keys[game.K_LEFT]:
                Knight_ani.Change_array("Knight Run L")
                if prev_Knight_ani != Knight_ani.ani_array:
                    animation_tracker = 0
                else:
                    x -= 4
            elif keys[game.K_UP]:
                for u in range(len(interactables)):
                    status = knight.status
                    interactable = interactables[u]
                    Screen_Manager.Object_Ani.Change_array(knight, x, interactable)
                    if status != knight.status:
                        #resetting animation_tracker
                        animation_tracker3 = 0
            else:
                Knight_ani.Change_array("Idle")
                if prev_Knight_ani != Knight_ani.ani_array:
                    animation_tracker = 0

        elif Knight_ani.ani_array != Animation_Manager.knight_death:
            Knight_ani.Change_array("Idle")
            if prev_Knight_ani != Knight_ani.ani_array:
                animation_tracker = 0
        else:
            Knight_ani.Change_array("Death")

        print(knight.status)

        screen.blit(temp_screen, (0, 0))
        for f in range(0, len(Screen_Manager.object_manager.Objects), 2 ):
            appendable3 = "(" + str(spot3 + 1) + ").png"
            if Screen_Manager.object_manager.Objects[f+1] == True:
                tmp_surface = game.image.load(Screen_Manager.Object_Ani.ani_array[1] + appendable3)
            else:
                tmp_surface = game.image.load(Screen_Manager.Object_Ani.ani_array[1])
            screen.blit(tmp_surface, Screen_Manager.object_manager.Objects[f])


        screen.blit(text_surface, (0, 0))
        screen.blit(knight_surface, (x, 440))

        #Animation tracker is for the knight(player character)
        animation_tracker += 1
        #Animation tracker2 is for the NPCs
        animation_tracker2 += 1
        #Animation tracker3 is for objects like chests and arrows
        if len(Screen_Manager.Object_Ani.ani_array) != 0 and animation_tracker3 == (10 * Screen_Manager.Object_Ani.ani_array[0] - 1):
            knight.status = KStatus.NORMAL
        elif knight.status != KStatus.NORMAL: #for now, I'll have to fiddle with this if I want the arrows to work
            animation_tracker3 += 1

        if x > 1000 or x < 0:
            #Code for switching screens
            temp_screen = Screen_Manager.changeScreen(x)
            interactable = Screen_Manager.Apply_context()

            NPC_Manager.context = Screen_Manager.context
            NPC_Manager.Apply_context()
            #Probably gonna make this a function

            if x > 1000:
                x = 0
            else:
                x = 900

        if animation_tracker >= 99 and Knight_ani.ani_array == Animation_Manager.knight_death:
            animation_tracker = 99

        elif animation_tracker >= (10 * Knight_ani.ani_array[0] - 1):
            animation_tracker = 0

        #This is gonna be an issue eventually
        if len(NPC_Manager.ani_array) != 0 and animation_tracker2 >= (10 * NPC_Manager.ani_array[0] - 1):
            animation_tracker2 = 0







        appendable = "(" + str(spot + 1) + ").png"
        if len(NPC_Manager.ani_array) != 0:
           appendable2 = "(" + str((spot2 + 1) % NPC_Manager.ani_array[0] + 1) + ").png"



        knight_surface = game.image.load(Knight_ani.ani_array[1] + appendable)
        for z in range(len(NPC_Manager.NPCs)):
            NPC_Manager.Change_array(NPC_Manager.NPCs[z])
            screen.blit(game.image.load(NPC_Manager.ani_array[1] + appendable2), (NPC_Manager.ani_array[0], 500))

    pygame.display.update()
    clock.tick(60)



