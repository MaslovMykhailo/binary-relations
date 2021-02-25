from asymmetric import isAsymmetric
from section import getTopSection, getBottomSection

# Domination optimization utilities

def findGreatestByP(matrix):
    greatestByP = list()
    size = len(matrix)
    for index in range(size):
        bottomSection = getBottomSection(matrix, index)
        if len(bottomSection) == size - 1 and index not in bottomSection:
            greatestByP.append(index)
    return greatestByP

def findGreatestByR(matrix):
    greatestByR = list()
    size = len(matrix)
    for index in range(size):
        bottomSection = getBottomSection(matrix, index)
        if len(bottomSection) == size:
            greatestByR.append(index)
    return greatestByR

def findStronglyGreatestByR(matrix):
    stronglyGreatestByR = list()
    size = len(matrix)
    for index in range(size):
        bottomSection = getBottomSection(matrix, index)
        if len(bottomSection) == size:
            topSection = getTopSection(matrix, index)
            if len(topSection) == 1 and index in topSection:
                stronglyGreatestByR.append(index)
    return stronglyGreatestByR

# Domination optimization algorythm

def dominationOptimization(matrix):
    if isAsymmetric(matrix):
        return [
            findGreatestByP(matrix),
            [],
            []
        ]
    else:
        return [
            [], 
            findGreatestByR(matrix),
            findStronglyGreatestByR(matrix)
        ]

# Blocking optimization utilities

def findMaxByP(matrix):
    maxByP = list()
    for index in range(len(matrix)):
        topSection = getTopSection(matrix, index)
        if len(topSection) == 0:
            maxByP.append(index)
    return maxByP

def findMaxByR(matrix):
    maxByR = list()

    for index in range(len(matrix)):
        bottomContainsTop = True

        topSection = getTopSection(matrix, index)
        bottomSection = getBottomSection(matrix, index)

        if len(topSection) > len(bottomSection):
            continue

        for topItem in topSection:
            if topItem not in bottomSection:
                bottomContainsTop = False
                break;

        if bottomContainsTop:
            maxByR.append(index)

    return maxByR;

def findStronglyMaxByR(matrix):
    stronglyMaxByR = list()
    for index in range(len(matrix)):
        topSection = getTopSection(matrix, index)
        if len(topSection) == 0 or (len(topSection) == 1 and index in topSection):
            stronglyMaxByR.append(index)
    return stronglyMaxByR

# Blocking optimization algorythm

def blockingOptimization(matrix):
    if isAsymmetric(matrix):
        return [
            findMaxByP(matrix),
            [],
            []
        ]
    else:
        return [
            [], 
            findMaxByR(matrix),
            findStronglyMaxByR(matrix)
        ]
