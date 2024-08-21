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