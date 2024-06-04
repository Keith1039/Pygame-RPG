from Entity.Enemy import Enemy
import json

class EntityFactory:
    def __init__(self):
        self.path = "JSON/Enemies/"
        self.createdCount = {}  # keeps track of how many of a certain enemy it made

    def create_entity(self, name):
        path = self.path + name + ".json"  # Creates the path to the JSON file
        file = open(path, "r")  # Open with read permissions
        jsonInfo = json.load(file)  # Load the JSON information as dict
        file.close()  # Close file
        enemy = Enemy(jsonInfo)  # Return an enemy of that JSON template
        if self.createdCount.get(name) is None:
            # add the enemy name to the count
            self.createdCount.update({name: 1})
        else:
            self.createdCount[name] += 1  # increment the value by 1
            enemy.Name = enemy.Name + str(self.createdCount[name])  # add the number to the name
        return enemy  # return enemy

    def clear_created_count(self):
        # clears the created count for next time
        self.createdCount.clear()
