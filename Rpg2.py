
import pygame as game
from sys import exit
import managers
import Entity

def display_frame_rate(font, screen):
    fps = font.render("FPS: " + str(int(clock.get_fps())), False, "Red")
    screen.blit(fps, (1300, 0))

# function that deals with player movement
def handle_basic_input(keys, knight): # This is just movement for left and right
    # Determines players overworld movement
    prevAniStatus = knight.aniStatus

    if prevAniStatus != knight.aniStatus:  # check if the animation status is different
        knight.aniTracker = 0
        knight.reset_max_animation_val()  # reset the max animation value

    if knight.fieldStatus == "Normal":
        if keys[game.K_RIGHT]:
            knight.aniStatus = "Run"
            knight.flipped = False
            if prevAniStatus == knight.aniStatus:
                knight.x += 4

        elif keys[game.K_LEFT]:
            knight.aniStatus = "Run"
            knight.flipped = True
            if prevAniStatus == knight.aniStatus:
                knight.x -= 4
        else:
            knight.aniStatus = "Idle"

    elif knight.aniStatus != "Death":
        knight.aniStatus = "Idle"
    else:
        knight.aniStatus = "Death"

def handle_player_interaction(keys, knight, saveManager, screenManager, npcManager):
    if keys[game.K_s]:
        saveManager.quick_save()  # Needs to be error checked

    elif keys[game.K_l]:
        saveManager.quick_load()  # Needs to be error checked
        npcManager.get_NPCs(screenManager.context)

    elif keys[game.K_b]:
        # start a battle
        knight.x = 500  # set the x coord
        knight.y = 300  # set the y coord
        knight.rect.center = (knight.x, knight.y)  # recenter the rect
        battleManager.enemies.clear()  # clear the enemies
        for i in range(2):
            enemy = entityFactory.create_entity("Goblin")  # create an enemy
            entityGroup.add(enemy)  # add the enemy to the sprite group
            battleManager.add_enemy(enemy)  # add an enemy to the battle manager

        knight.Inventory.update({"Potion": 2})  # add a potion
        knight.Inventory.update({"Bomb": 1})  # add a bomb
        battleManager.battleState = (True, "")  # set the battle manager to active


def change_screen(knight, screenManager, npcManager):
    min_x = 50
    max_x = 1350
    if knight.x > max_x or knight.x < min_x:
        # Code for switching screens
        prev_screen = screenManager.screen
        screenManager.change_screen(min_x, max_x, knight.x)

        # You only change screens when the conditions are met, else you run in place
        if prev_screen != screenManager.screen:
            npcManager.get_NPCs(screenManager.context)
            objectManager.get_objects(screenManager.context)
            if knight.x > max_x and prev_screen != screenManager.screen:
                knight.x = min_x
            elif knight.x < min_x and prev_screen != screenManager.screen:
                knight.x = max_x
        else:
            if knight.x > max_x:
                knight.x = max_x
            else:
                knight.x = min_x
interact_functions = {}

# I should have an array of sprite managers and it goes through them
game.init()
screen = game.display.set_mode((1422, 800))
clock = game.time.Clock()
game.display.set_caption("Legend of Zeroes, Trails of Cold Meals")
font = game.font.Font('font/Pixeltype.ttf', 50)

# Hero Object
knight = Entity.Knight()
knight.moveList.append("Double Slash")

# Think I'll go for the 1422 x 800 route from now on
tempScreen = game.image.load("Background_Art/gothic_chapel_portfolio_1422x800.png")



start = True

# An array filled with spots where the treasure chests are. Dictated by Screen Manager
# Interactable also applies to npcs so yeah.

x = 500
entityFactory = Entity.EntityFactory()
screenManager = managers.ScreenManager(tempScreen)
dialogueManager = managers.DialogueManager(font, screen)
questManager = managers.QuestManager(knight)
eventManager = managers.EventManager(knight, dialogueManager, questManager)
npcManager = Entity.NPCManager(knight)
objectManager = Entity.ObjectManager(knight)
saveManager = managers.SaveManager(knight, vars(), screenManager, eventManager, questManager, npcManager, objectManager)
itemManager = managers.ItemManager(knight)
animationManager = Entity.AnimationManager(screen)
battleManager = Entity.BattleManager(knight, itemManager, animationManager)
uiManager = managers.UIManager(font, screen)
uiHandler = managers.UIHandler(uiManager, saveManager, knight, vars(), battleManager, itemManager)




eventManager.push_event("mockDialogue")

interactables = screenManager.interactables
buffered_move = ""  # for battlemanager
targets = []  # for battlemanager

entityGroup = game.sprite.Group(knight)  # make a sprite group

screenManager.change_context("Start")
while True:
    if knight.fieldStatus == "Dead":
        knight.aniStatus = "Dead"

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
        context, choice = uiManager.draw_UI(eventList)
        uiHandler.handle_interaction(context, choice)
        if not start and choice == "Start Game":  # If it's not start game then context was already changed
            screenManager.change_context("Background1")
            npcManager.get_NPCs(screenManager.context)  # get NPCs for this context
            objectManager.get_objects(screenManager.context)  # get objects for this context change
    else:
        eventManager.process_events(screenManager.context)  # process any outstanding events before the game code
        screen.blit(screenManager.screen, (0, 0))
        # Determines players overworld movement
        if not battleManager.battleState[0] and battleManager.battleState[1] == "":
            # handles basic movement for the player character
            handle_basic_input(keys, knight)
            # handles the player interaction
            handle_player_interaction(keys, knight, saveManager, screenManager, npcManager)

            # Draws the objects on the screen

            # draw the rectangle around objects
            # for sprite in objectManager.interactableGroup.sprites():
            #     game.draw.rect(screen, (150, 150, 150), sprite.rect)
            objectManager.interactableGroup.update()  # update object sprites
            objectManager.interactableGroup.draw(screen)  # draw the sprites

            # draw the rectangle around NPCs
            # for sprite in npcManager.interactableGroup.sprites():
            #     game.draw.rect(screen, (150, 150, 150), sprite.rect)
            npcManager.interactableGroup.update()  # update sprites
            npcManager.interactableGroup.draw(screen)  # draw the NPCs

            # draw the rectangle behind entities
            # for sprite in entityGroup.sprites():
            #     game.draw.rect(screen, (255, 0, 0), sprite.rect)
            entityGroup.update()  # update all the sprites in the group
            entityGroup.draw(screen)  # draw all the sprites

            collidingSprite = npcManager.get_colliding()  # the NPC that the player can interact with
            event = npcManager.get_interaction_event(eventList)  # should only ever be one event at a time
            if event is not None:  # check if there is an event to push
                eventManager.push_event(event)  # push the event

            # collidingObject = objectManager.get_colliding()  # the object the player is colliding with
            event = objectManager.get_interaction_event(eventList)  # should only ever be one event at a time
            if event is not None:  # check if there's an event to push
                eventManager.push_event(event)  # push the vent

            # Code for testing the dialogueManager
            if dialogueManager.event is None and len(dialogueManager.nextEvents) > 0:
                dialogueManager.get_new_text()  # queue up the next event
            if dialogueManager.event is not None:
                dialogueManager.draw_dialogue(eventList)  # draw the dialogue

            change_screen(knight, screenManager, npcManager)

        elif battleManager.battleState[0]:
            # draw the knight object here
            # if this condition is ever true that means that the player used a move last turn
            # and the values need to be reset

            if animationManager.active:
                animationManager.process_action()  # process all of this
                # check if the dialogue manager is active
                if len(dialogueManager.dialogue) > 0:
                    dialogueManager.draw_dialogue(eventList, True)
                    # when we're done reading through the dialogue, check battle state
                    if len(dialogueManager.dialogue) == 0:
                        battleManager.determine_battle_state()  # checks to see if the battle state has changed
                if not animationManager.active:  # check to see if the animation manager was just de-activated
                    battleManager.determine_battle_state()  # checks to see if the battle state has changed
            else:
                entityGroup.update()  # update the entities
                entityGroup.draw(screen)  # draw the entities
                if buffered_move != "" and len(targets) == battleManager.targetNum:
                    buffered_move = ""  # reset the move string
                    targets.clear()  # remove the targets from the list
                    battleManager.targetNum = -1  # set target number to -1 (invalid number)
                if len(battleManager.turnOrder) == 0:
                    battleManager.reset_turn_order()
                if battleManager.turnOrder[0] == knight:
                    if uiManager.UI is None:
                        uiManager.change_UI("Player Select")  # Change the UI to the proper UI
                    context, choice = uiManager.draw_UI(eventList)
                    uiHandler.handle_interaction(context, choice)
                    # See if the move selected is a valid move
                    if battleManager.moveDict.get(choice) is not None or itemManager.itemJson.get(choice) is not None:
                        buffered_move = choice  # set the buffered move
                        if battleManager.moveDict.get(choice) is not None:
                            battleManager.set_target_number(choice)
                        else:
                            battleManager.targetNum = 1
                    elif isinstance(choice, tuple):
                        if len(battleManager.enemies) > 1:  # we don't assume anything
                            targets.append(choice)  # add the choice to the tuple
                        elif len(battleManager.enemies) == 1:  # if there is 1 enemy assume all hits target them
                            for i in range(battleManager.targetNum):
                                targets.append(choice)
                        if len(targets) == battleManager.targetNum:  # check if we should leave targeting screen
                            uiManager.change_UI(None)
                returnable_strings, refresh = battleManager.do_one_turn(buffered_move, targets)
                if refresh:
                    uiManager.subMenuItems = itemManager.get_usable_items()  # refresh displayed
                    uiManager.subMenuMaxIndex = len(uiManager.subMenuItems) - 1
                    if uiManager.subMenuSlider >= len(uiManager.subMenuItems) and len(uiManager.subMenuItems) != 0:
                        uiManager.subMenuSlider -= 1  # move slider back by 1
                if len(returnable_strings) != 0:
                    # load the event strings into the dialogue list
                    dialogueManager.load_dialogue_list(returnable_strings)
        elif not battleManager.battleState[0] and battleManager.battleState[1] != "":
            entityFactory.clear_created_count()  # clear the dictionary
            # this means the battle ended and its result needs to be processed
            battleResult = battleManager.battleState[1]
            if battleResult == "Hero Wins":
                entityGroup = game.sprite.Group(knight)  # reset the entity group
                # reset to default positions
                knight.x = knight.default_x
                knight.y = knight.default_y
                knight.get_rewards(battleManager.lootPool)
                # reset lootpool
                battleManager.lootPool = {
                    "Exp": 0,
                    "Money": 0,
                    "Items": {

                    }

                }
                knight.fieldStatus = "Normal"  # reset Knight's status to normal
            elif battleResult == "Hero Loses":
                # send them back to the start menu and reset their player character?
                pass
            battleManager.battleState = (False, "")
        uiManager.draw_health_bar(knight)
        display_frame_rate(font, screen)
    game.display.update()
    clock.tick(60)

