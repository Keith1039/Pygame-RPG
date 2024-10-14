import os
def get_max_animation_val(sprite, name, aniStatus):
    # gets the maximum number for the animation in use
    fileList = os.listdir(sprite)  # get the list of files in the given sprite directory
    referenceString = name + "_" + aniStatus + "_"  # what we use to match
    matchingFiles = []  # a list of all the file names that match the reference string
    for fileName in fileList:  # loop through the file names
        if referenceString in fileName:  # if the name matches the reference string, add it to the list
            matchingFiles.append(fileName)
    matchingFiles.sort(key=sort_func)  # sort the list
    final = matchingFiles.pop()  # get the last item in the sortest list (the biggest)
    final = final.replace(".png", "")  # get rid of the png portion of the file name
    finalNum = int(final.split("_").pop())  # get the maximum number
    return finalNum

def sort_func(e):
    final = e.replace(".png", "")  # get rid of the png portion of the file name
    return int(final.split("_").pop())  # get the maximum number

def get_others(actor, selectedTargets, targets):
    others = []
    for target in targets:
        if target not in selectedTargets and target != actor:
            others.append(target)
    return others

def construct_matrix_given_parameters(constraints, items):
    matrix = []  # matrix we'll be returning

    # get the values from constraints
    x_constraints = constraints["x_constraints"]
    y_constraints = constraints["y_constraints"]
    x_spacing = constraints["x_spacing"]
    y_spacing = constraints["y_spacing"]

    columnNum = int((x_constraints[1] - x_constraints[0]) / x_spacing)  # should always be an even split
    rowNum = int((y_constraints[1] - y_constraints[0]) / y_spacing)
    # for i in range(columnNum):
    #     matrix.append([])

    columnPointer = 0
    firstLoop = True
    # fill in the matrix
    for i in range(len(items)):
        x_pos = x_constraints[0] + columnPointer * x_spacing
        y_pos = y_constraints[0] + int(i/rowNum) * y_spacing
        if firstLoop:
            matrix.append([])  # add the column
        matrix[columnPointer].append((x_pos, y_pos))  # append the locations
        columnPointer += 1
        if columnPointer > columnNum:  # check if the column pointer is still valid
            columnPointer = 0  # reset the column pointer
            firstLoop = False
    # print(matrix)
    return matrix  # return the constructed matrix
