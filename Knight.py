weapons={"sword":10,"poisoned sword":12,"silver sword":20,"rusty dagger":1,"poisoned rusty dagger":2,"lance":5,"silver lance":10,"???":999999,"unarmed":3}
items_shop_list=["old map", "old bread","potion"]
items_shop={"old map":1000,"old bread":50,"potion":150,"moonstone":300,"silver polish":50}
items_sell={"sword":100, "lance":80,"old bread":10, "potion":50, "rusty dagger":20,"silver lance":100,"silver sword":150}
books = ['Gospel of the dragons',"History book" "Ruined journal #1","Ruined journal #2", "Ruined journal #3", "Demons", "old book", "Items"]
items={"Volatile Poison","silver polish","emblem","moonlit map",'Gospel of the dragons', "Ruined journal #1","Ruined journal #2", "Ruined journal #3", "Werewolf tooth"
"Demons", "old book","History book", "Items","moonstone","basement key", "upstairs key"}
combinable_items=["Volitile poison", "silver polish","lance", "rusty dagger", "sword", "old map", "moonstone"]
consumable_item={"old bread":20,"potion":50}
inventory=[]
class Knight:
    def __init__(self, name, level, strength, vitality, Hp, HPcap, agility, magic, defence, weapon, exp, expcap, money):
        self.Hp = Hp
        self.name = name
        self.str = strength
        self.weapon = weapon
        self.attack = strength + weapons[weapon]
        self.vit = vitality
        self.agl = agility
        self.stance = "Normal"
        self.mag = magic
        self.defence = defence
        self.exp = exp
        self.expcap = expcap
        self.Hp = Hp
        self.Hpcap = HPcap
        self.bal = money
        self.lvl = level