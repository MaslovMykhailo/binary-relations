from numpy import zeros, intersect1d as intersection
from ipn import toIPN
from section import getBottomSection

kFamily = {
    '1': ['P', 'I', 'N'],
    '2': ['P', 'N'],
    '3': ['P', 'I'],
    '4': ['P']
}

def buildKFamilyMatrix(ipnMatrix, family):
    size = len(ipnMatrix);
    kFamilyMatrix = zeros(shape = (size, size), dtype=int)

    for i in range(size):
        for j in range(size):
            if ipnMatrix[i][j] in kFamily[family]:
                kFamilyMatrix[i][j] = 1
    
    return kFamilyMatrix

def findMaxAndOptimal(matrix):
    omega = range(len(matrix));
    sections = []

    for item in omega:
        sections.append(getBottomSection(matrix, item))

    max = []
    optimal = []

    for item in omega:
        if len(intersection(sections[item], omega)) == len(omega):
            max.append(item)
            optimal.append(item)
            continue

        containsAll = True

        for section in sections:
            if len(intersection(section, sections[item])) < len(section):
                containsAll = False

        if containsAll: 
            max.append(item)
    
    return [max, optimal]
        

def optimizationK(matrix):
    ipn = toIPN(matrix)
    kFamilyOptimization = {}
    for family in kFamily.keys():
        kFamilyOptimization[family] = findMaxAndOptimal(
            buildKFamilyMatrix(ipn, family)
        )
    return kFamilyOptimization  
