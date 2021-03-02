from numpy import zeros
from sigma import buildSigmaMatrix

def lexicographicCondition(sigma, order): 
    for index in order:
        if sigma[index] == 1:
            return True
        elif sigma[index] != 0:
            return False
    return False

def getLexicographicRelation(criteria, order):
    size = len(criteria)
    sigma = buildSigmaMatrix(criteria)

    lexicographic = zeros(shape = (size, size), dtype = int)

    for i in range(size):
        for j in range(size):
            if lexicographicCondition(sigma[i][j], order):
                lexicographic[i][j] = 1

    return lexicographic
    