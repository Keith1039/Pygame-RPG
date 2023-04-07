### Pygame RPG

This is a RPG I'm making that is based off an older version called
rpg_1_prototype.py which is in this same repo for now. I thought it
would be fun to remake it with pygame instead of base python but I'm slowly 
regretting my own decision. Oh well, at least it's fun working on this. For now
this repo has a lot of free art assets. At the end of this project I'll add where 
I got these assets if I ended up using them. Hopefully that'll get some of these
artists more recognition :).

## Story

This RPG has the player play as a knight who has just woken up with amnesia. They 
find themselves in a dark cave. You must then take control of the knight and 
make your way through the cave that they woke up in to discover more about
the world and themselves. The story of the world is fed to the player through
dialogue and books(why books? Because I love books). 
See if you can find the true ending of this short tale.

## Features

- Interactable NPCs
- Stanced and turn based system (planned)
- Standard RPG mechanics

### Developper portion

This portion is mostly so I remeber what some of these classes do and also here to explain
bash script instructions if I add more.

# init.sh 
A Script that automatically runs Jenkins and changes my Github repos webhook 
so Jenkins can work properly. Feel free to grab this if you also can't afford a 
server that runs Jenkins 24/7. If you do decide to grab this script heres some things you
should know.

1. This script uses a github token to authenticate the curl command to the github api in 
order to change the webhook. This is stored in a file called Git_key on my own computer.
If you want to use the script as it is you should have a token in a file in the same directory
called **Git_key**. You should add this to a .gitignore file so you don't accidently push 
your token to the repo by accident.

2. This script is hardcoded to change MY repo's webhook so fill your repos path instead of 
mine and you should be fine

## classes relating to the Knight

# Knight
Has the Kstatus class which indicates the status of the knight object for use in the game
for example if status is not normal, movement cannot be performed by the knight. This is 
helpful for when the player really shouldn't be moving like if their in a fight, reading dialogue
or just dead.

Also contains the stat line for the knight. I plan to add functions for use in combat and a 
`levelUp()` function.

# Animation_Manager
The knight characters animation manager. This class is responsible for displaying the proper animations
for the knight. Like all of the other manager classes, an improvement for this class will be making the
`change_array()` function use a dictionary to find the proper array instead of 'if' statements.

## Manager classes

These classes are responsible for managing the animations on screen whether it's the 
NPCs animations or an object's animation. All of these classes will receive an upgrade to their 
`change_array()` functions to use dictionaries instead of 'if' statements.


# NPCAnimationManager
Uses a context to determine which npcs should be present and what animations should play. Usually plays
an idle animation of some sort.

# ObjectAnimationManager
A manager class dedicated to object animations. At the moment this class is only used for the animation
that plays when the player opens a chest facing either direction. It's `change_array()` function is the 
most complex out of the managers so far. It takes in a list called 'interactable' which holds information
about any interactable object.

The first index of interactable is a tuple which contains where the player must be in order to interact
with the object. The second index contains the name of the interactable object and the final index has boolean
which tells the system whether this item can be interacted with. for example, if the chest hasn't been opened,
the boolean is false but once you open it, the boolean will be true. A colleague of mine told me that making 
a smaller class would be better instead of using lists and I might use that in the future.

Once the player is deemed to be 
interacting with the object this class will set the knight's status to 'Opening_chest' which will disable
the players ability to move until the chest has been opened. Its `set_array()` function is pretty redundant so
I will probably remove it at some point.

# ScreenManager
The class that is responsible for drawing the screen. Well actually, it holds the information that gets drawn 
on the screen but that's semantics. Unlike the other managers that require a context of some sort, this is the
class that actually determines said context. instead of a `change_array()` function it has a `changeScreen()`
function which changes the screen based on the previous screen and the previous context. This class also
determines the interactable objects on the screen which is determined by it's `applyContext()` class. 

I should probably make more descriptive function names for the manager classes so no one get's confused. I'll
address that in another PR.

## UI

These classes are responsible for the user interface so things like the menus, minimap etc.
Since I'm allergic to anything that anything even remotely resembling front end, I'm doing this part last.

# MapInfo
The class that has all of the dungeon events and information. Things like bos encounters, enemy encounters
and the such are recorded in this file. The class itself holds information of events in dungeons and whether
they have been accessed or not. This is all stored in dictionaries inside the map class. Which dict is in
use will be determined via a .... CONTEXT and be applied 

## Saving

Don't have a package for it yet but this section will be how the player saves the game.

## Credits