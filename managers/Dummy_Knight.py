class Knight():
    def __init__(self, name="Rion", level=1, strength=1, vitality=1, Hp=1, HPcap=1, agility=1, defence=1, exp=1, expcap=1, money=1):
        self.Hp = Hp
        self.Hpcap = HPcap
        self.Name = name
        self.Lvl = level
        self.Str = strength
        self.Vit = vitality
        self.Agl = agility
        self.Status = "Normal" 
        self.Stance = "1"
        self.Defence = defence
        self.Exp = exp
        self.Expcap = expcap
        self.Bal = money
    
    def levelup(self):
        self.Lvl += 1
        self.Hp += 50
        self.Str += 30
        self.Vit += 10
        self.Agl += 20
        self.Defence += 30
        self.Exp = 0
        self.Expcap += 100

    def load_dict(self, knightDict):
        self.__dict__ = knightDict

    def __eq__(self, other):
        return self.__dict__ == other.__dict__