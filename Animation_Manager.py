knightAttack = 4, "Knight/Cut_Sprites/Attack_1 "
knightRunR = 10, "Knight/Cut_Sprites/Run_R "
knightRunL = 10, "Knight/Cut_Sprites/Run_L "
knightIdle = 10, "Knight/Cut_Sprites/Idle "
knightDeath = 10, "Knight/Cut_Sprites/Death "

class AnimationManager:

    def __init__(self):
        self.aniArray = []

    def change_array(self, name):
        if name == "Knight Attack":
            self.aniArray = knightAttack

        elif name == "Knight Run R":
            self.aniArray = knightRunR

        elif name == "Knight Run L":
            self.aniArray = knightRunL

        elif name == "Idle":
            self.aniArray = knightIdle

        elif name == "Death":
            self.aniArray = knightDeath



