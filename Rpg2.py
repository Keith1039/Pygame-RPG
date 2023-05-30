import pygame as game
from sys import exit
import Animation_Manager
import Knight
from Knight import KStatus
import managers


interact_functions = {}
# Make this hard coded for now
mockDialogEvent = managers.Event(None, "Dialogue","event_text/Test_dialogue.txt")
def draw_dialogue(dialogueTimer, font):
    text = dialogueManager.prevText
    if dialogueTimer % 180 == 0:
        text = dialogueManager.get_text()
    textSurface = font.render(text, False, "Red")
    if dialogueManager.portrait != None:
        nameSurface = font.render(dialogueManager.name, False, "Red")
        screen.blit(dialogueManager.characterBox, (0, 650))
        screen.blit(dialogueManager.portrait, (15, 670))
        screen.blit(nameSurface, (20, 620))
        screen.blit(dialogueManager.textBox, (120, 650))
        screen.blit(textSurface, (140, 670))
    else:
        #This way there's no awkward space where the portrait used to be.
        screen.blit(dialogueManager.textBox, (0, 650))
        screen.blit(textSurface, (20, 670))
    #There is an easier way to do this but it makes my eyes bleed so no :)
    return text != ""

#I should have an array of sprite managers and it goes through them
game.init()
screen = game.display.set_mode((1422, 800))
clock = game.time.Clock()
game.display.set_caption("Legend of Zeroes, Trails of Cold Meals")
font = game.font.Font('font/Pixeltype.ttf', 50)

#Hero Object
knight = Knight.Knight("Rion", 1, 2, "sword", 1, 1, 1, 1, 1, 1, 1, 1)

#Think I'll go for the 1422 x 800 route from now on
tempScreen = game.image.load("Background_Art/gothic_chapel_portfolio_1422x800.png")
textSurface = font.render("Checking", False, "Red")
knightSurface = game.image.load("Knight/Cut_Sprites/Attack_1 (1).png")

knightAni = Animation_Manager.AnimationManager()
knightAni.change_array("Knight Attack")
NPCManager = managers.NPCAnimationManager()
prevKnightAni = []

temporary = game.image.load("portraits/Knight.png")
animationTracker = 0
animationTracker2 = 0
animationTracker3 = 0
dialogueTimer = 0

#An array filled with spots where the treasure chests are. Dictated by Screen Manager
#Interactable also applies to npcs so yeah.

x = 500
screenManager = managers.ScreenManager(tempScreen)
dialogueManager = managers.DialogueManager()

interactables = screenManager.interactables
textEnable = True #For the purposes of this test

while True:
    #print(x)
    spot = animationTracker // 10
    spot2 = animationTracker2 // 10
    spot3 = animationTracker3 // 10
    if knight.status == KStatus.DEAD:
        knightAni.change_array("Death")


    for event in game.event.get():
        if event.type == game.QUIT:
            game.quit()
            exit()

    # Changing animations

    # Get's the players key input
    keys = game.key.get_pressed()

    # Determines players overworld movement
    if knight.status != KStatus.IN_COMBAT:
        prevKnightAni = knightAni.aniArray
        if knight.status == KStatus.NORMAL:
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

            elif keys[game.K_UP]:
                for u in range(len(interactables)):
                    status = knight.status
                    interactable = interactables[u]
                    if interactable.eventType == "Chest":
                        screenManager.objectAni.change_tuple(knight, x, interactable)
                        if status != knight.status:
                            #resetting animationTracker
                            animationTracker3 = 0
                    elif interactable.eventType == "Dialogue":
                        textEnable = True
                        knight.status = KStatus.IN_CUTSCENE
                        # Do something
                        
                        #print("Triggered")
                    
                    screenManager.objectAni.change_tuple(knight, x, interactable)
                    if status != knight.status:
                        #resetting animationTracker
                        animationTracker3 = 0

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

        ##print(knight.status)

        screen.blit(tempScreen, (0, 0))
        #screen.blit(temporary, (100, 550))

        for f in range(0, len(screenManager.objects), 2):
            appendable3 = "(" + str(spot3 + 1) + ").png"
            if screenManager.objects[f+1] == True:
                tmpSurface = game.image.load(screenManager.objectAni.aniTuple[1] + appendable3)

            else:
                tmpSurface = game.image.load(screenManager.objectAni.aniTuple[1])
            screen.blit(tmpSurface, screenManager.objects[f])


        screen.blit(textSurface, (0, 0))
        screen.blit(knightSurface, (x, 440))
        #Code for testing the dialogueManager
        if textEnable == True:
            if dialogueManager.file == None:
                dialogueTimer = 180
                dialogueManager.load_file(mockDialogEvent)
            textEnable = draw_dialogue(dialogueTimer, font)
            dialogueTimer += 1
        else:
            dialogueTimer = 0

        #Animation tracker is for the knight(player character)
        animationTracker += 1
        #Animation tracker2 is for the NPCs
        animationTracker2 += 1
        #Animation tracker3 is for objects like chests and arrows
        if len(screenManager.objectAni.aniTuple) != 0 and animationTracker3 == (10 * screenManager.objectAni.aniTuple[0] - 1):
            knight.status = KStatus.NORMAL

        elif knight.status != KStatus.NORMAL: #for now, I'll have to fiddle with this if I want the arrows to work
            animationTracker3 += 1

        if x > 1000 or x < -280:
            # Code for switching screens
            prev_screen = screenManager.screen
            tempScreen = screenManager.change_screen(x)
            interactable = screenManager.interactables

            NPCManager.apply_context(screenManager.context)

            # You only change screens when the conditions are met, else you run in place
            if x > 1000 and prev_screen != screenManager.screen:
                x = 0
            elif x < -280 and prev_screen != screenManager.screen:
                x = 900
            else:
                if x > 1000:
                    x = 1000
                else:
                    x = -280

        if animationTracker >= 99 and knightAni.aniArray == Animation_Manager.knightDeath:
            animationTracker = 99

        elif animationTracker >= (10 * knightAni.aniArray[0] - 1):
            animationTracker = 0

        #This is gonna be an issue eventually
        if len(NPCManager.aniTuple) != 0 and animationTracker2 >= (10 * NPCManager.aniTuple[0] - 1):
            animationTracker2 = 0

        appendable = "(" + str(spot + 1) + ").png"

        knightSurface = game.image.load(knightAni.aniArray[1] + appendable)
        for z in range(len(NPCManager.NPCs)):
            NPCManager.change_tuple(NPCManager.NPCs[z])
            appendable2 = "(" + str((spot2 + 1) % NPCManager.aniTuple[0] + 1) + ").png"
            screen.blit(game.image.load(NPCManager.aniTuple[1] + appendable2), (NPCManager.aniTuple[0], 500))

    game.display.update()
    clock.tick(60)

