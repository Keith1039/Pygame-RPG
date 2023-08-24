import pygame as game
from sys import exit
import Animation_Manager
import Knight
import managers

def display_frame_rate(font, screen):
    fps = font.render("FPS: " + str(int(clock.get_fps())), False, "Red")
    screen.blit(fps, (0, 0))

# function that deals with player movement
def handle_basic_input(keys, knightAni, knight, x, animationTracker): # This is just movement for left and right
    # Determines players overworld movement
    prevKnightAni = knightAni.aniArray
    if knight.Status == "Normal":
        if keys[game.K_RIGHT]:
            knightAni.change_array("Knight Run R")
            if prevKnightAni != knightAni.aniArray:
                animationTracker = 0

            else:
                x += 4

        elif keys[game.K_LEFT]:
            knightAni.change_array("Knight Run L")
            if prevKnightAni != knightAni.aniArray:
                animationTracker = 0

            else:
                x -= 4
        else:
            knightAni.change_array("Idle")
            if prevKnightAni != knightAni.aniArray:
                animationTracker = 0
    elif knightAni.aniArray != Animation_Manager.knightDeath:
        knightAni.change_array("Idle")
        if prevKnightAni != knightAni.aniArray:
            animationTracker = 0

    else:
        knightAni.change_array("Death")
    return x, animationTracker

def handle_player_interaction(keys, knight, saveManager, screenManager, NPCManager, textEnable, animationTracker3):
    if keys[game.K_UP]:
        for u in range(len(interactables)):
            status = knight.Status
            interactable = interactables[u]
            if interactable.eventType == "Chest":
                screenManager.objectAni.change_tuple(knight, x, interactable)
                if status != knight.Status:
                    # resetting animationTracker
                    animationTracker3 = 0
            elif interactable.eventType == "Dialogue":
                textEnable = True
                knight.Status = "In cutscene"
                # Do something

            screenManager.objectAni.change_tuple(knight, x, interactable)
            if status != knight.Status:
                # resetting animationTracker
                animationTracker3 = 0

    elif keys[game.K_s]:
        saveManager.quick_save()

    elif keys[game.K_l]:
        saveManager.quick_load()
        NPCManager.apply_context(screenManager.context)  # Updates NPC Animation Manager when loading save
    return textEnable, animationTracker3

def draw_objects(screen, screenManager, spot3):
    for f in range(0, len(screenManager.objects), 2):
        appendable3 = "(" + str(spot3 + 1) + ").png"
        if screenManager.objects[f + 1]:
            tmpSurface = game.image.load(screenManager.objectAni.aniTuple[1] + appendable3)

        else:
            tmpSurface = game.image.load(screenManager.objectAni.aniTuple[1])
        screen.blit(tmpSurface, screenManager.objects[f])
    # In the future, this will be done automatically with Omni manager

def change_screen(x, screenManager, NPCManager):
    if x > 1000 or x < -280:
        # Code for switching screens
        prev_screen = screenManager.screen
        screenManager.change_screen(x)
        #interactable = screenManager.interactables
        NPCManager.apply_context(screenManager.context)

        # You only change screens when the conditions are met, else you run in place
        if x > 1000 and prev_screen != screenManager.screen:
            x = -260
        elif x < -280 and prev_screen != screenManager.screen:
            x = 980
        else:
            if x > 1000:
                x = 1000
            else:
                x = -280
    return x
interact_functions = {}
# Make this hard coded for now
mockDialogEvent = managers.Event(None, "Dialogue","event_text/Test_dialogue.txt")

# I should have an array of sprite managers and it goes through them
game.init()
screen = game.display.set_mode((1422, 800))
clock = game.time.Clock()
game.display.set_caption("Legend of Zeroes, Trails of Cold Meals")
font = game.font.Font('font/Pixeltype.ttf', 50)

# Hero Object
knight = Knight.Knight()

# Think I'll go for the 1422 x 800 route from now on
tempScreen = game.image.load("Background_Art/gothic_chapel_portfolio_1422x800.png")
knightSurface = game.image.load("Knight/Cut_Sprites/Attack_1 (1).png")

knightAni = Animation_Manager.AnimationManager()
knightAni.change_array("Knight Attack")
NPCManager = managers.NPCAnimationManager()
prevKnightAni = []

animationTracker = 0
animationTracker2 = 0
animationTracker3 = 0

# An array filled with spots where the treasure chests are. Dictated by Screen Manager
# Interactable also applies to npcs so yeah.

x = 500
screenManager = managers.ScreenManager(tempScreen)
dialogueManager = managers.DialogueManager(font, screen)
saveManager = managers.SaveManager(knight, vars(), screenManager)

interactables = screenManager.interactables
textEnable = True  # For the purposes of this test

while True:
    spot = animationTracker // 10
    spot2 = animationTracker2 // 10
    spot3 = animationTracker3 // 10
    if knight.Status == "Dead":
        knightAni.change_array("Death")

    eventList = game.event.get()
    for event in eventList:
        if event.type == game.QUIT:
            game.quit()
            exit()

    # Changing animations

    # Gets the players key input
    keys = game.key.get_pressed()

    # Determines players overworld movement
    if knight.Status != "In Combat":
        # handles basic movement for the player character
        x, animationTracker = handle_basic_input(keys, knightAni, knight, x, animationTracker)
        # handles the player interaction
        textEnable, animationTracker3, = handle_player_interaction(keys, knight, saveManager, screenManager, NPCManager, textEnable, animationTracker3)

        # Draws the objects on the screen
        screen.blit(screenManager.screen, (0, 0))
        draw_objects(screen, screenManager, spot3)
        screen.blit(knightSurface, (x, 440))

        # Code for testing the dialogueManager
        if textEnable:
            if dialogueManager.file is None:
                dialogueManager.load_file(mockDialogEvent)
            textEnable = dialogueManager.draw_dialogue(eventList)

        # Animation tracker is for the knight(player character)
        animationTracker += 1
        # Animation tracker2 is for the NPCs
        animationTracker2 += 1
        # Animation tracker3 is for objects like chests and arrows
        if len(screenManager.objectAni.aniTuple) != 0 and animationTracker3 == (10 * screenManager.objectAni.aniTuple[0] - 1):
            knight.Status = "Normal"

        elif knight.Status != "Normal":  # Fine for now but won't work for the arrows later
            animationTracker3 += 1

        x = change_screen(x, screenManager, NPCManager)

        # Here to stop death animation from looping
        if animationTracker >= 99 and knightAni.aniArray == Animation_Manager.knightDeath:
            animationTracker = 99

        # if the end is reached, loop over for knight
        elif animationTracker >= (10 * knightAni.aniArray[0] - 1):
            animationTracker = 0

        # This will need to be changed to support multiple NPCs
        if len(NPCManager.aniTuple) != 0 and animationTracker2 >= (10 * NPCManager.aniTuple[0] - 1):
            animationTracker2 = 0
        # Load Knight image
        appendable = "(" + str(spot + 1) + ").png"
        knightSurface = game.image.load(knightAni.aniArray[1] + appendable)

        # this needs to be changed for later
        for z in range(len(NPCManager.NPCs)):
            NPCManager.change_tuple(NPCManager.NPCs[z])
            appendable2 = "(" + str((spot2 + 1) % NPCManager.aniTuple[0] + 1) + ").png"
            screen.blit(game.image.load(NPCManager.aniTuple[1] + appendable2), (NPCManager.aniTuple[0], 500))

    display_frame_rate(font, screen)
    game.display.update()
    clock.tick(60)

