This portion is mostly here so I remember what some of these classes do and also here to explain
bash script instructions if I add more.

# init.sh 
A Script that automatically runs Jenkins and changes my GitHub repos webhook 
so Jenkins can work properly. Feel free to grab this if you're like me and don't want a 
server that runs Jenkins 24/7. If you do decide to grab this script here's some things you
should know.

1. This script uses a GitHub token to authenticate the curl command to the GitHub api in 
order to change the webhook. This is stored in a file called Git_key on my own computer.
If you want to use the script as it is you should have a token in a file in the same directory
called **Git_key**. You should add this to a .gitignore file, so you don't accidentally push 
your token to your GitHub Repo by accident.

2. This script is hardcoded to change MY repo's webhook so switch my repo's path with yours and 
it should work fine

# script
script is a file that has some useful scripts that I use in my workflows.

###  clear-save
clear-save is an option given to script that clears out the save folder

### fill-save
this is a call to a python script to populate the save folder with 4 save files.
This is mostly done so I can look at what my UI would look like with all 4 save files
filled.

### run-tests
Run tests does as its name suggests and runs tests for the entire project. The reason why
this is called instead of just running pytests is that pytests does not allow for keyboard
input to be run during the testing process. This was a problem for UIManager since the entire
class is mostly handling user input. As such, this script creates a folder called testDetails,
runs the tests for UIManager and saves the information in a json file for pytest and then calls pytest.
Once the pytest is done, the script deletes the testDetails folder.

Scripts.py
A script that accompanies the script file in helping with my workflows.
This file contains all the scripts that would be a pain to implement with bash such as the filling of
my save directory with dummy save files as well as the execution of the UI_manager tests as well as 
saving them in a json file.

# Manager classes

These classes are responsible for managing what happens in the game, whether it be drawing screens, saving the game state etc. 

### NPCAnimationManager
Uses a context to determine which NPCs should be present on screen and what animations should play. Usually plays
an idle animation of some sort.

### ObjectAnimationManager
A manager class dedicated to object animations. At the moment this class is only used for the animation
that plays when the player opens a chest facing either direction. It's `change_array()` function is the 
most complex out of the managers so far. It takes in a list called 'interactable' which holds Event type objects.

The class then goes through the list of 'interactables' and does the following:
The class checks if the player is within range of the Event(checks Event.range).
It then checks the type of Event(Event.eventType) and see's if the event relates to an object.
If the above are both true i.e. player is in range and this class can process the Event, it checks
if the event has been triggered before by looking at the boolean value of Event.activated.
If all conditions are met, the objects animation will start and the Knight object will be stuck in place until
the animation has finished.

### ScreenManager
The class that is responsible for drawing the screen. Well actually, it holds the information that gets drawn 
on the screen but that's semantics. Unlike the other managers that require a context of some sort, this is the
class that actually determines said context. instead of a `change_array()` function it has a `change_screen()`
function which changes the screen based on the previous context. This class also determines the interactable 
Event objects on the screen which is determined by its `apply_context()` function. 

### DialogueManager
The class responsible for managing the text boxes and the accompanying dialogue. This class takes in an 
Event object and looks to see if its Event.path value isn't empty. Unlike ObjectAnimationManager however, this 
class stores the Event object inside itself for future use. This class draws the assets displayed on screen for the
dialogue and then once the EOF has been reached, it clears the Event associated with it and sets the 
Event.activated to True(Not true in all cases, repeatable dialogue is an exception). For now the class does not contain 
an actual function for drawing and repeating the dialogue but it will be added later on. Currently, the function that handles
this is in Rpg2.py.

Another note is that the cutscenes (as of this moment) are completely automated, user input for progression
will be added later.

### SaveManager
This class is responsible for saving and loading information. The format chosen for the save files are json files. The 
reason why I chose json files is because, in python, object data can easily be stored in a dictionary and those dictionaries
can easily be converted into json data. Since python stores local variables in a dictionary, I can also easily save variable data.
This format makes storing and loading data simple and efficient. Another reason why json was picked was because it is 
easy for anyone to read. This helps when verifying bugs in the code.

The class has 4 main functions. it has `quick_save()`, `save()`, `quick_load()` and `load()`. 
All of these are variations of each other. The only difference between `quick_save()` and `quick_load()`compared
to `save()` and `load()` is that `save()` and `load()` requires a specific save slot to be given. The quick versions
of those functions just take the last used slot which is stored in the class itself. To ensure that the most recent save
slot is never lost, it's stored inside a json file called 'prev_save_data.json' and is loaded when the Object is created.

The load functions for this class also load the necessary information into the objects that need it such as ScreenManager,
Knight, etc.

### UIManager
This class is responsible for drawing the UI and handling the interactions between UI and keyboard input.
This class relies on an external file called UI_Manager_draw.py for more complex UI drawings such as the Load Game
screen. The class uses, what's displayable, X and Y restrictions along with the values of X spacing and Y spacing to determine how 
the UI is drawn. Currently, this class cannot fully handle user interaction as actually processing the user's choice 
will be handled by another class. In the future, the MapInfo Object may be used by this class for drawing the 
map for the player.

This class has a mini class called Cursor which handles the cursor aspect of the UI. The curser object is what handles
user input.

# Other classes

### MapInfo
The class that has all the dungeon events and information. Things like boss encounters, enemy encounters
and the like are recorded in this file. The class itself holds information of events in dungeons and whether
they have been accessed or not. This is all stored in dictionaries inside the map class. Which dict is in
use will be determined via the context and be applied appropriately. This class is unfinished and has not been 
fully implemented.

