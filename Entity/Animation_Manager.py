knightAttack = 4, "Knight/Cut_Sprites/Attack_1 "
knightRunR = 10, "Knight/Cut_Sprites/Run_R "
knightRunL = 10, "Knight/Cut_Sprites/Run_L "
knightIdle = 10, "Knight/Cut_Sprites/Idle "
knightDeath = 10, "Knight/Cut_Sprites/Death "

aniArray = {"Knight Attack": knightAttack, "Knight Run R": knightRunR, "Knight Run L": knightRunL, "Idle": knightIdle,
            "Death": knightDeath}
class AnimationManager:

    def __init__(self):
        self.aniArray = []

    def change_array(self, name):
        self.aniArray = aniArray.get(name)

