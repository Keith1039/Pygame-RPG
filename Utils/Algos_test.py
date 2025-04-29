import Utils
from Utils import construct_matrix_given_parameters


def test_get_max_animation_val():
    sprite = "Entity_Sprites/Knight/"
    name = "Knight"
    aniStatus = "Idle"
    assert Utils.get_max_animation_val(sprite, name, aniStatus) == 10

def test_construct_matrix_given_parameters():
    # get the values from constraints
    # x_constraints = constraints["x_constraints"]
    # y_constraints = constraints["y_constraints"]
    # x_spacing = constraints["x_spacing"]
    # y_spacing = constraints["y_spacing"]

    # no y spacing
    constraints = {
        "x_constraints": (500, 600),
        "y_constraints": (500, 500),
        "x_spacing": 50,
        "y_spacing": 0,
    }
    items = []
    for i in range(3):
        items.append("blah")

    matrix = construct_matrix_given_parameters(constraints, items)

    flag = len(matrix) == 3 and len(matrix[0]) == 1 and len(matrix[1]) == 1 and len(matrix[2]) == 1
    flag2 = True
    # ensure that no list remains empty (each column has a minimum of 1 item always)
    for i in range(len(matrix)):
        flag2 = matrix[i][0] != []
        if not flag:
            break


    # check to see if the matrix can be uneven (all columns don't have the same number of items)
    constraints = {
        "x_constraints": (380, 1180),
        "y_constraints": (580, 730),
        "x_spacing": 400,
        "y_spacing": 75
    }
    items.clear() # clear the list
    for i in range(8):
        items.append("blah")

    matrix = construct_matrix_given_parameters(constraints, items)
    flag3 = len(matrix) == 3 and len(matrix[2]) == 2
    flag4 = True
    # ensure that no list remains empty (each column has a minimum of 1 item always)
    for i in range(len(matrix)):
        flag4 = matrix[i][0] != []
        if not flag3:
            break

    # check to see if the matrix can handle no x spacing
    constraints = {
        "x_constraints": (380, 380),
        "y_constraints": (580, 730),
        "x_spacing": 0,
        "y_spacing": 75
    }
    items.clear() # clear the list
    for i in range(3):
        items.append("blah")
    matrix = construct_matrix_given_parameters(constraints, items)
    flag5 = len(matrix) == 1 and len(matrix[0]) == 3
    assert flag and flag2 and flag3 and flag4 and flag5