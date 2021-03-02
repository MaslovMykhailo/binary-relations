from numpy import zeros
from functools import reduce
from sigma import buildSigmaMatrix

def paretoCondition(sigma):
    return reduce(lambda c, n: c and n >= 0, sigma, True)

def getParetoRelation(criteria):
    size = len(criteria)
    sigma = buildSigmaMatrix(criteria)

    pareto = zeros(shape = (size, size), dtype = int)

    for i in range(size):
        for j in range(size):
            if paretoCondition(sigma[i][j]):
                pareto[i][j] = 1

    return pareto
