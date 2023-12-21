# Entity Classes
The entity classes are classes that are meant to interact with each other closely.
Some represent both the player character and the bosses/mobs that are encountered in game.
Other classes in this package focus on facilitating the interaction between Entities in some ways.

### Entity
The entity class is the parent class of all other game entities. It contains the basic
functions of all entities serving as a template that the other entities inherit from.
It contains the object attributes that all entities have like Hp, Strength etc. It contains the 
`take_damage()`, `attack()`, `apply_bonuses()` and `remove_bonuses()`. `attack()` is the standard damage
calculation done when 2 entity objects fight. `take_damage()` is used when the entity object is receiving damage.
`apply_bonuses()` is used to apply stat buffs to the entities stats. `remove_bonuses()` is used to take away the 
buffs. Theses are all functions entities will need access to.

### Knight
Knight is the player character's object. It contains all the stats that are associated with an
RPG protagonist, Hp, Mp, attack etc. This object also has the status variable which indicates the status
of the knight object for use in the game. For example if status is not normal, movement cannot be performed by the knight. 
This is helpful for when the player really shouldn't be moving like if they're in a fight, reading dialogue
or just dead.

As the object for the player character, this class has some unique functions such as, `level_up()`, `get_rewards()` and `load_dict()`.
`level_up()` is self-explanatory, it increases the level attribute of the knight and increases the object's stats based on 
predefined growths. These growths have yet to be set in stone. `get_rewards()` is a function meant to be used in conjunction with 
the future BattleManager class. It takes in all the rewards from winning a battle(exp, money, items) and adds it to the 
Knight object. `load_dict()` is a function that is used to load the save data for the knight object into the current object, updating it 
to match what is in the save file.

### Enemy
The entity class used for the enemy objects in the game. This includes both normal enemies and boss type enemies.
This class pulls all it's information from JSON templates stored under the JSON folder. Unlike other entities,
this class has access to unique buffs and weaknesses for gameplay purposes. Objects of this class are created via the 
EntityFactory class.

As a result, this function has some unique functions. These functions are `take_attack()` and `die()`. `take_attac()` is a Enemy exclusive
version of Entity's `take_damage()` function. The `take_attack()` function calls `take_damage()` and if the damage is fatal, it calls the `die()` function.
the `die()` function, adds the experience, bal, and inventory attribute values to a lootpool(a dictionary of rewards the player gets if they win).

### EntityFactory
This is a factory object that produces entities. At the moment, it only produces Enemy type entities.

### AnimationManager
The knight character's exclusive animation manager. This class is responsible for displaying the proper animations
for the knight. This is de-coupled from the rest of the managers since it is not for the game at large.

