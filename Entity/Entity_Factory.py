from Entity.Enemy import Enemy
import json

class EntityFactory:
    def __init__(self):
        self.path = "JSON/Enemies/"

    def create_entity(self, name):
        path = self.path + name + ".json"  # Creates the path to the JSON file
        file = open(path, "r")  # Open with read permissions
        jsonInfo = json.load(file)  # Load the JSON information as dict
        file.close()  # Close file
        return Enemy(jsonInfo)  # Return an enemy of that JSON template
