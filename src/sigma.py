from numpy import zeros

def getSigmaSign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0

def buildSigmaMatrix(criteria):
    size = len(criteria)
    criteriaCount = len(criteria[0])

    sigma = zeros(shape = (size, size, criteriaCount), dtype = int)
    for c in range(criteriaCount):
        for i in range(size):
            for j in range(size):
                sigma[i][j][c] = getSigmaSign(
                    criteria[i][c] - criteria[j][c]
                )

    return sigma

def buildSigmaByClass(criteriaClass, cI, cJ):
    return map(lambda c : getSigmaSign(cI[c] - cJ[c]), criteriaClass)
    