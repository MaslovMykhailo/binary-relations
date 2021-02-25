from numpy import setdiff1d as difference, intersect1d as intersection
from section import getTopSection

def optimizationNeumannMorgenstern(matrix):
    omega = range(len(matrix))
    
    sArray = [[]]

    for item in omega:
        if len(getTopSection(matrix, item)) == 0:
            sArray[0].append(item)

    while len(sArray[len(sArray) - 1]) < len(omega):
        s = [] 
        prevS = sArray[len(sArray) - 1]

        for item in difference(omega, prevS):
            topSection = getTopSection(matrix, item)
            if len(intersection(topSection, prevS)) == len(topSection):
                s.append(item)

        sArray.append(prevS + s)

    qArray = [sArray[0]]
    for step in range(1, len(sArray)):
        q = []
        prevQ = qArray[step - 1]
        for item in difference(sArray[step], sArray[step - 1]):
            topSection = getTopSection(matrix, item)
            if len(intersection(topSection, prevQ)) == 0:
                q.append(item)
            
        qArray.append(prevQ + q)
    
    return qArray[len(qArray) - 1]
