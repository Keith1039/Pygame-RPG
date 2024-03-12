import pygame as game
from sys import exit
import managers
import Entity

def display_frame_rate(font, screen):
    fps = font.render("FPS: " + str(int(clock.get_fps())), False, "Red")
    screen.blit(fps, (1300, 0))

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
    elif knightAni.aniArray != Entity.Animation_Manager.knightDeath:
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
        saveManager.quick_save()  # Needs to be error checked

    elif keys[game.K_l]:
        saveManager.quick_load()  # Needs to be error checked
        NPCManager.apply_context(screenManager.context)  # Updates NPC Animation Manager when loading save

    elif keys[game.K_b]:
        # start a battle
        battleManager.enemies.clear()  # clear the enemies
        for i in range(2):
            battleManager.add_enemy(entityFactory.create_entity("dummy"))
        battleManager.battleState = (True, "")
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
mockJson = {"eventType": "Dialogue", "path": "event_text/Test_dialogue.txt"}
mockDialogEvent = managers.Event(mockJson)

# I should have an array of sprite managers and it goes through them
game.init()
screen = game.display.set_mode((1422, 800))
clock = game.time.Clock()
game.display.set_caption("Legend of Zeroes, Trails of Cold Meals")
font = game.font.Font('font/Pixeltype.ttf', 50)

# Hero Object
knight = Entity.Knight()

# Think I'll go for the 1422 x 800 route from now on
tempScreen = game.image.load("Background_Art/gothic_chapel_portfolio_1422x800.png")
knightSurface = game.image.load("Knight/Cut_Sprites/Attack_1 (1).png")

knightAni = Entity.AnimationManager()
knightAni.change_array("Knight Attack")
NPCManager = managers.NPCAnimationManager()
prevKnightAni = []

animationTracker = 0
animationTracker2 = 0
animationTracker3 = 0

start = True

# An array filled with spots where the treasure chests are. Dictated by Screen Manager
# Interactable also applies to npcs so yeah.

x = 500
entityFactory = Entity.EntityFactory()
screenManager = managers.ScreenManager(tempScreen)
dialogueManager = managers.DialogueManager(font, screen)
saveManager = managers.SaveManager(knight, vars(), screenManager)
battleManager = Entity.BattleManager(knight)
UIManager = managers.UIManager(font, screen)
UIHandler = managers.UIHandler(UIManager, saveManager, knight, vars(), battleManager)

interactables = screenManager.interactables
textEnable = True  # For the purposes of this test
buffered_move = ""  # for battlemanager
target = ()  # for battlemanager

screenManager.change_context("Start")
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
    if start:
        screen.blit(screenManager.screen, (0, 0))
        context, choice = UIManager.draw_UI(eventList)
        UIHandler.handle_interaction(context, choice)
        if not start and choice == "Start Game":  # If it's not start game then context was already changed
            screenManager.change_context("Background1")
    else:
        # Determines players overworld movement
        if not battleManager.battleState[0] and battleManager.battleState[1] == "":
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

            elif knight.Status != "Normal" and knight.Status != "Dead":
                # Fine for now but this needs to be fixed
                animationTracker3 += 1

            x = change_screen(x, screenManager, NPCManager)

            # Here to stop death animation from looping
            if animationTracker >= 99 and knightAni.aniArray == Entity.Animation_Manager.knightDeath:
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
        elif battleManager.battleState[0]:
            screen.blit(screenManager.screen, (0, 0))  # draw the screen
            # draw the knight object here

            # if this condition is ever true that means that the player used a move last turn
            # and the values need to be reset
            if buffered_move != "" and target != ():
                buffered_move = ""
                target = ()
            if len(battleManager.turnOrder) == 0:
                battleManager.reset_turn_order()
            if battleManager.turnOrder[0] == knight:
                if UIManager.UI is None:
                    UIManager.change_UI("Player Select")  # Change the UI to the proper UI
                context, choice = UIManager.draw_UI(eventList)
                UIHandler.handle_interaction(context, choice)
                if battleManager.moveDict.get(choice) is not None:  # See if the move selected is a valid move
                    buffered_move = choice  # set the buffered move
                if isinstance(choice, tuple):
                    target = choice
                    UIManager.change_UI(None)
            returnable_strings = battleManager.do_one_turn(buffered_move, target)
            # if len(returnable_strings) != 0:
            # integrate dialogue manager here
            # print(returnable_strings)
            battleManager.determine_battle_state()  # checks to see if the battle state has changed
        elif not battleManager.battleState[0] and battleManager.battleState[1] != "":
            # this means the battle ended and its result needs to be processed
            battleResult = battleManager.battleState[1]
            if battleResult == "Hero Wins":
                knight.get_rewards(battleManager.lootPool)
                # reset lootpool
                battleManager.lootPool = {
                    "Exp": 0,
                    "Money": 0,
                    "Items": {

                    }

                }
                knight.Status = "Normal"  # reset Knight's status to normal
            elif battleResult == "Hero Loses":
                # send them back to the start menu and reset their player character?
                pass
            battleManager.battleState = (False, "")
        UIManager.draw_health_bar(knight)
        display_frame_rate(font, screen)
    game.display.update()
    clock.tick(60)

