from Entity.Move import *
from Entity.Knight import Knight

knight = Knight()

testString1 = "Str * Lvl"
testString2 = "Str * 100-Hp%"  # modified desperato
testString3 = "Str * 0.7"  # normal format for string
testString4 = "Vit * .4"  # different format for float numbers

def test_isfloat():
    # check if it confirms that float numbers and integers are allowed and non-numeric strings aren't
    flag = isfloat(".3") and isfloat("0.4") and isfloat("1") and not isfloat("1a")
    assert flag

def test_replace_all_stats_with_values():
    flag = replace_all_stats_with_values(testString1, knight) == "1 * 1"
    assert flag

def test_look_for_special_symbols():
    flag = look_for_special_symbols(testString2)
    flag2 = look_for_special_symbols(testString1)
    # verify that we don't have any misfires
    assert flag and not flag2

def test_parse_special_symbols():
    newTestString1 = replace_all_stats_with_values(testString1, knight)
    flag = parse_special_symbols(newTestString1.split()[2], knight) == 1.0  # should return a float
    flag2 = parse_special_symbols(testString2.split()[2], knight) == 0.0
    flag3 = parse_special_symbols(testString3.split()[2], knight) == 0.7
    flag4 = parse_special_symbols(testString4.split()[2], knight) == 0.4
    assert flag and flag2 and flag3 and flag4

def test_parse_damage_calculation():
    flag = parse_damage_calculation(testString1, knight) == 1
    flag2 = parse_damage_calculation(testString2, knight) == 0
    flag3 = parse_damage_calculation(testString3, knight) == 1  # rounds up because .7 > .5
    flag4 = parse_damage_calculation(testString4, knight) == 0  # rounds down because .4 < .5
    flag5 = parse_damage_calculation("", knight) == 0  # check to see if empty string damage calculation works
    assert flag and flag2 and flag3 and flag4 and flag5
