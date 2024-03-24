import json
from managers.Equipment import Equipment
from managers import Knight
file = open("JSON/Items/Equipment.json", "r")
equipmentJson = json.load(file)  # dict with all equipment info
file.close()

knight = Knight()
rustyDagger = Equipment("Rusty Dagger", equipmentJson["Rusty Dagger"])
stats = ["Hpcap", "Mpcap", "Str", "Mag", "Agl", "Defence"]
oldStats = knight.__dict__.copy()
def test_apply_stat_bonuses():
    rustyDagger.apply_stat_bonuses(knight)  # the flag should be triggered
    flag = False
    for i in range(len(stats)):
        stat = stats[i]  # the stat we care about
        difference = knight.__dict__[stat] - oldStats[stat]  # the difference between the stats
        flag = difference == rustyDagger.__dict__[stat]  # compare the difference to equipment attribute
        if not flag:
            break
    flag2 = "Pilfering Strike" in knight.moveList
    assert flag and flag2 and rustyDagger.statsApplied

def test_remove_stat_bonuses():
    rustyDagger.remove_stat_bonuses(knight)  # removes the stat bonuses
    flag = not rustyDagger.statsApplied  # check if the flag has been changed to false
    rustyDagger.remove_stat_bonuses(knight)  # this should do nothing now
    flag2 = oldStats == knight.__dict__
    flag3 = "Pilfering Strike" not in knight.moveList
    assert flag and flag2 and flag3
