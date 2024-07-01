class Equipment:

    def __init__(self, name, jsonInfo):
        self.name = name
        self.statsApplied = False  # flag to prevent stat loss
        self.attribute = jsonInfo["Attribute"]
        self.type = jsonInfo["Type"]
        self.Hpcap = jsonInfo["Hpcap"]
        self.Mpcap = jsonInfo["Mpcap"]
        self.Str = jsonInfo["Str"]
        self.Mag = jsonInfo["Mag"]
        self.Agl = jsonInfo["Agl"]
        self.Def = jsonInfo["Def"]
        self.movelist = jsonInfo["Movelist"]

    def apply_stat_bonuses(self, knight):
        self.statsApplied = True  # set the flag to true
        for i in range(len(self.movelist)):
            knight.moveList.append(self.movelist[i])
        # Add to knight's stats
        knight.__dict__["Hpcap"] += self.Hpcap
        knight.__dict__["Mpcap"] += self.Mpcap
        knight.__dict__["Str"] += self.Str
        knight.__dict__["Mag"] += self.Mag
        knight.__dict__["Agl"] += self.Agl
        knight.__dict__["Def"] += self.Def

    def remove_stat_bonuses(self, knight):
        if self.statsApplied:  # only lets stats be removed if item was equipped
            self.statsApplied = False  # set the flag to false
            for i in range(len(self.movelist)):
                knight.moveList.remove(self.movelist[i])
            # subtract to knight's stats
            knight.__dict__["Hpcap"] -= self.Hpcap
            knight.__dict__["Mpcap"] -= self.Mpcap
            knight.__dict__["Str"] -= self.Str
            knight.__dict__["Mag"] -= self.Mag
            knight.__dict__["Agl"] -= self.Agl
            knight.__dict__["Def"] -= self.Def

