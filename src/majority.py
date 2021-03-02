from numpy import zeros
from functools import reduce
from sigma import buildSigmaMatrix

def majorityCondition(sigma):
    return reduce(lambda sum, n: sum + n, sigma, 0) > 0

def getMajorityRelation(criteria):
    size = len(criteria)
    sigma = buildSigmaMatrix(criteria)

    majority = zeros(shape = (size, size), dtype = int)

    for i in range(size):
        for j in range(size):
            if majorityCondition(sigma[i][j]):
                majority[i][j] = 1

    return majority
    