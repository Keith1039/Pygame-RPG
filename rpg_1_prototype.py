from cmath import phase
import math
import random

weapons={"sword":10,"poisoned sword":12,"silver sword":20,"rusty dagger":1,"poisoned rusty dagger":2,"lance":5,"silver lance":10,"???":999999,"unarmed":3}
items_shop_list=["old map", "old bread","potion"]
items_shop={"old map":1000,"old bread":50,"potion":150,"moonstone":300,"silver polish":50}
items_sell={"sword":100, "lance":80,"old bread":10, "potion":50, "rusty dagger":20,"silver lance":100,"silver sword":150}
books = ['Gospel of the dragons',"History book" "Ruined journal #1","Ruined journal #2", "Ruined journal #3", "Demons", "old book", "Items"]
items={"Volitile Poison","silver polish","emblem","moonlit map",'Gospel of the dragons', "Ruined journal #1","Ruined journal #2", "Ruined journal #3", "Werewolf tooth"
"Demons", "old book","History book", "Items","moonstone","basement key", "upstairs key"}
combinable_items=["Volitile poison", "silver polish","lance", "rusty dagger", "sword", "old map", "moonstone"]
consumable_item={"old bread":20,"potion":50}
inventory=[]



#counts
fight_counter=[1] #fixed
ruined_castle_flag=[1] #fixed
potion_flag=[1] #fixed
combine_menu=[1] #fixed
descriptions_menu=[1] #fixed
main_menu_count=[1] #fixed
equip_menu_count=[1] #fixed
shopkeeper_count=[1] #fixed
shopkeeper_hint=[1] #fixed
werewolf_clue1=[1] #fixed
werewolf_clue2=[1] #fixed
werewolf_clue3=[1] #fixed
werewolf_hints=[] #fixed
inn_count=[1]

#dungeon 1 item checks
book3_flag=[]
book1_flag=[]
book2_flag=[]
book8_flag=[]
potion_flag=[]
Volitile_poison_flag=[]

#town
town_phase=[1]
final_flag=[]

#dream flags
memory_frag1_flag=[]
memory_frag2_flag=[]
memory_frag3_flag=[]


#boss kill checks
Minotaur_kill_count=[]
werewolf_kill_count=[]
Gargoyle_kill_count=[]

#boss specials
werewolf_special=[]
gargoyle_special=[]

#Gargoyle stuff
action_count=[]
first_encounter=[]

#Dungeon 2 item_check
book4_flag=[]
book5_flag=[]
book6_flag=[]

potion1_flag=[]
potion2_flag=[]
potion3_flag=[]
basement_key_flag=[]
upstairs_key_flag=[]


#Combat_Tutorial.txt
def combat_tutorial():
    input("In a world full of monsters knowing how to fight is essential!")
    input("When a fight starts there's no stopping until one of you is dead so try your best!")
    input("Luckily for you most enemies are lone wolves, meaning you only have to deal with one at a time!")
    input("In combat, there are three options. Attack, defend and item.")
    input("Attack, well, attacks your enemy dealing damage based on your attack and their defence.")
    input("Defence braces your character to receive an attack, halving the potential damage. Knowing when to defend is a crucial way to stay alive.")
    input("Item let's you use the consumable items in your inventory. This is your go to way to heal. Scarfing down bread and potions in a fight is crucial to survival!")
    input("Who attacks first depends on your agility stats. If your enemy is faster they'll go first. If not, you'll go first.")
    input("The turn order matters for the attack and item options.")
    input("If you're slower than your opponent that means that you'll attack second or heal second so be careful.")
    input("regardless of who goes first you'll always get your defence off so when you think you're in danger don't hesitate to defend!")
    input("Goodluck and try not to die!")

#Combine_Tutorial.txt
def combine_tutorial():
    input("Various items that you find might have other uses.")
    input("In this menu, two items can be combined to create another item.")
    input("2 seemingly useless items can combine to create a key item that is required to continue on.")
    input("In order to beat this game be sure to alwaydies try to combine anything and everything.")
    input("Even if two items don't end up making anything, you won't lose them by trying so go wild.")
    input("Items are only consumed when a new item is succesfully created.")

#Descritptions_Tutorial.txt
def descriptions_tutorial():
    input("Item descriptions can help you understand the potential uses for an item.")
    input("Some items need to be examined in this menu in order for certain events to trigger.")
    input("This menu is also how you read the various books you collect throughout your journey.")
    input("Books can contain clues as to how to progress and the current setting.")
    input("Be sure to frequently check this menu!")

#Main_Menu_Tutorial.txt
def main_menu_tutorial():
    input("The main menu is where you go to use items, equip items, combine items and examine items.")
    input("Each function has it's on separate tutorial so feel free to explore each option!")

#Equip_Tutorial.txt
def equip_tutorial():
    input("Here the player character can change their equipment.")
    input("For the purposes of the setting you may only change your weapon for now.")




class Hero:
    def __init__(self,name,level,strenth,vitality,Hp,HPcap,agility,magic,defence,weapon,chestplate,gauntlets,
    pants,exp,expcap,money):
        self.Hp=Hp
        self.name=name
        self.str=strenth
        self.weapon=weapon
        self.attck=strenth+weapons[weapon]
        self.vit=vitality
        self.agl=agility
        self
        self.mag=magic
        self.defence=defence+chestplate+gauntlets+pants
        self.exp=exp
        self.expcap=expcap
        self.Hp=Hp
        self.Hpcap=HPcap
        self.bal=money
        self.lvl=level

    def level_up(self):
        growths = (2,5,1,1,3)
        print(self.name+" "+"has leveled up!")
        self.str = self.str+(growths[0])
        self.vit= self.vit+(growths[1])
        self.agl= self.agl+(growths[2])
        self.mag= self.mag+(growths[3])
        self.defence=self.defence+(growths[4])
        self.Hp=self.Hp+((self.vit*2))
        self.Hpcap=self.Hpcap+(self.vit*2)
        self.lvl=self.lvl+1
    
    def victory(self,enemy):
        print(str(self.name)+' '+ "Won!")
        print(self.name+' '+ "gained"+' '+ str(enemy.exp)+"XP")
        print(enemy.name +' '+"dropped"+' '+str(enemy.drop)+' '+"Gold")
        self.bal = self.bal+enemy.drop
        self.exp=self.exp+enemy.exp
    
    def level_up_sequence(self):
        while self.exp >= self.expcap:
            self.level_up()
            self.expcap = self.expcap+100
            self.exp=self.exp-self.expcap
        if self.exp < 0:
            self.exp = 0
    
    def fight(self,enemy):
        while self.Hp >0 and enemy.vit >0:
            combat_options=self.combat_options()
            self.option_result(combat_options,enemy)
        if self.Hp > 0:
            self.victory(enemy)
            if self.exp >= self.expcap:
                self.level_up_sequence()
        else:
            print(enemy.name+' '+ "Won!")
            print("Game over")
    
    def attack(self,enemy):
        damage = (self.attck-enemy.defence)
        if damage  > 0:
            input(enemy.name+' '+ "lost" + ' ' + str(damage)+" "+"HP!")
            enemy.vit = enemy.vit-damage
        elif damage <= 0:
             input(enemy.name+' '+"received 0 damage!")

    def defend(self,enemy):
        input(self.name+' '+"braced for an attack!")
        damage = (enemy.attck-self.defence)
        if damage > 0:
            input(self.name+' '+"blocked the blow!")
            input(self.name + ' '+ "took"+' '+str((damage//2))+' '+"damage")
            self.Hp = self.Hp-(damage//2)
        elif damage <= 0:
            input(self.name+"blocked the blow but it was too weak to even damage him!")
            input(self.name+' '+"took 0 damage!")

    def take_damage(self,enemy):
        damage=(enemy.attck-self.defence)
        if damage  > 0:
            input(self.name+' '+ "lost" + ' ' + str(damage)+" "+"Hp!")
            self.Hp = self.Hp-damage
        elif damage <= 0:
             input(self.name+' '+"received 0 damage!")
    
    def items(self,consumable_item,inventory):
            check = True
            
            while check == True:
                applicable_items=[]
                check1=0
                for i in range(len(inventory)):
                    if (inventory[i] in consumable_item) == True:
                        applicable_items.append(inventory[i])
                        
                if len(applicable_items) ==0:
                    input("You do not have any items that can be used")
                    check = False
                else:
                    while check == True:
                        confirm = input("What item would you like to use?: ")
                        confirm=confirm.strip()
                        while (confirm in consumable_item) != True and confirm != "5":
                            confirm = input("What item would you like to use?: ")
                            confirm = confirm.strip()
                        if (confirm in inventory) == True:
                            input(self.name+' '+ "used"+' '+ confirm)
                            print(self.name+' '+"recovered"+' '+ str(consumable_item[confirm])+' '+"Hp")
                            self.Hp = self.Hp+consumable_item[confirm]
                            inventory.remove(confirm)
                            if self.Hp > self.Hpcap:
                                self.Hp = self.Hpcap
                        elif confirm == "5":
                            check = False
                        else:
                            print("you don't have that item.")

        
    def rest(self):
        self.Hp=self.Hpcap
        input(self.name+':'+' '+"That was a nice nap. I feel better.")
        input(self.name+' '+'has recovered all their Hp!')

    def combat_options(self):
            print("1: Attack")
            print('2: Defend')
            print('3: Item')
            combat_options = input("What will you do?: input the number corresponding to your choice.")
            while combat_options != "1" and combat_options != "2" and combat_options != "3":
                combat_options = input("What will you do?: input the number corresponding to your choice.")
            return(combat_options)

    def option_result(self,combat_options,enemy):
        if combat_options == "1" and (enemy.agl <= self.agl):
            self.attack(enemy)
            if enemy.vit > 0:
                damage=enemy.special(self)
                enemy.process(self,damage)
        elif combat_options == "1" and (enemy.agl > self.agl):
            damage=enemy.special(self)
            enemy.process(self,damage)
            if self.Hp > 0:
                self.attack(enemy)
        elif combat_options == "2":
            input("You brace for an attack")
            damage=enemy.special(self)
            damage = damage//2
            enemy.process(self,damage)
        elif combat_options == "3" and (enemy.agl <= self.agl):
            self.items(consumable_item,inventory)
            damage=enemy.special(self)
            enemy.process(self,damage)
        elif combat_options == "3" and (enemy.agl > self.agl):
            damage=enemy.special(self)
            enemy.process(self,damage)
            if self.Hp > 0:
                self.items(consumable_item,inventory)

            
            

    '''
    def combat_options(self,enemy):
            print("1: Attack")
            print('2: Defend')
            print('3: Item')
            combat_options = input("What will you do?: input the number corresponding to your choice.")
            while combat_options != "1" and combat_options != "2" and combat_options != "3":
                combat_options = input("What will you do?: input the number corresponding to your choice.")
            if self.agl >= enemy.agl:
                if combat_options == "1":
                    self.attack(enemy)
                    if enemy.vit > 0:
                        self.take_damage(enemy)
                elif combat_options == "2":
                    self.defend(enemy)
                elif combat_options == "3":
                    self.items(consumable_item,inventory)
                    self.take_damage(enemy)
            else:
                if combat_options == "1":
                    self.take_damage(enemy)
                    if self.Hp > 0:
                        self.attack(enemy)
                elif combat_options == "2":
                    self.defend(enemy)
                elif combat_options == "3":
                    self.take_damage(enemy) 
                    if self.Hp > 0:
                        self.items(consumable_item,inventory)
    '''
    def combat_options_special(self,enemy):
        print("1: Overlimit")
        combat_options = input("What will you do?: input the number corresponding to your choice.")
        while combat_options != "1":
            combat_options = input("What will you do?: input the number corresponding to your choice.")
        print("1: Dead end")
        combat_options = input("What will you do?: input the number corresponding to your choice.")
        while combat_options != "1":
            combat_options = input("What will you do?: input the number corresponding to your choice.")
        input("your body moves by instinct.")
        input("in an instant 10 slashes are unleashed.")
        dead_end=(weapons[self.weapon]*(self.str//50))
        total=0
        for i in range(10):
            damage=dead_end-enemy.defence
            total+=dead_end-enemy.defence
            enemy.vit= enemy.vit-damage
            print("Fafnir took "+str(damage)+' '+"damage!")
        

    def get_book1(self):
        if len(book1_flag) == 0:
            input("there is an old book on the ground. You decided to pick it up.")
            input(self.name+' '+"got an old book")
            inventory.append("old book")
            input(self.name+':'+" "+"This may come in handy.")
            book1_flag.append(1)
    
    def get_book2(self):
        if len(book2_flag) == 0:
            input("there is a book titled, 'Demons: A Pocket Guide to Humanities Greatest Enemies', on the ground. You decided to pick it up")
            input(self.name+' '+ "got 'Demons: A Pocket Guide to Humanities Greatest Enemies'")
            inventory.append("Demons")
            input(self.name+':'+' '+"Demons? Is that the name of the things I've been fighting.")
            input(self.name+':'+" "+"Guess it wouldn't hurt to give this a read later.")
            book2_flag.append(1)

    def get_book3(self):
        if len(book3_flag) == 0:
            input("There is a book titled 'Items: An Adventurer's best friend! on the ground. You decided to pick it up. ")
            input(self.name+' '+"got 'Items: An Adventurer's best friend!'")
            inventory.append("Items")
            input(self.name+':'+" "+"This book seems to be about items. Maybe I should read it later.")
            book3_flag.append(1)
    def get_book8(self):
        if len(book8_flag)==0:
            input("There is a withered textbook on the ground. It seems to be a history book.")
            input(self.name+' '+"got History book")
            inventory.append("History book")
            input(self.name+':'+" "+"I don't know much about this world. Maybe I should read some of this.")
            book8_flag.append(1)

    def get_Volitile_poison(self):
        if len(Volitile_poison_flag) == 0:
            input("You stumble upon a jar with some green liquid")
            input("The label identifies it as a sort of corrosive poison")
            input(self.name+':'+' '+"'I definitely don't want this to end up on me.'")
            input(self.name+':'+' '+"'Still, it has it's uses. I should take it with me just in case.'")
            input(self.name+' '+"got Volitile poison!")
            inventory.append("Volitile poison")
            print(inventory)
            Volitile_poison_flag.append(1)

    def get_potion(self):
        if len(potion_flag) == 0:
            input("You find a bottle with red fluid.")
            input(self.name+':'+" ""I recognize this... this is... medicine?")
            input(self.name+':'+' '+"......")
            input(self.name+':'+' '+"If it really is medicine.. I have to bring it along.")
            input(self.name+' '+"got potion!")
            inventory.append("potion")
            potion_flag.append(1)
    
    def resting_spot(self):
        input("You find a place where there's no monsters")
        input(self.name+':'+' '+"This may be a good place to rest.")
        confirmation = input("Will you rest? yes/no ")
        confirmation = confirmation.strip()
        while confirmation != "yes" and confirmation != "no":
           confirmation = input("Will you rest? yes/no ")
           confirmation=confirmation.strip()
        if confirmation == "yes":
            self.rest()
        else:
            input(self.name+':' +' '+"I don't need to rest right now.")
    
    def movement_minotaur_dungeon(self,x_pos,y_pos):
        if (x_pos == 0 and y_pos == 0) or (x_pos == 1 and y_pos == 3):
            print("1: Move forward")
            print("2: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2":
                print("1: Move forward")
                print("2: Main menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved forward")
                y_pos+=1
            elif decision == "2":
                self.main_menu(main_menu_count)

        elif x_pos == 0 and y_pos == 1:
            print("1: Move to the right")
            print("2: Move to the left")
            print("3: Move backwards")
            print("4: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3" and decision != "4":
                print("1: Move to the right")
                print("2: Move to the left")
                print("3: Move backwards")
                print("4: Main menu")     
                decision = input("What will you do? ")  
                decision = decision.strip() 
            if decision == "1":
                print("You moved to the right")
                x_pos+=1   
            elif decision == "2":
                print("You moved to the left")
                x_pos-=1
            elif decision == "3":
                print("you went backwards")
                y_pos-=1
            elif decision == "4":
                self.main_menu(main_menu_count)
        
        elif (x_pos ==-1 and y_pos == 2) or (x_pos ==-1 and y_pos == 3) or (x_pos ==3 and y_pos == 2) or (x_pos ==3 and y_pos == 3) or (x_pos ==3 and y_pos == 4) or (x_pos ==3 and y_pos == 5):
            print("1: Move forward")
            print("2: Move backwards")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move forward")
                print("2: Move backwards")
                print("3: Main menu")   
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved forward")
                y_pos+=1
            elif decision == "2":
                print("You moved backwards")
                y_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)

        elif (x_pos == -1 and y_pos == 1) or(x_pos == -2 and y_pos == 5) or (x_pos == 2 and y_pos == 6):
            print("1: Move forward")
            print("2: Move to the right")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move forward")
                print("2: Move to the right")
                print("3: Main menu")
                decision = input("What will you do? ")  
                decision = decision.strip()  
            if decision == "1":
                print("You moved forwards")
                y_pos+=1
            elif decision == "2":
                print("You moved to the right")
                x_pos+=1
            elif decision == "3":
                self.main_menu(main_menu_count)

        elif x_pos == -1 and y_pos == 4:
            print("1: Move forward")
            print("2: Move to the right")
            print("3: Move backwards")
            print("4: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3" and decision != "4":
                print("1: Move forward")
                print("2: Move to the right")
                print("3: Move backwards")
                print("4: Main menu")
                decision = input("What will you do? ")   
                decision = decision.strip()
            if decision == "1":
                print("You moved forwards")
                y_pos+=1
            elif decision == "2":
                print("You moved to the right")
                x_pos+=1
            elif decision == "3":
                print("You moved backwards")
                y_pos-=1
            elif decision == "4":
                self.main_menu(main_menu_count)

        elif (x_pos == -1 and y_pos == 5) or (x_pos == 1 and y_pos == 4) or (x_pos == 3 and y_pos == 6):
            print("1: Move backwards")
            print("2: Move to the left")
            print("3: Main menu")
            decision = input("What will you do? ") 
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move backwards")
                print("2: Move to the left")
                print("3: Main menu")
                decision = input("What will you do? ")       
                decision = decision.strip()
            if decision == "1":
                print("You moved backwards") 
                y_pos-=1 
            elif decision == "2":
                print("You moved to the left") 
                x_pos-=1   
            elif decision == "3":
                self.main_menu(main_menu_count)
        
        elif (x_pos == 1 and y_pos == 1) or (x_pos == 2 and y_pos == 1) or (x_pos == 0 and y_pos == 4):
            print("1: Move to the right")
            print("2: Move to the left")
            print("3: Main menu")
            decision = input("What will you do? ") 
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move to the right")
                print("2: Move to the left")
                print("3: Main menu")
                decision = input("What will you do? ") 
                decision = decision.strip()
            if decision == "1":
                print("You moved to the right")
                x_pos+=1
            elif decision == "2":
                print("You moved to the left")
                x_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)
        
        elif x_pos == 2 and y_pos == 7:
            print("1: Leave")
            print("2: Move backwards")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Leave")
                print("2: Move backwards")
                print("3: Main menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                y_pos+=1
                pass
            elif decision == "2":
                print("You moved backwards")
                y_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)
            
        elif (x_pos == -2 and y_pos == 6):
            print("1: Move backwards")
            print("2: Main Menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2":
                print("1: Move backwards")
                print("2: Main Menu")    
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved backwards")
                y_pos-=1
            elif decision == "2":
                self.main_menu(main_menu_count)
        
        elif x_pos == 3 and y_pos == 1:
            print("1: Move forward")
            print("2: Move to the left")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2":
                print("1: Move forward")
                print("2: Move to the left")
                print("3: Main menu")
                decision = input("What will you do? ")          
                decision = decision.strip()
            if decision == "1":
                print("You moved forward")
                y_pos+=1
            elif decision == "2":
                print("You moved to the left")
                x_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)

        cords = (x_pos,y_pos)
        return(cords)


    def minotaur_dungeon(self,book3_flag, book1_flag, book8_flag, book2_flag, potion_flag, Volatile_poison_flag, Minotaur_kill_count):
        leave=[]
        fight_cords=[(0,1),(-1,2),(-1,3),(-1,5),(-2,5),(1,4),(2,1),(3,1),(3,3),(3,4),(3,5),(3,6)]
        item_cords=[(-1,1),(-1,4),(-2,6),(1,1),(3,2),(1,3)]
        boss_cords=(2,7)
        rest_cords=[(2,6),(0,4)]
        dict_events={(-1,1):self.get_book8,(-1,4):self.get_book1, (-2,6):self.get_book3, (1,1):self.get_Volitile_poison, (3,2):self.get_potion, 
        (1,3):self.get_book2, (2,6):self.resting_spot, (0,4):self.resting_spot}
        for i in range(len(fight_cords)):
            dict_events[(fight_cords[i])]=self.battle
        
        
        if len(Minotaur_kill_count) == 1:
    
            x_pos=2
            y_pos=7
        else:
            x_pos=0
            y_pos=0
        

        cords=(x_pos,y_pos)
        while len(leave) == 0 and self.Hp > 0:
            cords=self.movement_minotaur_dungeon(cords[0],cords[1])
            print(cords)
            if (cords in fight_cords) == True:
                print("You encountered an enemy!")
                (dict_events[cords])(Goblin,fight_counter)
                del dict_events[cords]
                fight_cords.remove(cords)
            elif cords == (boss_cords):
                if len(Minotaur_kill_count) == 0:
                    self.minotaur_confirmation()
                    if len(Minotaur_kill_count) == 0:
                        cords = (x_pos,(y_pos-1))
                else:
                    cords=(2,7)
            elif cords[1] == 8:
                leave.append(1)
            elif cords == (0,0):
                pass
            elif (cords in dict_events) == False:
                pass
            else:
                dict_events[cords]()
        
            
            



    def boss_battle1(self,Minotaur):
        input("Before you lies a living corpse. It wields a greataxe and has a helmet with pointed horns.")
        input("With a beastial roar the monster pounces at you signifying that the battle has begun.")
        if self.weapon == "poisoned rusty dagger" or self.weapon == "poisoned sword":
            print("You jam the poisoned weapon into your foe!")
            print("The vicious poison greatly weakens the Minotaur!")
            Minotaur=Enemy("Minotaur",40,60,10,10,500,400)
            while self.Hp >0 and Minotaur.vit >0:
                print("The poison courses through the monsters veins!")
                print(Minotaur.name+ ' ' + "loses 15 hp!")
                Minotaur.vit = Minotaur.vit-15
                combat_options=self.combat_options()
                self.option_result(combat_options,Minotaur)
            if self.Hp > 0:
                self.victory(Minotaur)
                if self.exp >= self.expcap:
                    self.level_up_sequence()
                input("The living corpse stops moving.")
                input(self.name+':'+" "+"That was close... If I didn't have that poison I would be a goner!")
                input(self.weapon+' '+"is unusable now because of the poison.")
                input(self.name+':'+' '+"Huh? What's that in the corner?")
                input("In the dark ruins you spot a weapon in the distance.")
                input("As you approach you recognize that it is a grey lance.")
                input("Despite it's age it seems to still be usable and in good condition.")
                input("Besides it is some silver polish. Probably belonged to the previous owner")
                input("You take the lance")
                input("You take the silver polish")
                inventory.append("lance")
                inventory.append("silver polish")
                input(self.name+':'+' '+"A fine replacement for what I've lost.")
                input("you quickly get up and head to the exit.")
                input(self.name+':'+" "+"No time to waste. Gotta keep moving if I want to remember who I am.")
                Minotaur_kill_count.append(1)
            else:
                print(Minotaur.name+' '+ "Won!")
                print("Game over")
        else:
            self.fight(Minotaur)
            if self.Hp > 0:
                Minotaur_kill_count.append(1)
            else:
                print("Game over")

    def boss_battle2(self,Werewolf):
        if self.weapon == "silver sword" or self.weapon == "silver lance":
            print("your opponent fears silver!")
            print("You feel strength surge through you!")
            original_attack=self.attck
            self.attck= self.attck*5
            while self.Hp >0 and Werewolf.vit >0:
                print("Silver weakens the beast!")
                Werewolf.attck = Werewolf.attck-5
                Werewolf.agl=Werewolf.agl-5
                Werewolf.defence=Werewolf.defence-5
                combat_options=self.combat_options()
                self.option_result(combat_options,Werewolf)
            if self.Hp > 0:
                self.victory(Werewolf)
                if self.exp >= self.expcap:
                   self.level_up_sequence()
                input("Werewolf: So you're the completed product... Pathetic.")
                input("Werewolf: But maybe I'm more pathetic for losing to you.")
                input("Werewolf: Your expression tells me everything. How laughable, I was defeated by a tool that's ignorant of it's identity.")
                input(self.name+':'+" "+"You know me?")
                input("Werewolf: No, I know of you. Your ilk... They'll cause more damage than I ever could.")
                input("More blood seeps from the fatal wound.")
                input("Werewolf: I'll see you in hell.... I hope humanity is dragged down with you")
                #input(Werewolf.name+' '+ "dropped"+str(Werewolf.drop))
                inventory.append("Werewolf tooth")
                input("You claim the Werewolf's tooth as proof of what you've done.")
                input(self.name+' '+"Got the 'Werewolf's tooth!'")
                if ("old map" in inventory) == True:
                    input(self.name+':'+' '+"What the?!")
                    input("The old map is reacting to the moonlight!")
                    input(self.name+' '+"obtained the 'moonlit map!'")
                    inventory.append("moonlit map")
                    input(self.name+':'+' '+"That was unexpected, I should check the map later.")
                input(self.name+':'+' '+"There's no time to waste. I'll go see the Mysterious shopkeep")
                self.attck=original_attack
                werewolf_kill_count.append(1)
                self.shopkeeper(shopkeeper_count)
            else:
                print(Werewolf.name+' '+ "Won!")
                print("Game over")
        else:
            self.fight(Werewolf)
            if self.Hp > 0:
                if ("old map" in inventory) == True:
                    input(self.name+':'+' '+"What the?!")
                    input("The old map is reacting to the moonlight!")
                    input(self.name+' '+"obtained the 'moonlit map!'")
                    inventory.append("moonlit map")
                    input(self.name+':'+' '+"That was unexpected, I should check the map later.")
                werewolf_kill_count.append(1)
                inventory.append("Werewolf tooth")
                print("You claim the Werewolf's tooth as proof of what you've done.")
                print(self.name+' '+"Got the 'Werewolf's tooth!'")
                input(self.name+':'+' '+"There's no time to waste. I'll go see the Mysterious shopkeep")
                self.shopkeeper(shopkeeper_count)
            else:
                print("Game over")
    '''
    action_count=[]
    first_encounter=[]
    book4_flag=[]
    book5_flag=[]
    book6_flag=[]
    book7_flag=[]
    potion1_flag=[]
    potion2_flag=[]
    
    basement_key_flag=[]
    upstairs_key_flag=[]

    '''
    def get_potion1(self):
        if len(potion1_flag) == 0:
            input("You found a potion on the ground")
            input(self.name+':'+' '+"This should come in handy")
            input(self.name+' '+"got a potion!")
            inventory.append("potion")
            potion1_flag.append(1)
    
    def get_potion2(self):
        if len(potion2_flag) == 0:
            input("You found a potion on the ground")
            input(self.name+':'+' '+"This should come in handy")
            input(self.name+' '+"got a potion!")
            inventory.append("potion")
            potion2_flag.append(1)

    def get_potion3(self):
        if len(potion3_flag) == 0:
            input("You found a potion on the ground")
            input(self.name+':'+' '+"This should come in handy")
            input(self.name+' '+"got a potion!")
            inventory.append("potion")
            potion3_flag.append(1)
            
    #"Ruined journal #1","Ruined journal #2", "Ruined journal #3"
    def get_book4(self):
        if len(book4_flag) == 0:
            input("You find what seems to be a journal.")
            input(self.name+':'+" "+"Maybe this has some clues about this place")
            input("you picked up the journal")
            input(self.name+' '+"got Ruined journal #1")
            inventory.append("Ruined journal #1")
            book4_flag.append(1)
    
    def get_book5(self):
        if len(book5_flag) == 0:
            input("You find what seems to be a journal.")
            input(self.name+':'+" "+"Maybe this has some clues about this place")
            input("you picked up the journal")
            input(self.name+' '+"got Ruined journal #2")
            inventory.append("Ruined journal #2")
            book5_flag.append(1)
    
    def get_book6(self):
        if len(book6_flag) == 0:
            input("You find what seems to be a journal.")
            input("It seems to have dried blood on it.")
            input(self.name+':'+" "+"Maybe this has some clues about this place, very creepy though")
            input("you picked up the journal")
            input(self.name+' '+"got Ruined journal #3")
            inventory.append("Ruined journal #3")
            book6_flag.append(1)
    
    def get_basement_key(self):
        if len(basement_key_flag) == 0:
            input("You found a key")
            input(self.name+':'+' '+"This key might unlock something. I should bring it with me.")
            input(self.name+' '+"Got basement key!")
            inventory.append("basement key")
            basement_key_flag.append(1)

    def get_upstairs_key(self):
        if len(upstairs_key_flag) == 0:
            input("You found a key")
            input(self.name+':'+' '+"This key might unlock something. I should bring it with me.")
            input(self.name+' '+"Got upstairs key!")
            inventory.append("upstairs key")
            upstairs_key_flag.append(1)
    def do_action(self):
        if len(action_count) == 0:
            input("There is a large amount of debris and rubble here")
            input(self.name+':'+' '+"'Isn't this just above the Gargoyle? Maybe I should push this pile down")
            decision=input("Try to push rubbled onto Gargoyle? yes/no ")
            decision=decision.strip()
            while decision != "yes" and decision != "no":
               decision=input("Try to push rubbled onto Gargoyle? yes/no ")
               decision=decision.strip()
            if decision == "yes":
                input(self.name+':'+' '+"Alright, let's do it!") 
                input("You push the large pile of debris with all your might")
                input("This load is far too much for a normal human")
                input(self.name+':'+' '+"Come on just move already!")
                input("inhuman strength fills your body as your pupils flash red for an instant")
                input("you suceeded in pushing the rubble")
                input(self.name+':'+' '+"'Was I always that strong? Oh well, I'll think about it later'")
                action_count.append(1)
            else:
                input(self.name+':'+' '+"Maybe trying this isn't the best idea. How would I even move all of this?")
                input("you give up for now")
    
    def movement_gargoyle_dungeon_base_floor(self,x_pos,y_pos):
        if (x_pos == 0 and y_pos == 0):
            print("1: Move forward")
            print("2: Leave")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2":
                print("1: Move forward")
                print("2: Leave")
                print("3: Main Menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved forward")
                y_pos+=1
            elif decision == "2":
                print("You leave the ruined castle")
                y_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)

        elif x_pos == 0 and y_pos == 1:
            print("1: move Forwards")
            print("2: Move to the right")
            print("3: Move to the left")
            print("4: Move backwards")
            print("5: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3" and decision != "4" and decision != "5":
                print("1: Move to the right")
                print("2: Move to the left")
                print("3: Move backwards")
                print("4: Main menu")     
                decision = input("What will you do? ") 
                decision = decision.strip()
            if decision == "1":
                print("You moved forward")  
                y_pos+=1
            elif decision == "2":
                print("You moved to the right")
                x_pos+=1   
            elif decision == "3":
                print("You moved to the left")
                x_pos-=1
            elif decision == "4":
                print("you went backwards")
                y_pos-=1
            elif decision == "5":
                self.main_menu(main_menu_count)
        
        elif (x_pos == -1 and y_pos == 1) or (x_pos == 1 and y_pos == 1) or (x_pos == 2 and y_pos == 1) :
            print("1: Move to the right")
            print("2: Move to the left")
            print("3: Main menu")
            decision = input("What will you do? ") 
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move to the right")
                print("2: Move to the left")
                print("3: Main menu")
                decision = input("What will you do? ") 
                decision = decision.strip()
            if decision == "1":
                print("You moved to the right")
                x_pos+=1
            elif decision == "2":
                print("You moved to the left")
                x_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)
        

        elif (x_pos == -2 and y_pos == 2) or (x_pos == -2 and y_pos == 3) or (x_pos == 3 and y_pos == 2) or (x_pos == 1 and y_pos == 5) :
            print("1: Move forward")
            print("2: Move backwards")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move forward")
                print("2: Move backwards")
                print("3: Main menu")   
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved forward")
                y_pos+=1
            elif decision == "2":
                print("You moved backwards")
                y_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)

        elif (x_pos == -2 and y_pos == 1) or(x_pos == 1 and y_pos == 4) or (x_pos == 2 and y_pos == 3):
                    print("1: Move forward")
                    print("2: Move to the right")
                    print("3: Main menu")
                    decision = input("What will you do? ")
                    decision = decision.strip()
                    while decision != "1" and decision != "2" and decision != "3":
                        print("1: Move forward")
                        print("2: Move to the right")
                        print("3: Main menu")
                        decision = input("What will you do? ")    
                        decision = decision.strip()
                    if decision == "1":
                        print("You moved forwards")
                        y_pos+=1
                    elif decision == "2":
                        print("You moved to the right")
                        x_pos+=1
                    elif decision == "3":
                        self.main_menu(main_menu_count)
        
        elif (x_pos == 1 and y_pos == 3) or (x_pos == 3 and y_pos == 3) or (x_pos == 2 and y_pos == 4):
            print("1: Move backwards")
            print("2: Move to the left")
            print("3: Main menu")
            decision = input("What will you do? ") 
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move backwards")
                print("2: Move to the left")
                print("3: Main menu")
                decision = input("What will you do? ") 
                decision = decision.strip()      
            if decision == "1":
                print("You moved backwards") 
                y_pos-=1 
            elif decision == "2":
                print("You moved to the left") 
                x_pos-=1   
            elif decision == "3":
                self.main_menu(main_menu_count)
        
        elif (x_pos == 0 and y_pos == 2) or (x_pos == 1 and y_pos == 6):
            print("1: Move backwards")
            print("2: Main Menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2":
                print("1: Move backwards")
                print("2: Main Menu")    
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved backwards")
                y_pos-=1
            elif decision == "2":
                self.main_menu(main_menu_count)
        
        elif (x_pos == -2 and y_pos == 4):
            print("1: Move uptairs")
            print("2: Move bakckwards")
            print("3: Main Menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move backwards")
                print("2: Main Menu")    
                print("3: Main Menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                if ("upstairs key" in inventory) == False:
                    input("It's locked.")
                    input(self.name+':'+' '+"Looks like I'll need a key to enter.")
                    input(self.name+':'+' '+"Maybe the key is somewhere in this place")
                else:
                    input("You used upstairs key.")
                    input("You go up the staircase")
                    self.Gargoyle_dungeon_top_floor(action_count,potion2_flag,potion3_flag)
            elif decision == "2":
                print("You moved backwards")
                y_pos-=1

            elif decision == "3":
                self.main_menu(main_menu_count)   

        elif (x_pos == 3 and y_pos == 1):
            print("1: Move to the basement")
            print("2: Move forward")
            print("3: Move to the left")
            print("4: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3" and decision != "4":
                print("1: Move to the basement")
                print("2: Move forward")
                print("3: Move to the left")
                print("4: Main menu")
                decision = input("What will you do? ")  
                decision = decision.strip()
            if decision == "1":
                if ("basement key" in inventory) == False:
                    input("It's locked.")
                    input(self.name+':'+' '+"Looks like I'll need a key to enter.")
                    input(self.name+':'+' '+"Maybe the key is somewhere in this place")
                else:
                    print("You use the basement key")   
                    print("You go down the stairs")
                    self.gargoyle_dungeon_basement(book5_flag,book6_flag,upstairs_key_flag)
            elif decision == "2":
                print("You moved forward")
                y_pos+=1
            elif decision == "3":
                print("You moved to the left")
                x_pos-=1
            elif decision == "4":
                self.main_menu(main_menu_count)
    #done I think
        cords=(x_pos,y_pos)
        return(cords)

    def Gargoyle_dungeon_base_floor(self,action_count,first_encounter,book4_flag,potion1_flag,basement_key_flag,Gargoyle_kill_count):
        leave=[]
        x_pos=0
        y_pos=0
        cords=(x_pos,y_pos)
        boss_cords=(0,2)
        fight_cords_base=[(-1,1),(-2,1),(-2,3),(-2,4),(1,1),(2,1),(3,1),(3,3),(2,3),(2,4),(1,4),(1,5)]  
        #fight_cords_basement=[(1,0),(2,0),(2,1),(2,2),(1,4),(0,4),(-1,4),(1,5)]
        #fight_cords_top_floor=[(0,1),(0,2),(1,3),(2,3),(2,2),(2,1),(-1,3),(-1,4),(-1,5)]

        item_cords_base=[(-2,2),(3,2),(1,6)]
        #item_cords_basement=[(-1,2),(1,3),(2,5)]
        #item_cords_top_floor=[(0,3),(0,5)]

        rest_cords_base=[(0,1)]
        #rest_cords_basement=[(1,2),(-1,3)]
        
        dict_events_base={(-2,2):self.get_book4,(3,2):self.get_potion1,(1,6):self.get_basement_key,(0,1):self.resting_spot}
        #dict_events_basement ={(-1,2):self.get_upstairs_key,(1,3):self.get_book5,(2,5):self.get_book6,(1,2):self.resting_spot,(-1,3):self.resting_spot}
        #dict_events_top_floor={(0,2):self.do_action,(0,3):self.get_potion2,(0,5):self.get_potion3}
        #action_cord=(2,0)
        for i in range(len(fight_cords_base)) :
            dict_events_base[(fight_cords_base[i])] = self.battle
        '''
        for i in range(len(fight_cords_basement)):
            dict_events_basement[(fight_cords_basement[i])]=self.battle
        
        for i in range(len(fight_cords_top_floor)):
            dict_events_top_floor[(fight_cords_top_floor[i])]=self.battle
         '''
        while len(leave) == 0 and self.Hp > 0:
            cords=self.movement_gargoyle_dungeon_base_floor(cords[0],cords[1])
            print(cords)
            if (cords in fight_cords_base) == True:
                print("You encountered an enemy!")
                (dict_events_base[cords])(Kobald,fight_counter)
                del dict_events_base[cords]
                fight_cords_base.remove(cords)

            elif cords == (boss_cords) :
                if len(Gargoyle_kill_count) == 0:  #What the hell is wrong with this part?
                    self.gargoyle_confirmation(action_count,first_encounter)
                    if len(Gargoyle_kill_count) == 0:
                        cords = (0,1)
                    else:
                        cords=(0,2)
            elif cords[1] == -1:
                leave.append(1)
            elif cords == (0,0):
                pass
            elif (cords in dict_events_base) == False:
                pass
            else:
                dict_events_base[cords]()
        if self.Hp > 0:
            print("You left the ruined castle.")
            self.town(town_phase)
        else:
            print("Game over")
        
    def movement_gargoyle_dungeon_basement(self,x_pos,y_pos):
        if x_pos == 0 and y_pos == 0:
            print("1: Leave basement")
            print("2: Move to the right")
            print("3: Main menu")
            decision=input("What will you do? ")
            decision=decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Leave basement")
                print("2: Move to the right")
                print("3: Main menu")
                decision=input("What will you do? ")
                decision=decision.strip()

            if decision == "1":
                print("You left the basement")
                x_pos-=1
            elif decision == "2":
                print("You moved to the right")
                x_pos+=1
            elif decision == "3":
                self.main_menu(main_menu_count)
        elif (x_pos == 1 and y_pos == 0) or (x_pos == 0 and y_pos == 4) :
            print("1: Move to the right")
            print("2: Move to the left")
            print("3: Main menu")
            decision = input("What will you do? ") 
            decision=decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move to the right")
                print("2: Move to the left")
                print("3: Main menu")
                decision = input("What will you do? ") 
                decision=decision.strip()
            if decision == "1":
                print("You moved to the right")
                x_pos+=1
            elif decision == "2":
                print("You moved to the left")
                x_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)

        elif (x_pos == 2 and y_pos == 1) or (x_pos == 1 and y_pos == 3) or (x_pos == -1 and y_pos == 3):
            print("1: Move forward")
            print("2: Move backwards")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision=decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move forward")
                print("2: Move backwards")
                print("3: Main menu")   
                decision = input("What will you do? ")
                decision=decision.strip()
            if decision == "1":
                print("You moved forward")
                y_pos+=1
            elif decision == "2":
                print("You moved backwards")
                y_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)

        elif (x_pos == 2 and y_pos == 5):
            print("1: Move to the left")
            print("2: Main menu")
            decision = input("What will you do? ")
            decision=decision.strip()
            while decision != "1" and decision != "2":
                print("1: Move to the left")
                print("2: Main menu")
                decision = input("What will you do? ")
                decision=decision.strip()
            if decision == "1":
                print("You moved to the left")
                x_pos-=1
            elif decision == "2":
                self.main_menu(main_menu_count)

        elif (x_pos == -1 and y_pos == 2):
            print("1: Move forward")
            print("2: Main menu")
            decision = input("What will you do? ")
            decision=decision.strip()
            while decision != "1" and decision != "2":
                print("1: Move forward")
                print("2: Main menu")
                decision = input("What will you do? ")
                decision=decision.strip()
            if decision == "1":
                print("You moved forward")
                y_pos+=1
            elif decision == "2":
                self.main_menu(main_menu_count)
    
        elif (x_pos == 1 and y_pos == 4):
            print("1: Move forward")
            print("2: Move to the left")
            print("3: Move backwards")
            print("4: Main menu")
            decision = input("What will you do? ")
            decision=decision.strip()
            while decision != "1" and decision != "2" and decision != "3" and decision != "4":
                print("1: Move forward")
                print("2: Move to the left")
                print("3: Move backwards")
                print("4: Main menu")
                decision = input("What will you do? ")
                decision=decision.strip()
            if decision == "1":
                print("You moved forward")
                y_pos+=1
            elif decision == "2":
                print("You moved to the left")
                x_pos-=1
            elif decision == "3":
                print("You moved backwards")
                y_pos-=1
            elif decision == "4":
                self.main_menu(main_menu_count)
        
        elif (x_pos == 2 and y_pos == 0):
            print("1: Move forward")
            print("2: Move to the left")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision=decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move forward")
                print("2: Move to the left")
                print("3: Main menu")
                decision = input("What will you do? ")
                decision=decision.strip()
            if decision == "1":
                print("You moved forwards")
                y_pos += 1
            if decision == "2":
                print("You moved to the left")
                x_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count) 

        elif (x_pos == 2 and y_pos == 2):
            print("1: Move backwards")
            print("2: Move to the left")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision=decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move backwards")
                print("2: Move to the left")
                print("3: Main menu")
                decision = input("What will you do? ")
                decision=decision.strip()
            if decision == "1":
                print("You moved backwards")
                y_pos -= 1
            if decision == "2":
                print("You moved to the left")
                x_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)      
        
        elif (x_pos == 1 and y_pos == 2):
            print("1: Move forward")
            print("2: Move to the right")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision=decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move forward")
                print("2: Move to the right")
                print("3: Main menu")
                decision = input("What will you do? ")
                decision=decision.strip()
            if decision == "1":
                print("You moved forwards")
                y_pos += 1
            if decision == "2":
                print("You moved to the right")
                x_pos+=1
            elif decision == "3":
                self.main_menu(main_menu_count) 

        elif (x_pos == -1 and y_pos == 4) or (x_pos == 1 and y_pos == 5):
            print("1: Move backwards")
            print("2: Move to the right")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision=decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move backwards")
                print("2: Move to the right")
                print("3: Main menu")
                decision = input("What will you do? ")
                decision=decision.strip()
            if decision == "1":
                print("You moved backwards")
                y_pos -= 1
            if decision == "2":
                print("You moved to the right")
                x_pos+=1
            elif decision == "3":
                self.main_menu(main_menu_count)   
        
        cords = (x_pos,y_pos)
        return(cords)

    def gargoyle_dungeon_basement(self,book5_flag,book6_flag,upstairs_key_flag):
        leave=[]
        x_pos=0
        y_pos=0
        cords=(x_pos,y_pos)
        fight_cords_basement=[(1,0),(2,0),(2,1),(2,2),(1,4),(0,4),(-1,4),(1,5)]
        item_cords_basement=[(-1,2),(1,3),(2,5)]
        rest_cords_basement=[(1,2),(-1,3)]
        dict_events_basement ={(-1,2):self.get_upstairs_key,(1,3):self.get_book5,(2,5):self.get_book6,(1,2):self.resting_spot,(-1,3):self.resting_spot}
        for i in range(len(fight_cords_basement)):
            dict_events_basement[(fight_cords_basement[i])]=self.battle

        while len(leave) == 0 and self.Hp > 0:
            cords=self.movement_gargoyle_dungeon_basement(cords[0],cords[1])
            print(cords)
            if (cords in fight_cords_basement) == True:
                print("You encountered an enemy!")
                (dict_events_basement[cords])(Kobald,fight_counter)
                del dict_events_basement[cords]
                fight_cords_basement.remove(cords)

            elif cords[0] == -1 and cords[1] == 0:
                leave.append(1)
            elif cords == (0,0):
                pass
            elif (cords in dict_events_basement) == False:
                pass
            else:
                dict_events_basement[cords]()
        if self.Hp > 0:
            print("You left the basement")
        else:
            print("Game over")
        
    
    def movement_Gargoyle_dungeon_top_floor(self,x_pos,y_pos):
        if (x_pos == 0 and y_pos == 0):
            print("1: Move forward")
            print("2: Leave")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2":
                print("1: Move forward")
                print("2: Leave")
                print("3: Main Menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved forward")
                y_pos+=1
            elif decision == "2":
                print("You leave the ruined castle")
                y_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)

        elif (x_pos == 0 and y_pos == 1) or (x_pos == 0 and y_pos == 2) or (x_pos == 2 and y_pos == 1) or (x_pos == 2 and y_pos == 2) or (x_pos == -1 and y_pos == 4):
            print("1: Move forward")
            print("2: Move backwards")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move forward")
                print("2: Move backwards")
                print("3: Main menu")   
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved forward")
                y_pos+=1
            elif decision == "2":
                print("You moved backwards")
                y_pos-=1
            elif decision == "3":
                self.main_menu(main_menu_count)


        elif (x_pos == -1 and y_pos == 3):
            print("1: Move forward")
            print("2: Move to the right")
            print("3: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move forward")
                print("2: Move to the right")
                print("3: Main menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved forwards")
                y_pos += 1
            if decision == "2":
                print("You moved to the right")
                x_pos+=1
            elif decision == "3":
                self.main_menu(main_menu_count) 
        
        elif (x_pos == 0 and y_pos == 3):
            print("1: Move backwards")
            print("2: Move to the left")
            print("3: Move to the right")
            print("4: Main menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3" and decision != "4":
                print("1: Move backwards")
                print("2: Move to the left")
                print("3: Move to the right")
                print("4: Main menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved backwards")
                y_pos -= 1
            elif decision == "2":
                print("You moved to the left")
                x_pos -= 1
            if decision == "3":
                print("You moved to the right")
                x_pos+=1
            elif decision == "4":
                self.main_menu(main_menu_count) 

        elif (x_pos == 2 and y_pos == 3):
            print("1: Move backwards")
            print("2: Move to the left")
            print("3: Main Menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move backwards")
                print("2: Move to the left")
                print("3: Main menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved backwards")
                y_pos -= 1
            elif decision == "2":
                print("You moved to the left")
                x_pos -= 1
            elif decision == "3":
                self.main_menu(main_menu_count) 
    
        elif (x_pos == -1 and y_pos == 5):
            print("1: Move backwards")
            print("2: Move to the right")
            print("3: Main Menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move backwards")
                print("2: Move to the right")
                print("3: Main menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved backwards")
                y_pos -= 1
            elif decision == "2":
                print("You moved to the right")
                x_pos += 1
            elif decision == "3":
                self.main_menu(main_menu_count)
        
        elif (x_pos == 0 and y_pos == 5):
            print("1: Move to the left")
            print("2: Main Menu")
            decision = input("What will you do?")
            while decision != "1" and decision != "2":
                print("1: Move to the left")
                print("2: Main menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved to the left")
                x_pos -= 1
            elif decision == "2":
                self.main_menu(main_menu_count) 

        elif (x_pos == 1 and y_pos == 3):
            print("1: Move to the left")
            print("2: Move to the right")
            print("3: Main Menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2" and decision != "3":
                print("1: Move to the left")
                print("2: Move to the right")
                print("3: Main menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved to the left")
                x_pos -= 1
            elif decision == "2":
                print("You moved to the right")
                x_pos+=1
            elif decision == "3":
                self.main_menu(main_menu_count) 

        elif (x_pos == 2 and y_pos == 0):
            print("1: Move forward")
            print("2: Main Menu")
            decision = input("What will you do? ")
            decision = decision.strip()
            while decision != "1" and decision != "2":
                print("1: Move forward")
                print("2: Main menu")
                decision = input("What will you do? ")
                decision = decision.strip()
            if decision == "1":
                print("You moved forward")
                y_pos += 1
            elif decision == "2":
                self.main_menu(main_menu_count) 
    
        cords=(x_pos,y_pos)
        return(cords)
        
    
    def Gargoyle_dungeon_top_floor(self,action_count,potion2_flag,potion3_flag):
        leave =[]
        x_pos=0
        y_pos=0
        cords=(x_pos,y_pos)
        fight_cords_top_floor=[(0,1),(0,2),(1,3),(2,3),(2,2),(2,1),(-1,3),(-1,4),(-1,5)]
        item_cords_top_floor=[(0,3),(0,5)]
        dict_events_top_floor={(2,0):self.do_action,(0,3):self.get_potion2,(0,5):self.get_potion3}
        for i in range(len(fight_cords_top_floor)):
            dict_events_top_floor[(fight_cords_top_floor[i])]=self.battle

        while len(leave) == 0 and self.Hp > 0:
            cords=self.movement_Gargoyle_dungeon_top_floor(cords[0],cords[1])
            print(cords)
            if (cords in fight_cords_top_floor) == True:
                print("You encountered an enemy!")
                (dict_events_top_floor[cords])(Kobald,fight_counter)
                del dict_events_top_floor[cords]
                fight_cords_top_floor.remove(cords)

            elif cords[-1] == -1:
                leave.append(1)
            elif cords == (0,0):
                pass
            elif (cords in dict_events_top_floor) == False:
                pass
            else:
                dict_events_top_floor[cords]()
        if self.Hp > 0:
            print("You left the top floor")
        else:
            print("Game over")
        
        pass
        
    def boss_battle3(self,Gargoyle,action_count):
        if len(action_count) == 1:
            input("You face the stone sentinel, Gargoyle.")
            #Gargoyle = Enemy("Gargoyle",100,700,400,90,10000,3000)
            Gargoyle = Enemy("Gargoyle",50,350,150,45,10000,3000)
            while self.Hp >0 and Gargoyle.vit >0:
                combat_options=self.combat_options()
                self.option_result(combat_options,Gargoyle)  
            if self.Hp > 0:
                self.victory(Gargoyle)
                if self.exp >= self.expcap:
                   self.level_up_sequence()
                input("You pierce through the glowing red stone at the Gargoyle's chest.")
                input("It looks at you clutching it's halberd swinging it down.")
                input("It aims to take you down in it's final moments")
                input("There's no dodging this attack")
                input(self.name+':'+' '+"*closes eyes* 'Is this how it's gonna end?'")
                input("Instead of the expected flash of pain you simply feel the stone sentinel's hand gently resting on your head.")
                input("You look up to see it's eyes stop glowing.")
                input("On it's face sits a satisfied smile before it's body cracks and fragments into peaces. ")
                input(self.name+':'+' '+"It... hesitated?")
                input("Your head begins to hurt.")
                self.memory_frag2_3()
                input(self.name+':'+' '+"So you've been here this entire time... Staying true to your final orders.")
                input("You smile")
                input(self.name+':'+' '+"You did well.")
                input("You search around to find what the Gargoyle was guarding")
                input(self.name+':'+' '+"This is the item I saw in my memories. I'll take it with me.")
                input(self.name+':'+' '+"If I were to leave then killing the Gargoyle would have been for nothing.")
                input(self.name+' '+"Got the emblem!")
                inventory.append("emblem")
        else:
            self.fight(Gargoyle)
            if self.Hp > 0:
                Gargoyle_kill_count.append(1)
                input("You search around to find what the Gargoyle was guarding")
                input(self.name+':'+' '+"If I were to leave then killing the Gargoyle would have been for nothing.")
                input(self.name+' '+"Got the emblem!")
                inventory.append("emblem") 
            else:
                print("Game over")

    
    def boss_battle4(self,Fafnir,inventory):
        if ("emblem" in inventory) == True:
            while self.Hp > 0 and Fafnir.vit>0:
                input("The dragon spews forth a sea of flames")
                '''
                combat_options=self.combat_options()
                self.option_result(combat_options,Fafnir)
                '''
                damage = 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                input(self.name+' '+"Took"+' '+str(damage)+'!')
                self.Hp = -1
            if self.Hp < 0:
                input("???: Do you wish to win? Then simply use me.")
                confirmation=input("Will you draw the sword?: yes/no: ")
                while confirmation != "yes" and confirmation != "no":
                    confirmation=input("Will you draw the sword?: yes/no: ")
                    confirmation=confirmation.strip()
                if confirmation=="yes":
                    print("A small voice can be heard. Different from the ominous voice you heard before hand.")
                    print("*kind voice*: Will you draw that sword even if it makes your life a living hell?")
                    print("the emblem falls on the floor and upon looking at it you seem to be in a trance.")
                    confirmation=input("Will you draw the sword?: yes/no: ")
                    while confirmation != "yes" and confirmation != "no":
                        confirmation=input("Will you draw the sword?: yes/no: ")
                        confirmation=confirmation.strip()
                    if confirmation=="yes":
                        input("Fafnir: That emblem! I Thought all of you were dead!")
                        input("The Proud dragon's composure dissapears. Replacing it is a crippling fear.")
                        input("In your trance you calmly unsheathe the jet black sword.")
                        self.weapon="???"
                        self.attck=(self.str+weapons[self.weapon])
                        self.Hp=1
                        input("The end is near")
                        input("The proud dragon tries to fly away")
                        self.combat_options_special(Fafnir)
                        if Fafnir.vit <= 0:
                            input("in a flash the huge dragon is cut into 10 pieces with the black blade.")
                            self.victory(Fafnir)
                            if self.exp >= self.expcap:
                                self.level_up_sequence()
                            input("the dragon is slain.")
                            input(self.name+':'+ " "+"I remember everything... The empire I was sworn to protect is gone.")
                            input("you look at the cursed sword")
                            input(self.name+':'+ " "+" And it's all my fault....")
                            input("Flashes of your past appear. You gleefully cutting down monsters and innocents alike in the burning capital.")
                            input("You hold your head")
                            input(self.name+':'+' '+"I don't have much time. Now that the seal is broken it won't be long till I'm taken by madness.")
                            input("You point to edge of the sword downwards to your stomach")
                            input("???: I asked if you would draw the sword if your life would be made into a living hell")
                            input("???: Don't tell me you plan on running away O sword of the empire")
                            input("You recognize the playful voice and turn")
                            input(self.name+':'+' '+"Shopkeep... No... Morgan")
                            input("Morgan smiles taking off her hat.")
                            input("Morgan: It's been 1000 years. It hurt when you didn't recognize me you know.")
                            input(self.name+':'+' '+"I can imagine you had fun playing shopkeeper with the amnesiac version of myself.")
                            input(self.name+':'+' '+"As happy as I am to see you, I'm afraid this is going to be goodbye oncemore")
                            input("On your hand a black aura is manifesting, theatening to swallow your sanity")
                            input("Morgan: Stop with the melodrama, it's not about the curse, you've already given up haven't you?")    
                            input(self.name+':'+' '+"Without the empire... I don't have anything left.")
                            input("Morgan looks like she was about to say something but catches herself")            
                            input("Morgan: They're still out there. Your personal unit.")            
                            input("Morgan: You think I've spent 1000 years doing nothing? I've found a way to save you and everyone else.")
                            input("Morgan: So you can't die just yet O sword of the empire. You have a duty to save your men.")
                            input("Morgan holds out her hand")
                            input(self.name+':'+' '+"*smiles* I could never beat you in an argument")
                            input("You sheathe the sword")
                            input(self.name+':'+' '+"So long as I'm still sane I'll help as much as possible")
                            input("You shake her hand")
                            input("Morgan: Good, before we go, let's fix your problem first.")
                            input(self.name+' '+"'The soldier from a forgotten time'"+' '+"story prologue,Finished")
                    else:
                        self.ending_bad()
                else:
                    self.ending_bad()
        else:
            self.fight(Fafnir)
            if self.Hp >0:
                input("Congrats. You cheated.")
                input("If you didn't cheat and just grinded all the way to this level.... I applaud you, I know I didn't put a level cap but lord...")
                input("It's not like The mobs drop boatloads of XP too... ")
                input("With that being said... that means you're someone who has access to the Source code!")
                input("Just joking, this is on a public github repo, anyone could have it by now.")
                input("Hope you enjoyed the game anyway, I encourage you to get the true ending next time")
            else:
                self.ending_bad()

    def battle(self,enemy,fight_counter): 
        if len(fight_counter)==1:
            combat_tutorial()
            fight_counter.pop(0)
            self.battle(enemy,fight_counter)
            self.weapon_check()
        else:
            if enemy.name=="Fafnir":
                enemy=Enemy("Fafnir",300,10000,300,250,100000000,10000000000)
                self.boss_battle4(enemy,inventory)
                
            elif enemy.name=="Minotaur":
                enemy = Enemy("Minotaur",60,200,20,10,500,400)
                self.boss_battle1(enemy)
            elif enemy.name =="Werewolf":
                enemy=Enemy("Werewolf",70,500,10,30,1000,1000)
                self.boss_battle2(enemy)
            elif enemy.name == "Goblin":
                enemy=Enemy("Goblin",20,30,2,10,25,10)
                self.fight(enemy)
            elif enemy.name == "Kobald":
                enemy=Enemy("Kobald",40,90,20,30,60,100)
                self.fight(enemy)
            self.weapon_check()

    def weapon_check(self):
        if self.weapon == "silver lance" or self.weapon == "silver sword":
            input("the silver weapon loses it's effect")
            if self.weapon == "silver lance":
                self.weapon = "lance"
            else:
                self.weapon = "sword"

        elif self.weapon == "poisoned rusty dagger" or self.weapon == "poisoned sword":
            input("The poisoned weapon is reduced to scrap metal by the poison")
            self.weapon="unarmed"
        self.attck = self.str+weapons[self.weapon]

                

    def shop(self,items_shop,items_shop_list,inventory):
        if ("Werewolf tooth" in inventory) == True and ("moonlit map" in inventory) == False:
            items_shop_list.append("moonstone")
        elif ("silver polish" in inventory) != True:
            items_shop_list.append("silver polish")
        for i in range(len(items_shop_list)):
            print(items_shop_list[i])
        check = True
        print("Your money:"+' '+str(self.bal))
        while check == True:
            print("enter 5 if you want to leave.")
            item = input("What would you like to purchase?: ")
            item=item.strip()
            for i in range(len(items_shop_list)):
                print(items_shop_list[i]+' '+str(items_shop[(items_shop_list[i])])+' '+"Gold")
            if (item in items_shop_list) == True:
                if items_shop[item] > self.bal:
                    print("It appears you do not have enough money to purchase this item. please choose again")
                else:
                    if item == "old map":
                        print("Mysterious shopkeep: Keep that map close. I have a feeling you'll need it if you want to live.")
                        input(self.name+':'+" "+"As cryptic as always....")
                        input("She laughs")
                        add=items_shop_list.pop(0)
                        inventory.append(add)
                    else:
                        inventory.append(item)
                        print("Thank you for your purchase!")
                        self.bal=self.bal-(items_shop[item])
            elif item == "5":
                check = False
            else:
                print("invalid item. Please try again")

    def shop_sell(self,inventory,items_sell,books):
        check = True
        while check == True:
            for i in range(len(inventory)):
                print(inventory[i])
            print("Enter 5 if you want to leave.")
            sell = input("what would you like to sell?: ")
            if sell == "???" and len(potion_flag)==1:
                input("Mysterious shopkeep: That is.... No... I can't take this. Hold onto it.")
                input(self.name+':'+' '+"You recognize this?")
                input("Mysterious shopkeep: If you want to know then pay me 9999999999999999999999999 gold.")
                if self.bal < 9999999999999999999999999:
                    input(self.name+':'+' '+"How can you say that with such an innocent smile on your face. *sigh*")
                    print("You give up on trying to sell the mysterious sword")
                else:
                    input(self.name+':'+"You're in luck! I just so happen to have that much. count it and weep!")
                    input("Mysterious shopkeep: since when were you filthy rich? I didn't even think this much money existed.")
                    input(self.name+':'+' '+"So will you tell me now?")
                    input("Mysterious shopkeep: sorry, trade secret, no matter how much money you offer me I won't say a word.")
                    input(self.name+':'+' '+"All those days of goblin and kobald killing.....")
                    input("Mysterious shopkeep: OK OK, fine. Have this on the house!")
                    input(self.name+' '+ "gained 1000000000 potions!")
                    for i in range(1000000000):
                        inventory.append("potion")
                    input("Mysterious shopkeep: now please don't ever bring this up again.")
                    input("Mysterious shopkeep: *sobs* My profit marginsssssssssssss")
                    potion_flag.pop(0)
            elif sell =="???" and len(potion_flag)==0:
                input("Mysterious shopkeep: Like I said, can't tell you about that sword no matter what you offer me.")
                input(self.name+':'+' '+"Why not? I'm the owner of the sword so shouldn't I know about it.")
                input("Mysterious shopkeep: That's... I'm really sorry, I can't say anymore. When the time comes I promise to tell you everything.")
                input("you decide to not press her for information. She has been quite a help to you after all, you don't want to sour your relationship with her.")
                input(self.name+':'+' '+"'*sigh* Guess I'll drop it.'")

            elif (sell in books)== True:
                input("Mysterious shopkeep: Come on now. This isn't a library, I don't want your weird books.")
            elif (sell in inventory) == False:
                input("Mysterious shopkeep: How are you going to sell what you don't have?")
            elif (sell in inventory)==True and (sell in items_sell)==True:
                self.bal+=(items_sell[sell])
                inventory.remove(sell)
                input("Mysterious shopkeep: Thanks for always choosing us, even when you don't have a choice!")
                input("Mysterious shopkeep: keep selling your items here so that I can make it rich later!")
            
            elif sell == "5":
                input("Mysterious shopkeep: Bring back more fun things next time!")
                check = False

            else:
                input("Mysterious shopkeep: You should probably hold onto that.")
                input(self.name+':'+" "+"I'll sell it to someone else then.")
                input("Mysterious shopkeep: Go right ahead, I'd like to see who else buys the weird stuff you have.")
                input(self.name+':'+"'I hate to admit it but she's right....'")
                input("You give up on selling"+' '+sell)


    
    #Item descriptions
    #####################################################################################################

    #Rusty_dagger.txt
    def rusty_dagger_des(self):
        input("A rusted dagger that seems very feable. It is one of the items you found on yourself when you woke up. Maybe you'll find a use for it")
        input(self.name+':'+' '+"There's a weird engraving on the side... but it's too faint to read.")
        print("attack value is"+' '+ str(weapons["rusty dagger"]))
    
    #Poisoned_Rusty_Dagger.txt
    def poisoned_rusty_dagger_des(self):
        input("The same dagger but now drenched in the volitile posion. Looks like it will be good for one last blow. make it count.")
        input(self.name+':'+' '+"I don't know why but I feel bad using the dagger like this.")
        print("attack value is"+' '+ str(weapons["poisoned rusty dagger"]))
    
    #Lance.txt
    def lance_des(self):
        input("A lance found in the minotaurs lair. Although you feel you aren't proficient with the weapon it might be useful later on.")
        input(self.name+':'+' '+"I'm not a spearman but oh well")
        print("attack value is"+' '+ str(weapons["lance"]))
    
    #Silver_Lance.txt
    def silver_lance_des(self):
        input("You can feel the power of silver flow through this weapon. Make the effects count!")
        print("attack value is"+' '+ str(weapons["silver lance"]))
    
    #Sword.txt
    def sword_des(self):
        input("normal sword that was at your side when you woke up. Looks like you still know how to use it")
        input(self.name+':'+' '+"Old reliable. You've been with me for a while haven't you.")
        print("attack value is"+' '+ str(weapons["sword"]))

    #Poisoned_Sword.txt
    def poisoned_sword_des(self):
        input("The sword drenched in deadly poison. Sadly it looks like it'll break soon. maybe using that on your main weapon was a bad idea")
        input(self.name+':'+' '+"Maybe this wasn't the best idea.... *sigh*")
        print("attack value is"+' '+ str(weapons["poisoned sword"]))
    
    # Silver_Sword.txt
    def silver_sword_des(self):
        input("You can feel the power of silver flow through this weapon. Make the effects count!")
        print("attack value is"+' '+ str(weapons["silver sword"]))

    #Cursed_Sword.txt
    def cursed_sword_des(self):
        input("A sword that you carry on your back. Whenever you reach for it your body freezes and refuses to draw it out. Maybe you should leave it alone.")
        input(self.name+':'+' '+"*stare* Everytime I look at this a shiver goes down my spine")
    
    #Volitile_Poison.txt
    def Volitile_poison_des(self):
        input("Some poison you found. It comprimises the structural integrity of whatever it is applied to but will leave the victim of the attack poisoned. Maybe it'll come in handy later.")
        input(self.name+':'+' '+"Sometimes you gotta play dirty to win.")
        input(self.name+':'+' '+"it's only good for one fight so I should save it for a strong enemy.")
    
    #Silver_Polish.txt
    def Silver_polish_des(self):
        input("Applies the attribute of silver to whatever it is applied to. The effects last for only one fight, maybe you'll find a use for this latter.")
        input(self.name+':'+' '+"It's shiny")
    
    #Old_Bread.txt
    def old_bread_des(self):
        input("some old bread you found. Hopefully this doesn't make you sick")
        input(self.name+':'+' '+"I'm suprisingly used to eating food like this")
        print("Heals for 20 hp")
    
    #Emblem.txt
    def emblem_des(self):
        input("An emblem you found. Although you don't know why, you are certain this relates to you and so you keep it close.")
        input(self.name+':'+' '+"What secrets do you hold?....")
        print("you put away the emblem.")
    
    #Potion.txt
    def potion_des(self):
        input("A type of medicine with a fruity aftertaste. Good for wounds... just don't ask what it's made of.")
        input(self.name+':'+' '+"Nothing like a nice cold drink to help deal with serious wounds!")
        print("heals 50 hp")

    #Old_Map.txt
    def old_map_des(self):
        input("An old map you purchased from the shopkeeper. Maybe there's a secret to it?")
        input(self.name+':'+' '+"..... Should I try lighting it on fire?")
        input(self.name+':'+" "+"... what am I thinking, that's beyond stupid.")
        print("you put away the map")
    
    #Moonstone.txt
    def moonstone_des(self):
        input("A white smooth stone that's said to be the shape of the moon. You bought it from the shopkeeper.")
        input(self.name+':'+' '+"It's a pretty rock.")
        input(self.name+':'+' '+"I wonder if I can actually do something with this though.")
        input(self.name+':'+' '+"Should I combine it with something?")
        print("you put away the moonstone")
    
    #Moonlit_Map.txt
    def moonlit_map_des(self,ruined_castle_flag):                  
        print("The old map is illuminated to reveal the path to an ancient ruin.")
        input(self.name+':'+' '+"Looks like I won't have to complain to the shopkeep after all.")
        input(self.name+':'+' '+"I should explore this place. It might have something useful.")
        if len(ruined_castle_flag)==1:
            ruined_castle_flag.pop(0)

    #Werewolf_Tooth.txt
    def Werewolf_tooth_def(self):
        print("A large canines tooth. You obtained it after besting the Werewolf, Father David.")
        input(self.name+':'+' '+"What did he mean by 'your ilk' and 'completed product'?")
        input("You put away the werewolf's tooth.")
        input(self.name+':'+' '+"I should go see the shopkeeper now that I'm done.")
    
    #Basement_Key.txt
    def basement_key_des(self):
        input("A key for the basement floor of the ruined castle")
        input(self.name+':'+' '+"Wow that was early. SHouldn't I be getting this in season 3?") #AOT joke
        input("You put the basement key away")
    
    #Upstairs_Key.txt
    def upstairs_key_des(self):
        input("A key for the upstair floor of the ruined castle")
        input(self.name+':'+' '+"Now I can go upstairs and explore there!")
        input("You put away the upstairs key")

    #####################################################################################################

    def descriptions(self,inventory,descriptions_menu,ruined_castle_flag,):
        dict_des={"Volitile Poison":self.Volitile_poison_des,"silver polish":self.Silver_polish_des,"emblem":self.emblem_des,
        
        "moonlit map":self.moonlit_map_des,'Gospel of the dragons':self.book7, "Ruined journal #1":self.book4,

        'History book':self.book8, "Items":self.book3,
        
        "Ruined journal #2":self.book5, "Ruined journal #3":self.book6, "Werewolf tooth":self.Werewolf_tooth_def,
        
        "Demons":self.book2, "old book":self.book1,"moonstone":self.moonstone_des,"potion":self.potion_des,
        
        "sword":self.sword_des,"poisoned sword":self.poisoned_sword_des,"silver sword":self.silver_sword_des,"rusty dagger":self.rusty_dagger_des,
        
        "upstairs key":self.upstairs_key_des, "basement key":self.basement_key_des,

        "poisoned rusty dagger":self.poisoned_rusty_dagger_des,"lance":self.lance_des,"silver lance":self.silver_lance_des,"???":self.sword_des}
        if len(descriptions_menu) == 0:
            descriptions_tutorial()
            descriptions_menu.pop(0)
        
        for i in range(len(inventory)):
            print(inventory[i])
        check = True
        while check == True:
            print("Enter 5 to leave")
            item= input("Choose item: ")
            if (item in inventory) == False or (item in dict_des) == False:
                print("Invalid item")
            elif item == "5":
                check = False
            else:
                if item == "moonlit map":
                    dict_des[item](ruined_castle_flag)
                else:
                    dict_des[item]()
            
    

    def equip(self,weapons,equip_menu_count):
        if len(equip_menu_count) == 1:
            equip_tutorial()
            equip_menu_count.pop(0)
        check = True
        while check == True:
            for i in range(len(inventory)):
                if (inventory[i] in weapons) == True:
                    print(inventory[i])
            print("Equipped weapon:"+ ' '+self.weapon)
            print("Enter 5 to exit.")
            confirmations = input("What would you like to equip/unequip ")
            confirmations = confirmations.strip()
            while (confirmations in weapons) != True:
                confirmations= input("What would you like to equip/unequip ")
                confirmations=confirmations.strip()
            if confirmations == self.weapon and confirmations != "unarmed" and confirmations != "???":
                confirmation2=input("would you like to unequip this weapon? yes/no ")
                confirmation2=confirmation2.strip()
                while confirmation2 != "yes" and confirmation2 != "no":
                    confirmation2=input("would you like to unequip this weapon? yes/no ")
                    confirmation2=confirmation2.strip()
                if confirmation2 == "yes":
                    inventory.append(self.weapon)
                    self.weapon = "unarmed"
                else:
                    print("understood")
            elif confirmations == "???":
                input("you try but you can't seem to do it. Your body freezes everytime you try.")
                input("You give up on equipping the sword")
            elif confirmations == "unarmed":
                input("you are already unarmed.")
            elif confirmations == "5":
                check = False
            else:
                confirmation2=input("would you like to equip this weapon? yes/no ")
                confirmation2=confirmation2.strip()
                while confirmation2 != "yes" and confirmation2 != "no":
                    confirmation2=input("would you like to equip this weapon? yes/no ")
                    confirmation2=confirmation2.strip()
                if confirmation2 == "yes":
                    inventory.append(self.weapon)
                    self.weapon = confirmations
                    inventory.remove(confirmations)
                else:
                    print("You didn't equip"+' '+confirmations)

        self.attck=(self.str+weapons[self.weapon])
    

    def combine(self, inventory,combinable_items,combine_menu):

        if len(combine_menu) == 1:
            combine_tutorial()
            combine_menu.pop(0)
        check = True
        
        while check == True:
            
            applicable_items=[]
            for i in range(len(inventory)):
                if (inventory[i] in combinable_items) == True:
                    applicable_items.append(inventory[i])
            if len(applicable_items) == 0:
                print("You have no items that can be combined")
                check=False
            else:
                print(applicable_items)
                print("Enter 5 if you want to leave (on either the first or second item selection")
                confirmation = input("Which item will you pick?: ")
                while (confirmation in combinable_items) == False or (confirmation in inventory) == False or confirmation != "5":
                    confirmation = input("Which item will you pick?: ")
                if confirmation == "5":
                    pass
                else:
                    confirmation2 = input("what will you combine it with?: ")
                    while (confirmation2 in combinable_items) == False or  (confirmation2 in inventory) == False or confirmation2 !=  "5":
                        confirmation2 = input("what will you combine it with?: ")
                    if (confirmation == "sword" and confirmation2 == "Volitile poison") or (confirmation == "rusty dagger" and confirmation2 == "Volitile poison") or  (confirmation == "Volitile poison" and confirmation2 == "sword") or (confirmation =="Volitile poison" and confirmation2 == "rusty dagger"):
                        if confirmation=="rusty dagger" or confirmation2=="rusty dagger":
                            print("You made a poisoned rusty dagger!")
                            inventory.append("poisoned rusty dagger")
                            inventory.remove("Volitile poison")
                            inventory.remove("rusty dagger")
                        elif confirmation == "sword" or confirmation2 == "sword":
                            print("you made a poisoned sword!")
                            inventory.append("poisoned sword")
                            inventory.remove("sword")
                            inventory.remove("Volitile poison")
                    elif (confirmation == "sword" and confirmation2 == "silver polish") or (confirmation == "silver polish" and confirmation2 == "sword") or (confirmation == "lance" and confirmation2 == "silver polish") or (confirmation == "silver polish" and confirmation2 == "lance"):
                        if confirmation == "sword" or confirmation2 == "sword":
                            print("You made a silver sword!")
                            inventory.append("silver sword")
                            inventory.remove("sword")
                            inventory.remove("silver polish")
                        elif confirmation == "lance" or confirmation2 == "lance":
                            print("You made a silver lance!")
                            inventory.append("silver lance")
                            inventory.remove("lance")
                            inventory.remove("silver polish")
                    elif (confirmation== "lance" and confirmation2=="Volitile poison") or (confirmation=="Volitile poison" and confirmation2=="lance"):
                        print("Weird... You can't get the lance until you kill the minotaur... but you also can't kill the minotaur without using the poison.")
                        print("let's fix that.")
                        print(self.name+' '+"lost the lance!")
                        print(self.name+' '+"lost the Volitile poison!")
                        inventory.remove("Volitile poison")
                        inventory.remove("lance")
                    elif (confirmation == "moonstone" and confirmation2 == "old map") or (confirmation =="old map"  and confirmation2 == "moonstone") :
                        print("you made moonlit map!")
                        inventory.append("moonlit map")
                        inventory.remove("moonstone")
                        inventory.remove("old map")
                    elif confirmation == "5" or confirmation2 == "5":
                        check = False
                    else:
                        print("You can't make anything with those items.")



    def main_menu(self,main_menu_count):
        if len(main_menu_count)==0:
            main_menu_tutorial()
            main_menu_count.pop(0)
        check = True
        while check == True:
            print(self.name)
            print("Level:"+' '+str(self.lvl))
            print("Hp:"+' '+str(self.Hp)+"/"+str(self.Hpcap))
            print("Equipped weapon:"+' '+self.weapon)
            print("Attack:"+' '+str(self.attck))
            print("Strength:"+' '+str(self.str))
            print("Vitality:"+' '+str(self.vit))
            print("Defence:" +' '+str(self.defence))
            print("Magic:"+' '+str(self.mag))
            print("exp"+' '+str(self.exp)+"/"+str(self.expcap))
            print("Money:" +' '+str(self.bal))
            print("1: use items")
            print("2: combine items")
            print("3: examine items")
            print("4: change weapon")
            print("5: exit")
            confirmation=input("What would you like to do? input the corresponding number: ")
            confirmation=confirmation.strip()
            while confirmation != "1" and confirmation != "2"  and confirmation != "3" and confirmation != "4" and confirmation != "5":
               confirmation=input("What would you like to do? input the corresponding number: ")
               confirmation=confirmation.strip()
            if confirmation == "1" :
    
                self.items(consumable_item, inventory)
            elif confirmation == "2":
                self.combine(inventory,combinable_items,combine_menu)
            elif confirmation == "3":
                self.descriptions(inventory,descriptions_menu,ruined_castle_flag)
            elif confirmation == "4":
                self.equip(weapons,equip_menu_count)
            elif confirmation == "5":
                check = False
    
    #Inn_Welcome.txt
    def free_inn(self):
        input("Inn owner: Welcome! Oh? You're a new face.")
        input(self.name+':'+' '+"I just came to town.")
        input("Inn owner: You from the outside? What are you a priest or something?")
        input(self.name+':'+' '+"'priests can freely travel?'")
        input(self.name+':'+' '+"'No, even if I did go that route it would take too long.'")
        input(self.name+':'+' '+"something like that.")
        input("Inn owner: Ah well, this place is a little rundown but I can gurrantee you'll have a nice rest here! ")
        input("Inn owner: Since you're an outsider, the first nights on the house! Rest well.")
        input(self.name+':'+' '+"Thanks! I really appreciate it!")
        input(self.name+':'+' '+"You rest in the Inn")
        self.memory_frag1()
        self.rest()

    #Memory_Fragment#1.txt
    def memory_frag1(self):
        input("Your head starts to hurt")
        input("???: Is this the one? He looks like he's barely 12.")
        input("gruff voice: Yes your higness, he's the assassin Delta.")
        input("'his highness': Oh? A code name at his age? How intresting!")
        input("'his highness': I've decided, this boy will be my personal attendant! ")
        input("gruff voice: Your higness that's-!")
        input("'his higness': That's enough, this decision is final!")
        input("You hear footsteps approach you.")
        input("The drug is beginning to wear off, your vision clears.")
        input("You finally see who stands before you.")
        input("A young man with black hair and smooth features adorned in royal garbs")
        input("'his highness': Ah you're awake! I'm Amadeus ramses the third. Royal prince of the empire.")
        input("Amadeus: Oh right, the drugs. You probably can't even speak right now.")
        input("gruff voice: Your highness if you're waiting for him to introduce himself I'm afraid that's impossible.")
        input("Amadeus turned as he frowned.")
        input("Amadeus: Why's that?")
        input("gruff voice: The organization he belongs to steals orphans and pumps them full of dangerous stimulants.")
        input("gruff voice: He doesn't know anything but violence at this point.")
        input("Amadeus: He doesn't even remember his own name? Now that isn't good.")
        input("Amadeus: It may be presumptious but I will grant you a name, an identity outside of that dreaded code name.")
        input("Amadeus: Your name will be ....")
        input("You wake up")
        input(self.name+':'+' '+"Were those... my memories?")

    #Memory_Fragment#2.txt
    def memory_frag2(self):
        input("Amadeus: Ah you're here. How goes the campaign.")
        input("someone replies but you can't seem to hear them.")
        input("Amadeus: Not good huh.... It can't be helped. Our enemies are dragons.")
        input("someone replies but you can't seem to hear them.")
        input("Amadeus: You don't have to worry about me old friend.")
        input("someone replies but you can't seem to hear them.")
        input("Amadeus: In my studies I've found a possible solution to this problem. One in the world of the arcane.")
        input("someone replies but you can't seem to hear them.")
        input("Amadeus: You think I should ask her? She does have considerable knowledge but I can't have her leave her post.")
        input("Amadeus: If she leaves the western front will collapse.")
        input("someone replies but you can't seem to hear them.")
        input("Amadeus: Don't worry, I won't do anything rash. I just have to do what I can for the sake of the people.")
        input("someone replies but you can't seem to hear them.")
        input("Amadeus: What is it that I'm researching?")
        input("someone replies but you can't seem to hear them.")
        input("Amadeus: I guess it's fine to tell you.")
        input("someone replies but you can't seem to hear them.")
        input("Amadeus: I'm researching for a way to create soldiers that can use magic. artificial witches.")
        input("Amadeus: I think I'll call them... Magisters. Hopefully I can create them before everything falls.")
        input("You wake up")
        input(self.name+':'+' ' +"'again with the odd dreams. What does any of this mean?'")
        input(self.name+':'+' '+"What do I have to do with this nation at war?")
        input(self.name+':'+' '+"......")
        input(self.name+':'+' '+"I can only go forward.... I'll learn why as I continue this path")
    
    #Memory_Fragment#2.5.txt
    def memory_frag2_3(self):
        input("You see the Gargoyle you had just defeated, far less ancient than when you encountered it.")
        input("???: Your duty is over. I'm not gonna last much longer.")
        input("The Gargoyle shakes it's stone head")
        input("???: You're as stuborn as your creator. I had a feeling that this may happen.")
        input("???: In that case... I have one last order for you.")
        input("???: Guard this for me. It's something that should never see the light of day ever again. ")
        input("???: Attack anyone that comes to claim it.... Even if... Even if it's me.")
        input("The Gargoyle makes the saddest expression it can make with it's stony visage.")
        input("???: I understand that I've given you a hard task my friend but I can't take back that order.")
        input("???: This is my final order. A selfish order and one that will cause you pain.")
        input("???: Still, you're the only one I can ask. Please, I'm asking as a friend, not as your master.")
        input("The Gargoyle hesitates before giving a sad nod")
        input("???: Thank you. Here is the item.")
        input("A hand is outstretched clutching a small item ")
        input("The Gargoyle moves from it's position and takes it from the man.")
        input("???: I don't have much time.")
        input("The man puts his hand on top of the gargoyles stone head, patting it gently")
        input("???: Goodbye my friend. May we never meet again.") #says this because if they do, one of them dies
        input("???: 'I'll see my duty through.'")
        
    #Memory_Fragment#3.txt
    def memory_frag3(self):
        input("In front of you is the same Amadeus as before. He looks terrible.")
        input("The bright king from before is nowhere to be seen. It's as if he is crushed under the stress.")
        input("Amadeus: This is a risky process... I can't say for sure you'll survive.")
        input("Amadeus: If the situation wasn't dire I would have waited for the results to stabilize...")
        input("someone replies but you can't seem to hear them.")
        input("Amadeus: You trust me....")
        input("You nod")
        input("Amadeus sighs")
        input("Amadeus: The process should last for a week.")
        input("Amadeus: The rest of your personal knights have already been undergoing the process. You're the last one.")
        input("Amadeus: We'll do what we can to buy you time.")
        input("Amadeus: Don't die my friend, I order you, "+' '+self.name+', '+"to come back alive using my authority as emperor.")
        input("You smile and nod")
        input("An unknown amount of time passes")
        input("You sit still in the void, not feeling anything and not knowing anything.")
        input("When your eyes open your pupils are scarlet red")
        input("There is one thought in your head.")
        input("killkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkillkill")
        input("You jerk awake, sweating and breathing hard.")
        input(self.name+':'+' '+"It was all a dream....?")
        input(self.name+':'+' '+"That was... me...")
        input("Amadeus had clearly said your name.")
        input(self.name+':'+' '+"if I remember... will I...")
        input(self.name+':'+' '+"Will I... go back to being that... thing?")
        memory_frag3_flag.append(1)

    def inn(self):
        if len(inn_count)==1:
            self.free_inn()
            inn_count.pop(0)
            input(self.name+':'+' '+"It's time for me to go look for leads on how to leave this place.")
        
        else:
            confirmation=input("Inn owner: Welcome! what would you like a room? it's 20 gold a night yes/no ")
            confirmation=confirmation.strip()
            while confirmation != "yes" and confirmation != "no":
                confirmation=input("Inn owner: Welcome! what would you like a room? it's 20 gold a night yes/no ")
                confirmation=confirmation.strip()
            if confirmation == "yes" and self.bal >= 20 :
                self.rest()
                self.bal = self.bal - 20
                if len(werewolf_kill_count) == 1 and len(memory_frag2_flag) == 0:
                    self.memory_frag2()
                    memory_frag2_flag.append(1)
                elif len(Gargoyle_kill_count) == 1 and len(memory_frag3_flag) == 0:
                    self.memory_frag3()
                    memory_frag3_flag.append(1)
            elif confirmation == "yes" and self.bal < 20:
                input("Inn owner: Looks like you don't have enough. Sorry.")
                input(self.name+':'+' '+"'Maybe I should go hunt some more monsters or sell something in order to afford a room...'")
            else:
                input("Inn Owner: Alright! See you next time!")
            self.town(town_phase)
    #town Function
    def town(self,town_phase):
        if len(town_phase) == 1:
            input("You enter the town after your encounter with Dave")
            input("You enter  nearby inn")
            input(self.name+':'+' '+"'Great I made it. I should look into a store that sells useful things.'")
            input(self.name+':'+' '+"For now I should look for a place to res")
            self.inn()
            input(self.name+':'+' '+"'If I'm going to leave this place I have to make sure I have supplies for the road after all.")
            input(self.name+':'+' '+"'That dragon is still a problem though...")
            input("You go in search of a shop.")
            self.shopkeeper(shopkeeper_count)
        elif len(town_phase) == 2:
            check = True
            while check == True:
                print("1: Enter menu")
                print("2: Rest at Inn")
                if len(shopkeeper_hint) == 0:
                    print("3: Confront the mysterious shopkeep")
                else:
                    print("3: Visit the mysterious shopkeep")
                print("4: talk to the small boy.")
                print("5: talk to the nun ")
                print("6: talk to the shady looking man")
                print("7: head back to the ruins (fight monsters)")
                confirmation=input("What will you do? ")
                confirmation=confirmation.strip()
                while confirmation != "1" and confirmation !="2" and confirmation !="3" and confirmation != "4" and confirmation !="5" and confirmation !="6" and confirmation !="7":
                    confirmation=input("What will you do? ")
                    confirmation=confirmation.strip()
                if confirmation == "1":
                    self.main_menu(main_menu_count)
                elif confirmation == "2":
                    self.inn()
                elif confirmation == "3":
                    self.shopkeeper(shopkeeper_count)
                    if len(shopkeeper_hint) == 0:
                        check = False
                elif confirmation == "4": 
                    self.npc2()
                elif confirmation == "5":
                    self.npc3(inventory)
                elif confirmation == "6":
                    self.npc7(shopkeeper_hint)
                elif confirmation == "7":
                    self.minotaur_dungeon(book3_flag,book1_flag,book8_flag,book2_flag,potion_flag,Volitile_poison_flag,Minotaur_kill_count)
                elif confirmation == "6":
                    if len(shopkeeper_hint) == 0:
                        self.shopkeeper(shopkeeper_count)
                        check = False
                    else:
                        print("invalid input")
        
        #werewolf phase
        elif len(town_phase) == 3:
            check=True
            while check == True:
                print("1: Enter menu")
                print("2: talk to the scared looking man")
                print("3: talk to the flower lady ")
                print("4: Rest at the Inn")
                print("5: Go see the shopkeep")
                print("6: head back to the ruins (fight monsters)")
                if len(werewolf_hints) == 3:
                    print("7: confront Father David")
                confirmation = input("what will you do? ")
                while confirmation != "1" and confirmation != "2" and confirmation !="3" and confirmation != "4"and confirmation != "5" and confirmation != "6" and confirmation != "7":
                    confirmation = input("What will you do? ")
            
                if confirmation == "1":
                    self.main_menu(main_menu_count)
                elif confirmation == "2":
                    self.npc4(werewolf_clue2,werewolf_hints)
                elif confirmation == "3":
                    self.npc5(werewolf_clue3,werewolf_hints)
                elif confirmation == "4":
                    self.inn()
                elif confirmation == "5":
                    self.shopkeeper(shopkeeper_count)
                elif confirmation == "6":
                    self.minotaur_dungeon(book3_flag,book1_flag,book8_flag,book2_flag,potion_flag,Volitile_poison_flag,Minotaur_kill_count)
                    
                elif confirmation == "7":
                    if len(werewolf_hints) == 3:
                        self.werewolf_confirmation()
                        if ("Werewolf tooth") in inventory == True:
                            check = False
                    else:
                        print("invalid input")
        
        #D True_ending.txt
        elif len(town_phase) == 4: #("Make your exit conditions bro")
                check = True
                while check == True:
                    print("1: Enter menu.")
                    print("2: rest at the Inn")
                    print("3: Go see the Mysterious shopkeep")
                    if len(final_flag) == 1:
                        print("4: Give up")
                        print("5: Confront Fafnir")
                        print("6: Go to minotaurs dungeon ")
                        if ("moonlit map" in inventory) == True and ("emblem"in inventory) == False:
                            print("7: Go to ruined castle(dungeon)")
                        elif ("emblem" in inventory) == True:
                            print("7: return to the Gargoyles's castle.")
                    confirmation = input("What will you do? ")
                    while confirmation != "1" and confirmation != "2" and confirmation !="3" and confirmation != "4"and confirmation != "5" and confirmation != "6" and confirmation != "7":
                        confirmation = input("What will you do? ")
                    if confirmation == "1":
                        self.main_menu(main_menu_count)
                    elif confirmation == "2":
                        self.inn()
                    elif confirmation == "3":
                        self.shopkeeper(shopkeeper_count)
                    elif confirmation == "4" and len(final_flag) == 1:
                        confirmation = input("Will you give up and foraske the hunt for your past? yes/no ")
                        while confirmation != "yes" and confirmation != "no":
                            confirmation = input("Will you give up and forsake the hunt for your past? yes/no ")
                        if confirmation == "yes":
                            self.ending_neutral()
                            town_phase.append(1)
                            check = False
                    elif confirmation == "5" and len(final_flag) == 1:
                        #Final battle
                        town_phase.append(1)
                        self.battle(Fafnir,fight_counter)
                        check = False
                        pass
                    elif confirmation == "6" and len(final_flag) == 1:
                        self.minotaur_dungeon(book3_flag,book1_flag,book8_flag,book2_flag,potion_flag,Volitile_poison_flag,Minotaur_kill_count)
                    elif confirmation == "7":
                        
                        if ("moonlit map" in inventory) == True:
                            self.Gargoyle_dungeon_base_floor(action_count,first_encounter,book4_flag,potion1_flag,basement_key_flag,Gargoyle_kill_count)
                        else:
                            print("invalid input")

            

            

            
    #Faint_Book.txt
    def Book1(self): 
        confirmation=input("The book is old and worn and the title is too faint. Would you like to read it? yes/no ")
        confirmation=confirmation.strip()
        while confirmation != "yes" and confirmation != "no":
            confirmation=input("Invalid input. Please try again.")
            confirmation=confirmation.strip()
        if confirmation == "yes":
            input("'In the ancient land of Astrea there lives a frightening Minotaur.'")
            input("'He was a champion of justice and the leader of a grand army.'")
            input("The following pages are blank")
            input("you flip to the end.")
            input("Even though he fought bravely, a vile poison crept into his body, killing him during the great war")
            input(self.name+':'+' '+"These seem to be the memoirs of a great warrior named 'Minotaur'.")
            input(self.name+':'+' '+"maybe this will be useful for something down the line")
            print("you put the book away")
        else:
            pass
    
    #Demons_A_Pocket_Guide_to_Humanity's_Greatest_Enemies.txt
    def Book2(self): 
        confirmation=input("The book is called 'Demons: A Pocket Guide to Humanities Greatest Enemies'. Would you like to read it? yes/no ")
        confirmation=confirmation.strip()
        while confirmation != "yes" and confirmation != "no":
            confirmation=input("Invalid input. Please try again.")
            confirmation=confirmation.strip()
        if confirmation == "yes":
            input("The back says that it is a compilation of various demons that appeared during the great war.")            
            input("One entry catches your eye, 'Werewolf'")
            input("'these monsters were the result of a madman mixing the wolf monsters with humans in order to create supersoldiers.'")
            input("'The experiment failed and the new monsters escaped. Appearently they now fear a certain met-'")
            input("The rest of the pages relating to werewolves are ruined")
            input(self.name+':'+" "+"Weird... only the part about Werewolves ripped up.")
            input(self.name+':'+' '+"I wonder who wrote this book though. Most people would normally die after encountering just one demon.")
            print("you put the book away.")
        else:
            pass
    
    #Items_An_Adventurer's_Best_Friend.txt
    def Book3(self):
            confirmation=input("The title of the book is 'Items: An Adventurer's best friend!' Would you like to read it? yes/no ")
            confirmation=confirmation.strip()
            while confirmation != "yes" and confirmation != "no":
                confirmation=input("Invalid input. Please try again.")
                confirmation=confirmation.strip()
            if confirmation == "yes":
                input("Items are quite important to wanderers and adventurers!")
                input("Some Items can be combined and be used in order to help out in tough fights!")
                input("Some Items require special situations for their effects to truly show!")
                input("Whenever you're stuck just look at what you have and you'll sure to find a way forward!")
                input(self.name+':'+" "+"Uhhh I guess I'll keep that in mind.")
                input(self.name+':'+" "+"'Would've been better if you just gave me a list of things I can make with items....'")
                print("you put the book away")
            else:
                pass

    #Gargoyles_Dungeon_Journal_#1.txt
    def Book4(self):
        confirmation=input("This seems to be a journal of some sorts. Would you like to read it? yes/no ")
        confirmation=confirmation.strip()
        while confirmation != "yes" and confirmation != "no":
            confirmation=input("Invalid input. Please try again.")
            confirmation=confirmation.strip()
        if confirmation == "yes":
            input("Day 15,")
            input("'I don't know why but the dragons have turned against us! Our winged protectors are now our fiercest enemies.'")
            input("'I heard Astrea has lost their champion... It looks like they'll fall soon.'")
            input("'Dammit! Are we just going to die like this?!'")
            input("'No. I can't give up now! If the dragons were the greatest weapons humanity had then we simply must make weapons that surpass even them!'")
            input("'I will gather the strongest men and women and arm them with the strongest weapons!'")
            input("'They will be the blades that will strike down the threats to my empire! I mustn't waver! The lives of my people depend on this'")
            input("The rest is ruined.")
            input(self.name+':'+' '+"Sorry my prince. Your gamble failed.")
            input(self.name+':'+' '+"Wait why did I...")
            input(self.name+':'+' '+".......")
            input(self.name+':'+ ' '+"No... There's no point thinking about it... I just need to keep moving and eventually everything will come back.")
            print("you put the book away")
        else:
            pass

    #Gargoyles_Dungeon_Journal_#2.txt
    def Book5(self):
        confirmation=input("This seems to be a journal of some sorts. Would you like to read it? yes/no ")
        confirmation=confirmation.strip()
        while confirmation != "yes" and confirmation != "no":
            confirmation=input("Invalid input. Please try again.")
            confirmation=confirmation.strip()
        if confirmation == "yes":
            input("'Day 35'")
            input("'No earthly metal can even put a dent in the cursed lizards's scales.'")
            input("'What use do the greatest warriors have when their weapons are useless against their foes?'")
            input("'If I'm to make the greatest weapons I must summon up a power beyond our realm.'")
            input("'What I'm about to do is heresy of the highest degree... But it must be done.'")
            input("The following pages are torn and blood stains the ends of these pages")
            input("you frown")
            input(self.name+':'+"...... I still can't forgive you.")
            input(self.name+':'+' '+"Again... I...")
            print("you put the book away")
        else:
            pass

    #Gargoyles_Dungeon_Journal_#3.txt
    def Book6(self): 
        confirmation=input("This seems to be a journal of some sorts. Would you like to read it? yes/no ")
        confirmation=confirmation.strip()
        while confirmation != "yes" and confirmation != "no":
            confirmation=input("Invalid input. Please try again.")
            confirmation=confirmation.strip()
        if confirmation == "yes":
            input("'Day 110'")
            input("'ThOsE FoOlS! ThEy DaRe CaLl Me GrAnD HeReTiC! AfTeR AlL I'vE DoNe FoR ThEm. DaMn InGrAtEs!'")
            input("'If I DiDn'T AcT tHeY WoUlD AlL Be RoTtInG In ThE GrOuNd! ScOrChEd By ThE dAmN dRaGoNs!'")
            input("'EvEn NoW ThEy TrY To StOp Me! HeHeHeHeHeHe, It MaTtErS nOt. My WoRk Is DoNe!'")
            input("'My BlAdE's WiLl RaZe ThIs EmPiRe AnD ThE ScAlEd OnEs InTo ThE GrOuNd!'")
            input("'DiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiEDiE")
            input("The rest is illegible scribbles.")
            input("The Final pages have stained blood all over them.")
            input("Your heart races when you read the word 'Blade'")
            input(self.name+':'+' '+"....Why did you try to take all of this alone....")
            input(self.name+':'+' '+"huh")
            input("you touch your eyes to see that they are wet with tears.")
            input(self.name+':'+' '+"I'm... crying?")
            print("you put the book away")
        else:
            pass

    #Gospel_of_the_Dragons.txt
    def Book7(self): 
        confirmation=input("This was the book the religious woman gave to you. Would you like to read it? yes/no ")
        confirmation=confirmation.strip()
        while confirmation != "yes" and confirmation != "no":
            confirmation=input("Invalid input. Please try again.")
            confirmation=confirmation.strip()
        if confirmation == "yes":
            input("'Dragons are holy creatures. Created by the gods themselves to watch over mankind.'")
            input("'Through their divinity they are able to use any and all magic.'")  
            input("'As beings of high divinity dragons themselves are considered gods and must be worshipped as such.'") 
            input("'Any action taken against a dragon, especially the act of slaying one is a grave sin.'")
            input("'Attempting to replicate the power of the dragons is also a grave sin.'")
            input("'The strongest and most noble dragons are capable of transforming into a humanoid form to help guide our wayword race.'")
            input("There's more but it's just different ways to go about worshipping the dragons.")
            input(self.name+':'+' '+"The church huh...")
            print("you put the book away")
        else:
            pass

    #Ancient_History_Book.txt
    def Book8(self): #placed ("History book")
        confirmation=input("This was the book you found in the minotaurs dungeon. Would you like to read it yes/no ")
        confirmation=confirmation.strip()
        while confirmation != "yes" and confirmation != "no":
            confirmation=input("Invalid input. Please try again.")
            confirmation=confirmation.strip()
        if confirmation == "yes":
            input("In this world there are monsters, dragons and humans. The dragons protected the humans from the monsters and helped them expand.")
            input("Monsters vary in size in strength, weak monsters like spirits are relatively harmless.")
            input("Goblins, kobalds and other smaller monsters can be felled by a skilled enough warrior.")
            input("Humans CANNOT fight against the stronger monsters like high-level undead and...")
            input("The book proceeds to name a large amount of monster races that humans cannot fight.")
            input("Dear reader, if you try to fight these monsters I hope you're ready for a gruesome death. The only exception to this rule is me of course!")
            input("You think whoever wrote the book is incredibly arrogant and should die in a hole.")
            input(self.name+':'+" "+"What a weird book, but I have nothing else to go on right now.... monsters though... do they really exist.")
            input(self.name+":"+' '+"I wonder if I'll ever meet the author of this book.")
            input("You think of what the author might be like. You picture an arrogant person and smug person.")
            input(self.name+':'+' '+"ughhh nevermind I don't want that.")
            print("you put the book away")
        else:
            pass

    #Dave
    #Dave.txt
    def npc1(self):
        input('Dave:' +' '+"Names Dave, Haven't seen you around here. Did you come from the outside?")
        input(self.name+':'+' '+"I'm not sure...")
        input('Dave:' +' '+"tch and here I thought you would have a way to leave. Get lost. That damn dragon is just keeping us in here like livestock!")
        input(self.name+':'+' '+"What do you mean?")
        input("Dave: If we leave past this towns border a dragon will kill us.")
        input("Dave pointed to a black corpse in the distance. Burned to a crisp by dragon fire.")
        input("You look around to see that there wasn't just one of these. There were many simply left unnatended.")
        input(self.name+':'+' '+"What the hell...")
        input(self.name+':'+' '+"'looks like getting out will be tricky..'")
        print("You and Dave each go on your way. He kept scouring the outskirts, you go on towards the town in the distance.")

    #kid
    #Kid.txt
    def npc2(self):
        input("young boy: Man I wish I could use magic. Apparently only dragons can do it.")
        input(self.name+':'+" "+"Only dragons can use magic?")
        input("young boy: That's a weird question. Of course only dragons can use magic. Well, I hear some people could use but I'm not sure.")
        input("young boy: Yeah, apparently Witches can use it but I hear they've went into hiding.")
        input("young boy: They wear big hats and cause all sorts of mischief")
        input("A woman calls the boy over")
        input("young boy: Anyway bye weird mister!")
        print("The little boy runs off")

    #Nun
    #Nun.txt
    def npc3(self,inventory):
        input("Religious woman: I see you've met my fool of a son Dave. Hmph. Doesn't he know that the dragon protects us from the outside?!")
        input(self.name+':'+' '+"The dragon protects us?")
        input("Religious woman: Of course he does! We may not be able to leave but the horrors of the outside can't enter either!")
        input("Religious woman: Here! Have this book")
        input("The Zealous woman gives you a book before leaving")
        print(self.name+' '+"Gained the 'Gospel of the dragons'")
        inventory.append('Gospel of the dragons')

    #Insane man
    #Insane_Man.txt
    def npc4(self,werewolf_clue2,werewolf_hints):
        if len(werewolf_clue2) == 1:
            input("Drunk man: HAHHAHAHAHAHHA, It'll kill us all.")
            input(self.name+':'+" "+"What will kill us all?")
            input("Drunk man: The wolfman! I saw It, It ate someone and the next day they were put as missing!")
            input("Drunk man: People say I'm insane but I know what I saw! It had a cross on it's arm and blood on it's teeth.")
            input("Drunk man: He'll really do it! He'll kill us all!")
            print("From then on the Drunk man just keeps mumbling strange words. You decide to move on.")
            werewolf_hints.append(1)
            werewolf_clue2.pop(0)
        else:
            input("You try to approach the man but he just keeps muttering nonesence.")
            input(self.name+':'+' '+"It's no good. He's too shaken up.")
    
    #Insane_Man_Reocurring.txt
    def npc4a(self):
        input("You try to approach the man but he just keeps muttering nonesence.")
        input(self.name+':'+' '+"It's no good. He's too shaken up.")

        
    #Flower lady
    #Flower_Lady.txt
    def npc5(self, werewolf_clue3, werewolf_hints):
        if len(werewolf_clue3) == 1:
            input("CONDITION HERE")
            input("Flower Lady: Hey you want a flower? Normally I charge but I'm in such a good mood today!")
            input(self.name+':'+" "+"What's the occasion?")
            input("She smirks")
            input("Flower Lady: Father David spoke to me and complimented my gardening skills saying in his wonderfully deep voice, 'these flowers have grown to be as beautiful as you.'")
            input("'For some reason you refuse to believe that he said that.'")
            input(self.name+':'+" "+"Who even is this Father David character?")
            input("Flower Lady: HUH?!?! You don't even know that?!")
            input("Flower Lady: Father David is the head priest for this place! He's such a devoted man that he seared the cross of saint Helios on his arm!")
            input("Flower Lady: To be honest, men like you stand no chance.... Shoo, you don't even deserve a flower if you ask stupid questions like that.")
            input("The Flower Lady walks off")
            input(self.name+':'+" "+"A cross seared onto his arm?")
            print("You walk off.")
            werewolf_hints.append(1)
            werewolf_clue3.pop(0)
        else:
            input("Flower Lady: Don't talk to me! Anyone who doesn't know how great father David is can go die!")

    #Flower_Lady_Reocurring.txt
    def npc5_2():
        input("Hmph go away!")

    #Mysterious shopkeep final quest
    #Mysterious_Shopkeep_Final_Quest.txt
    def npc6(self):
        if len(final_flag) == 0:     
            if ("Werewolf tooth" in inventory) == True and ("emblem" in inventory) == False:
                input("CONDITION HERE")
                input("Mysterious shopkeep: well done")
                input("Mysterious shopkeep: It seems that you are ready for your final endeavor.")    
                input("A mysterious door appears")
                input("Mysterious shopkeep: This passageway leads to the edge of town past where the dragon sleeps. You may choose to go but you are leaving things unfinished.")
                input("Mysterious shopkeep: It will still not be too late to go after completing everything that needs to be done.")      
                input("Mysterious shopkeep: The choice is yours.") 
                input(self.name+':'+' '+"'That's right... I have to make a decision soon...'")
                final_flag.append(1)
                town_phase.append(1)
        
    #Mysterious_shopkeep_emblem.txt
    def npc_check(self):
        if ("emblem" in inventory) == True:
            input("CONDITION HERE")
            input("The Mystreious shopkeep is looking at you with a warm smile ")
            input(self.name+':' +' '+"You seem to be in good spirits")
            input("Mysterious shopkeep: I am. How embarassing.")
            input(self.name+':'+ ' '+"'wonder why she's smiling'")


    #Info_Broker.txt
    def npc7(self,shopkeeper_hint):
        if len(shopkeeper_hint) == 1:
            input("CONDITION HERE")
            input("Info broker: You wanna know about an exit? Pay up! ")
            confirmation = input("Will you pay? yes/no ")
            while confirmation != "yes" and confirmation != "no":
                confirmation = input("Will you pay? yes/no ")
            if confirmation == "yes":
                price = 300
                if self.bal >= price:
                    self.bal=self.bal-price
                    input("Info broker: Nice! Anyway. Apperently the shopkeep has a way out. That's all I know.")
                    input("you stare at the info broker hapilly counting his coins")
                    input(self.name+':'+' '+"'If this info is bogus I'm gonna beat my coins out of him.'")
                    input(self.name+':'+' '+"'For now, let's go talk to the shopkeeper.'")
                    shopkeeper_hint.pop(0)
                else:
                    input("Info broker: Tch, then just leave! Useless....")
            else:
                input("Info broker: Tch, then just leave! Useless....")
    
    #Info_Broker_Reocurring.txt
    def npc7_2():
        input("Screw off, can't you tell I'm busy counting money?!")

    #Mysterious_Shopkeep_Werewolf.txt
    def npc8(self,shopkeeper_hint,werewolf_clue1, werewolf_hints):
        if len(shopkeeper_hint)==0 and len(werewolf_hints) == 0:
            input("CONDITION HERE")
            input("Mysterious shopkeep: Hello to my favourite customer. You seem to want something other than my great items. ")
            input(self.name+':'+" "+"Word on the street is that you have a way out of this place. Is that true?")
            input("Mysterious shopkeep: My my... Aren't you well informed. But yes... I do have a way out")
            input(self.name+':'+" "+"Then-")
            input("Mysterious shopkeep: Ah ah ah... That's not how this works. Our relationship is transactional. You give me what I want. I give you what you want.")
            input(self.name+':'+" "+"*sigh* then what do you want.....")
            input("The shopkeeper smiles.")
            input("Mysterious shopkeep: Haha, now that's what we like to hear. Anyway I want you to deal with the mysterious murders around town. ")
            input(self.name+':'+" "+"Do I look like a detective to you?")
            input("Mysterious shopkeep: No but you do look like the two things I like in my customers. Capable and desperate.")
            input(self.name+':'+" "+"Ugh Fine.")
            input("Mysterious shopkeep: That's the spirit! Good luck!")
            input(self.name+':'+' '+"'it's no good, I don't think she'll budge until I do as she says.'")
            input(self.name+':'+' '+"'I should ask around the town to find more clues to this mystery killer.'")
            print("You walked away sighing upon receiving your new objective.")
            werewolf_clue1.pop(0)
            werewolf_hints.append(1)
            town_phase.append(1)

    


    #shopkeeper dialogue(npc9-npc14)
    ######################################

    #Mysterious Shopkeeps introduction diologue
    #Mysterious_Shopkeep_Intro.txt
    def npc9(self):
        input(self.name+':'+" "+"'what an odd shop... I looked around but coudln't find any shops that sell useful things.'")
        input("You enter the odd shop at the edge of town.")
        input("Mysterious shopkeep: Welcome!")
        input("the shopkeeper looks like an elegant noble woman except for the commically large hat she wore.")
        input("you find her black hair and red eyes oddly entrancing")
        input(self.name+':'+' '+"'why's someone like her in a rundown town like this?'")
        input(self.name+':'+" "+"Hello, I was wondering if this shop sold useful supplies for adventurers.")
        input("She gave a kind smile")
        input("Mysterious shopeeker: Of course! You're in luck, we sell exactly that. We have a variety of potions at your disposal.")
        input(self.name+':'+' '+"Do you sell weapons or armor as well?")
        input("Mysterious shopkeeper: Sorry, ever since the dragon has been here all armor and weapons were offered as a tribute.")
        input("Mysterious shopkeeper: To make it worse, this place doesn't have a blacksmith.")
        input("Mysterious shopkeeper: I wouldn't hold out hope of getting new equipment here.")
        input(self.name+':'+" "+"I see, seeing as I'll be here for a while, what should I call you?")
        input("Mysterious shopkeep: 'As I thought, you don't remember.'")
        input("Mysterious shopkeep: for now 'Mysterious shopkeep' is good enough.")
        input(self.name+':'+' '+"'I guess she has her reasons for hiding her name.'")
        input(self.name+':'+' '+"Anyway I'm"+' '+self.name+','+' '+"nice to meet you.")
        input("Mysterious shopkeep: Likewise.")
        input("You shake hands")

    #Mysterious Shopkeep talks about her hat
    #Mysterious_Shopkeep_Hat
    def npc10(self):
        input(self.name+':'+' '+"So.... What's with the hat?")
        input("Her hat was commically large and ressembled the hat worn by a witch.")
        input("Despite it's age, she took very good care of it, often cleaning it and sewing it back up.")
        input("Mysterious shopkeep: Just so you know it's not for sale. ")
        input(self.name+':'+' '+"Obviously I don't want to buy it.")
        input(self.name+':'+' '+"You just take very good care of it so I was wondering about it's backstory.")
        input("Mysterious shopkeep: Oh, it's a memento of a really important person. So until I see him again I'll take good care of the hat.")
        input("You remark that her smile is genuine for once. Like she was recalling a fond memory.")
        input(self.name+':'+' '+"'so you can smile like that too...'")
        input("Mysterious shopkeep: Jealous?")
        input(self.name+':'+' '+"Obviously not.")
    
    #Mysterious Shopkeep talks about Asterious
    #Mysterious_Shopkeep_Asterious.txt
    def npc11(self):
        input("Mysterious shopkeep: So I heard you defeated the undead in the ruins.")
        input(self.name+':'+' '+"'so that's what that was.'")
        input(self.name+':'+' '+"Yeah I guess so. It was really strong.")
        input("Mysterious shopkeep: Asterious was really powerful when he was alive but should be less powerful as an undead.")
        input("Mysterious shopkeep: Even so, I don't think he's weak enough for you to beat him. So how exactly did you defeat him?")
        input(self.name+':'+' '+"It wasn't the most honourable way but I coated my weapon in poison and well...")
        input("Mysterious shopkeep: 'That make sense, for a moment I thought he...'")
        input("Mysterious shopkeep: Asterious died to poison in his life.")
        input(self.name+':'+' '+"So the poison I used was the same one that killed him originally?")
        input("Mysterious shopkeep: No, there's no way you could get your hands on that.")
        input("Mysterious shopkeep: 'That' poison could even kill lesser dragons after all.")
        input("Mysterious shopkeep: An undead is naturally weak to what killed them. Even common rat poison would have a similar effect.")
        input(self.name+':'+' '+"Oh, I see. I'll keep that in mind.")

    #Mysterious Shopkeep mentions your condition
    #Mysterious_Shopkeep_Condition.txt
    def npc12(self):
        input("Mysterious shopkeep:.......")
        input("The shopkeeper is staring at you with her piercing gaze.")
        input(self.name+':'+" "+"You're staring at me pretty intently. Is something up?")
        input("Mysterious shopkeep: You said you woke up in a the ruins with no memory of what happend right?")
        input(self.name+':'+" "+"Yeah that's about right.")
        input("Mysterious shopkeep: Are you sure your body is alright? You sle-")
        input("Mysterious shopkeep: I mean, waking up in such a place with no memory, did something happen to your body?")
        input(self.name+':'+" "+"I feel fine, a little out of it but that's probably because of the monsters I've been fighting.")
        input("She breathes a sigh of relief")
        input("Mysterious shopkeep: You really need to take better care of yourself...")
        input(self.name+':'+" "+"Oh? I didn't know you cared about me so much.")
        input(self.name+':'+" "+"I'm touched.")
        input("Mysterious shopkeep: You're my only customer so stay alive and happily purchase my items. Ok?")
        input(self.name+':'+" "+"We almost had a moment and you ruined it...")
    
    #Mysterious Shopkeep Talks About Dragons
    #Mysterious_Shopkeep_Dragon.txt
    def npc13(self):
        input(self.name+':'+" "+"I have a question.")
        input("Mysterious shopkeeper: Sure, depending on what it is you'll have to pay though.")
        input(self.name+':'+" "+"Always trying to earn more gold huh..")
        input(self.name+':'+" "+"Anyway, I hear dragons and humans got along. What happened?")
        input("Mysterious shopkeep: True, there was a time like that.")
        input("Mysterious shopkeep: At this time monsters were even more common than they were now.")
        input("Mysterious shopkeep: The dragons took pity on humanity, guarding them and providing them shelter. We clung to them like children.")
        input("Mysterious shopkeep: However no child can stay under their parents forever. Humanity grew in both numbers and strength.")
        input("Mysterious shopkeep: What they lacked in strength they made up for in terms of numbers and technology.")
        input("You're completely entranced in her story. She notices and smiles.")
        input("Mysterious shopkeep: Anddddd that's the end of the free trial!")
        input(self.name+':'+" "+"Huh?!")
        input("Mysterious shopkeep: Don't be so shocked, there's limits to what I know as well you know.")
        input("Mysterious shopkeep: Some people say the dragons attacked humanity because of an evil man")
        input("Mysterious shopkeep: Some say the dragons made a pact with the gods to protect humans for a certain amount of time and it expired.")
        input("Mysterious shopkeep: The church believes that humanity as a whole commited a sin and now this is our punishment.")
        input("Mysterious shopkeep: At this point it's impossible to tell. It happened so long ago after all.")
        input(self.name+':'+" "+"I see... I guess that makes sense. i guess there are somethings even you don't know huh.")
        input("Mysterious shopkeep:'Sorry, I can't give you the answers you want. You must obtain them yourself.'")

    #reocurring dialogue
    #Mysterious_Shopkeep_Reocurring.txt
    def npc14(self):
        input("Mysterious shopkeep: You've been talking to me quite a bit.")
        input("Mysterious shopkeep: Are you perhaps charmed by me?")

#shopkeeper randomized dialogue
    def shopkeeper_altdialogue(self,shopkeeperAltDialogue,len_original):
        i=0
        if len(shopkeeperAltDialogue) != 0:
            while i!=1:
                try:
                    choice=random.randint(0,len_original)
                    shopkeeperAltDialogue[choice]()
                    shopkeeperAltDialogue.pop(choice)
                    i+=1
                    
                except:
                    pass
        else:
            self.npc14()
            
            


#Shopkeeper
    def shopkeeper(self,shopkeeper_count):
        check = True
        if len(shopkeeper_count) == 1:
            self.npc9()
            shopkeeperAltDialogue={1:self.npc10,2:self.npc11,3:self.npc12,4:self.npc13}
            len_original=len(shopkeeperAltDialogue)
            town_phase.append(1)
            shopkeeper_count.pop(0)
        self.npc8(shopkeeper_hint,werewolf_clue1,werewolf_hints)
        self.npc6()
        self.npc_check()
        while check == True:
            input("welcome!")
            print("1: Talk")
            print("2: Buy")
            print("3: Sell")
            print("4: Exit")
            confirmation = input("What will you do? input the number corresponding to your choice: ")
            while confirmation != "1" and confirmation != "2" and confirmation != "3" and confirmation !="4":
                confirmation = input("What will you do?: input the number corresponding to your choice.")
            if confirmation == "1":
                input("you decide to speak to the Mysterious shopkeep.")
                self.shopkeeper_altdialogue(shopkeeperAltDialogue,len_original)
            elif confirmation == "2":
                self.shop(items_shop,items_shop_list,inventory)
            elif confirmation == "3":
                self.shop_sell(inventory,items_sell,books)
            elif confirmation == "4":
                check = False
                input("Mysterious shopkeep: Come again!")
        self.town(town_phase)
            
    
    #Awakening.txt
    def wakeup(self):
        input("???: It seems like it's time for you to wake up.")
        input("???: This ... story is to be an intresting one. With these eyes I forsee three possible endings.")
        input("???: I advise you to think carefully before you make your decisions. Your very fate depends on it.")
        input("???: Now then, the stage is set and the actors are waking from their slumber. Without further ado, the play will begin. Do be sure to entertain me.")
        input("You wake up to the feeling of cold metal. You crawl out of the sarcophagus tired and confused.")
        input("???: my name... that's right.. I'm.")
        input("(This will only be asked once, if you leave the character name blank a default name will be used instead)")
        mcname=input("Please enter the name of this character: ")
        mcname=mcname.strip()
        if len(mcname)== 0:
            mcname="Rion"
        input("???: That's right. My name is"+' '+ mcname)
        self.name=mcname
        input(self.name+':'+ " "+"It looks like there's some stuff with me")
        input(self.name+' '+"Gained a rusty dagger!")
        inventory.append("rusty dagger")
        input(self.name+' '+"Gained a sword!")
        inventory.append("sword")
        input(self.name+' '+"Gained a sword?")
        inventory.append("???")
        input(self.name+':'+ " "+"This sword... whenever I try unsheathing it my body freezes. Honestly, it seems quite sinister but it might be a clue as to who I am.")
        input(self.name+':'+ " "+"Other than my name, I can't remember anything.why I'm here, who I am... I can't recall anything.")
        input(self.name+':'+" "+ "For now though, I should leave this place so that I can find out more about myself.")
        input("you swing the sword around for a bit.")
        input("Hopefully I won't have to use this, as for why I can wield this so well... Was I a mercenary or something?")
        input(self.name+' '+"equipped the sword.")
        self.weapon="sword"
        inventory.remove("sword")
        self.attck=(self.str+weapons[self.weapon])
    
    #Werewolf confrontation part 1
    def werewolf_confirmation(self):
        #plays when all 3 clues are uncovered
        input("CONDITION HERE")
        input(self.name+':'+' '+"'I think I have enough information.'")
        input(self.name+':'+' '+"'It looks like I have to confront this father David fellow.'")
        input("The sky grows dark and the moon rises.")
        input(self.name+':'+' '+"'It's getting dark but I have no choice, I better make the final preparations before I go however.'")
        input(self.name+':'+' '+"'I hope I'm wrong about this...")
        confirmation=input(self.name+':'+' '+"Am I ready to face the culprit? yes/no ")
        confirmation=confirmation.strip()
        while confirmation != "yes" and confirmation != "no":
            confirmation=input(self.name+':'+' '+"Am I ready to face the culprit? yes/no ")
            confirmation=confirmation.strip()
        if confirmation == "yes":
            self.werewolf_dialogue()
            self.battle(Werewolf,fight_counter)
        else:
            input(self.name+':'+' '+"I should prepare first.")
            #bring back the choices
    
    #Werewolf.txt
    def werewolf_dialogue(self):
        input("CONDITION HERE")
        input("You enter the church in the dead of night, in the darkness one man bathes in the moonlight. On his knees in prayer.")
        input(self.name+':'+' '+"Father David, we have to discuss something.")
        input("The priest rises to his feet. The room is covered in a sickening aura.")
        input("Father David: I'm sure you already know the answers to any question you might ask me.")
        input(self.name+':'+' '+"So you expected this.")
        input("Father David: This would happen eventually, this simply happened ahead of schedule.")
        input(self.name+':'+' '+"So you have no qualms on killing innocents? I thought your doctrine was better than that.")
        input("Father David: You mean those blasted dragon worshipping fools?!")
        input("The priest's face twisted in rage, becomming beastial in nature.")
        input("Father David: Those people kidnapped young children and indoctrinated them into their little cult!")
        input("Father David: Those who rebelled against them ended up like me!")
        input("Father David tore off the sleeve of his white robes revealing the sign of the cross, seered into his very flesh.")
        input("People believed he had gotten it as a sign of devotion to the faith. but that was False. It was a brand.")
        input("Father David: They branded us like animals! Treated us like filth because we didn't believe!")
        input("Father David: Such people don't deserve to live! That's what I have determined! Anyone who condones them will be granted death as well!")
        input("Father David: A race that condonnes this savagery doesn't deserve to exist!")
        input(self.name+':'+' '+"So you infilitrated the church to continue your murders?")
        input("Father David: Unlike normal people clergy men can leave and enter as they see fit.")
        input("Father David: Dragons don't much care for us since we're so devoted to pleasing them.")
        input("Father David: Aren't you the same as me who despises this miserable race? ")
        input("Father David: You reek of blood.")
        input(self.name+':'+' '+"!")
        input(self.name+':'+' '+"I don't care what happened to you. You got innocents involved! What did they ever do?!")
        input(self.name+':'+' '+"Don't you dare compare me to you!")
        input("Father David: Hmph, so you're like the rest after all! Then die here!")
        input("Father David commences his gruesome transformation growing taller and gaining a wolf-like body.")
        input(self.name+':'+' '+"It's now or never! Let's end this!")
        input("The two of you fight, bathed in moonlight.")
    
    #Minotaur Confirmation
    def minotaur_confirmation(self):
        input("CONDITION HERE")
        input("Before you stands the rotting corpse of a giant man.")
        input("The armor the giant of a man once wore is now dull and useless")
        input("On it's exposed skull sits a helmet with horns that ressemble a bulls")
        input("In it's hands is a giant dual edged axe.")
        input("It stands completely motionless but your instincts tell you that once you take a step into it's lair, the fight will begin.")
        confirmation =input("Will you face the minotaur? yes/no ")  
        confirmation=confirmation.strip() 
        while confirmation != "yes" and confirmation != "no":
            confirmation =input("Will you face the minotaur? yes/no ") 
            confirmation=confirmation.strip()
        if confirmation == "yes":
            self.battle(Minotaur,fight_counter)
        elif confirmation == "no":
            #go back a space
            pass
    
    #Gargoyle Confirmation
    def gargoyle_confirmation(self,action_count,first_encounter):
        if len(action_count) == 0 and len(first_encounter)== 0:
            input("CONDITION HERE")
            input("You approach the statue that holds a stone halberd. On it's head sat horns and on it's back were bat-like wings")
            input(self.name+':'+' '+"'What a weird statue... Whatever I'll just go...")
            input("You take a step forward")
            input("Your instincts scream out from the wave of blood lust directed at you")
            input("You jump back")
            input("The ground where you stood now has a deep groove in it.")
            input(self.name+':'+' '+"'If I didn't jump out of the way my legs would be gone!'")
            input("You look at the stone sentinel, now in a new pose after swinging the halberd")
            input(self.name+':'+' '+"'I don't think it'll react so long as I stay in this room.' ")
            input(self.name+':'+" "+"This things too strong, I'm not sure if I can win if I face it head on.")
            decision = input("Will you face the gargoyle? yes/no ")
            while decision != "yes" and decision != "no":
                decision = input("Will you face the gargoyle? yes/no ")
            if decision == "yes":
                self.boss_battle3(Gargoyle,action_count)
            elif decision == "no":
                input(self.name+':'+' '+"No, there's no need to rush. I should prepare.")
            first_encounter.append(1)
        
        elif len(action_count) == 0:
            decision = input("Will you face the gargoyle? yes/no ")
            while decision != "yes" and decision != "no":
                decision = input("Will you face the gargoyle? yes/no ")
            if decision == "yes":
                self.boss_battle3(Gargoyle,action_count)
            elif decision == "no":
                input(self.name+':'+' '+"No, there's no need to rush. I should prepare.")
        elif len(action_count) == 1:
            input("The debris caused immense damage to the Gargoyle")
            input("Half of it's body is broken leaving one horn, one eye, and one hand for it's halberd.")
            input("In it's half caved chest is a glowing red stone.")
            input(self.name+':'+' '+"That must be it's weakness! Alright, now I have a chance!")
            decision = input("Will you face the gargoyle? yes/no ")
            while decision != "yes" and decision != "no":
                decision = input("Will you face the gargoyle? yes/no ")
            if decision == "yes":
                self.boss_battle3(Gargoyle,action_count)
            elif decision == "no":
                input(self.name+':'+' '+"No, there's no need to rush. I should prepare.")
        



    #Ending_Neutral.txt
    def ending_neutral(self):
        input(self.name+':'+' '+"... is remembering really that important?")
        input("You think back against your fight against father David.")
        input(self.name+':'+' '+"He wasn't the strongest out there and I still almost died.")
        input(self.name+':'+' '+"There's no point in knowing who I am if it gets me killed.")
        input(self.name+':'+' '+"'and what Father David said still bothers me.'")
        input(self.name+':'+' '+"I should go tell the shopkeeper that I don't need her help anymore.")
        input("You head to see the mysterious shopkeep")
        input("Mysterious shopkeep: I see you've made a decision she said with a smile")
        input(self.name+':'+' '+"I have, I no longer wish to know who I am. It's better this way.")
        input("Myserious shopkeep: Are you afraid of who you were?")
        input(self.name+':'+' '+"'can she read my mind or something?'")
        input(self.name+':'+' '+"Yeah, he said I reeked of blood and that I was dangerous")
        input(self.name+':'+' '+"If I was a bad person, remembering might make me go back to being that person.")
        input(self.name+':'+' '+"Since that's the case I'd rather not remember.")
        input(self.name+':'+' '+"Right now I just want a peaceful life free of that type of worry.")
        input("Mysterious shopkeep: Rather than seek atonement you would live in ignorance.")
        input(self.name+':'+' '+"It's cowardly, I know. But it's my choice, I'm just tired of it all.")
        input("Mysterious shopkeep: It is cowardice, I won't deny that.")
        input("Mysterious shopkeep: but I won't condemn you.")
        input("Mysterious shopkeep: From the very beginning I decided that I would respect your decision.")
        input("Mysterious shopkeep: It is a shame though, if you don't continue adventuring then you will have no need for this store.")
        input(self.name+':'+' '+"That's true however I'll still drop by to see you.")
        input("Mysterious shopkeep: My, dropping by just for me? I'm honoured")
        input("You and the shopkeep continue to chat for a bit before it's time for you to leave")
        input("As you leave you turn to see her once more. The beautiful woman with the odd hat and fun demeanor")
        input("You don't know why but you burn that image into your eyes, framing it in your memory for all eternity")
        input("Mysterious shopkeep: Goodbye, my one and only customer.")
        input("Mysterious shopkeep: I'll do my best to protect that blissful paradise you reside in. So please be happy.")
        input("Years pass")
        input("After you defeated Father David the town readily accepts you")
        input("Officially, you are the towns investigator however there are very few things you need to do.")
        input("Sometimes you wander around in the village, always ending up in the same place.")
        input(self.name+':'+' '+"'I had the dream again..'")
        input("In the dream he saw a beautiful woman who wore a comically large witch's hat.")
        input("She would smile at him from beyond her shop counter.")
        input(self.name+':'+' '+"'she... she was crying'")
        input("In his dreams he noticed the underlying sorrow in that smile, highlighted by a single tear that fell from her eyes.")
        input("He looked up ahead at the empty land, he always thought something should be there. A shop of sorts")
        input("When he asked the villagers they all agreed that both the woman he saw and the shop he described didn't exist.")
        input("The man he remembered buying the information from was reported dead many years before he arrived.")
        input("These mysteries continued to add up however he would never investigate them.")
        input("He had chosen to live in blissful ignorance, as such he had no right to the truth.")
        input("That was his cross to bear.")
        input("He lived until the age of 90 before eventually dying of old age. His headstone placed on the land he would wander into.")
        input("???: It looks like you lived well in this paradise of ignorance.")
        input("A beautiful woman clad in magical armor wielding a staff approached the lonely grave.")
        input("On her head was the very same comical witche's hat, in over 70 years she appeared unchanged.")
        input("Mysterious shopkeep: In the end no matter what happened, we lost. Without you, we couldn't fight them back.")
        input("Mysterious shopkeep: No, even with you standing with us we may still have lost.")
        input("Mysterious shopkeep: I'm the only one who's still here, today will be my final battle.")
        input("She took off her hat and placed it on the gravestone.")
        input("Mysterious shopkeep: Although it's late, I'll return this to you for now.")
        input("Mysterious shopkeep: I'll see you soon. Until then, hold onto it for me, until I breathe my last.")
        input("Monsters of all sorts burst forth, attacking her.")
        input("Mysterious shopkeep: This will be my final battle, grand witch Morgan won't go down easily!")
        input("Netural ending: Paradise of ignorance in the ruined world Complete!")

    #Ending_Bad.txt
    def ending_bad(self):
        input("You stand no chance against the dragon's awesome might")
        input("???: So this is where it ends.")
        input("???: In the end I couldn't save you... I'm sorry.")
        input("Game over")
        






#The hero
#Rion=Hero("Rion",0,10,5,120,120,3,7,9,"unarmed",2,3,4,0,100,500)
Rion = Hero("Chad",999,999,999,999,999,999,999,999,"sword",999,999,999,999,999,99999999)





class Enemy:
    def __init__(self, name, strength, vitality, defence, agility, exp, money):
        self.name = name
        self.attck = strength
        self.vit = vitality
        self.agl = agility
        self.defence = defence
        self.exp = exp
        self.drop = money

    def attack(self,enemy):
        damage = self.attck - enemy.defence
        return(damage)

    def special(self,enemy):
        if self.name == "Werewolf":
            if len(werewolf_special) == 0: 
                if self.vit <= 250:
                    chance=random.randint(0,3)
                    if chance == 1:
                        
                        input("The werewolf looks at you with hungry eyes, it's claws gleaming in the moonlight.")
                        werewolf_special.append(1)
                        return(0)
                    else:
                        damage=self.attack(enemy)
                        return(damage)
                else:
                    damage=self.attack(enemy)
                    return(damage)
                
            else:
                damage=(self.attck*2 - enemy.defence)
                return(damage)
        elif self.name == "Gargoyle":
            if len(gargoyle_special) == 0:
                if self.vit <= 350:
                    chance = random.randint(0,4)
                    if chance == 1:
                        input("The stone sentinel lifts it's spear quietly in preparation.")
                        gargoyle_special.append(1)
                        return(0)
                    else:
                        damage=self.attack(enemy)
                        return(damage)
                else:
                    damage = self.attack(enemy)
                    return(damage)
            else:
                damage = (self.attck - enemy.defence)
                return(damage)
        else:
            damage = self.attack(enemy)
            return(damage)

    def process(self, enemy,damage):
        
        if damage <= 0:
            if damage == 0 and (self.name=="Werewolf" or self.name=="Gargoyle"):
                pass
            else:
                input("The attack from"+' '+self.name+' '+"did no damage!")
        
        else:
            if self.name == "Werewolf":
                if len(werewolf_special) == 1:
                    input("The werewolf unleashes a flurry of blows in the blink of an eye!")
                    for i in range(5):
                        input(enemy.name+' '+ "lost"+ ' '+str(damage)+' Hp!')
                        enemy.Hp = enemy.Hp - damage
                    werewolf_special.pop(0)
                else:
                    input(enemy.name+' '+ "lost"+ ' '+str(damage)+' Hp!')
                    enemy.Hp = enemy.Hp - damage
            elif self.name == "Gargoyle":
                if len(gargoyle_special)== 1:
                    input("The gargoyle slams the spear down for massive damage!")
                    input(enemy.name+' '+ "lost"+ ' '+str(damage)+' Hp!')
                    enemy.Hp = enemy.Hp - damage
                    gargoyle_special.pop(0)
                else:
                    input(enemy.name+' '+ "lost"+ ' '+str(damage)+' Hp!')
                    enemy.Hp = enemy.Hp - damage          
            else:
                input(enemy.name+' '+ "lost"+ ' '+str(damage)+' Hp!')
                enemy.Hp = enemy.Hp - damage      


            
Goblin=Enemy("Goblin",20,30,2,10,25,10)
Fafnir=Enemy("Fafnir",300,10000,300,250,100000000,10000000000)
Werewolf = Enemy("Werewolf",70,500,10,30,1000,1000)
Minotaur = Enemy("Minotaur",60,200,20,10,500,400)
Gargoyle = Enemy("Gargoyle",100,700,400,300,10000,3000)
Kobald = Enemy("Kobald",40,90,20,30,60,100)

def game():
    Rion.wakeup()
    Rion.minotaur_dungeon(book3_flag,book1_flag,book8_flag,book2_flag,potion_flag,Volitile_poison_flag,Minotaur_kill_count)
    Rion.npc1()
    Rion.town(town_phase)

    
#Rion.minotaur_dungeon(book3_flag,book1_flag,book8_flag,book2_flag,potion_flag,Volitile_poison_flag,Minotaur_kill_count)

#Rion.Gargoyle_dungeon_base_floor(action_count,first_encounter,book4_flag,potion1_flag,basement_key_flag,Gargoyle_kill_count)

#Main
##################################################################
game()
input("Thank you for playing my game. Hope you had fun. Look forward to the next time.")
input("For those of you who didn't reach the true ending then I implore you to try again and be more vigilant")
if Rion.name == "wiltley" or Rion.name == "Wiltley" or Rion.name == "abdi" or Rion.name == "Abdi" or Rion.name == "abd" or Rion.name == "Abd" or Rion.name == "Abdennour" or Rion.name == "abdennour":
    input("I'm assuming you didn't look at the source code... right?")
    input("Tell me if you managed to reach the true ending or if I created a ridiculous a bug again.")
    input("Hope you had fun :)")