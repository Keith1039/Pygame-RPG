knight_attack = 4, "Knight/Cut_Sprites/Attack_1 "
knight_run_R = 10, "Knight/Cut_Sprites/Run_R "
knight_run_L = 10, "Knight/Cut_Sprites/Run_L "
knight_idle = 10, "Knight/Cut_Sprites/Idle "

class AnimationManager:

    def __init__(self):
        self.ani_array = []

    def Change_array(self, name):
        if name == "Knight Attack":
            self.ani_array = knight_attack

        elif name == "Knight Run R":
            self.ani_array = knight_run_R

        elif name == "Knight Run L":
            self.ani_array = knight_run_L

        elif name == "Idle":
            self.ani_array = knight_idle



test = AnimationManager()
test.Change_array("Knight Attack")
print(len(test.ani_array))
print(len(knight_attack))