from numpy import zeros
from functools import reduce
from sigma import buildSigmaByClass

def getParetoCustomRelation(criteria, criteriaClass, condition):
    size = len(criteria)
    pareto = zeros(shape = (size, size), dtype = int)

    for i in range(size):
        for j in range(size):
            sigma = buildSigmaByClass(criteriaClass, criteria[i], criteria[j])
            if condition(sigma):
                pareto[i][j] = 1

    return pareto


def paretoPCondition(sigma):
    return 1 in sigma and -1 not in sigma

def getParetoPRelation(criteria, criteriaClass):
    return getParetoCustomRelation(criteria, criteriaClass, paretoPCondition)


def paretoICondition(sigma):
    return reduce(lambda c, s : c and s == 0, sigma, True)

def getParetoIRelation(criteria, criteriaClass):
    return getParetoCustomRelation(criteria, criteriaClass, paretoICondition)


def paretoNCondition(sigma):
    return 1 in sigma and -1 in sigma

def getParetoNRelation(criteria, criteriaClass):
    return getParetoCustomRelation(criteria, criteriaClass, paretoNCondition)


def getParetoIPNRelation(criteria, criteriaClass):
    return {
        'I': getParetoIRelation(criteria, criteriaClass),
        'P': getParetoPRelation(criteria, criteriaClass),
        'N': getParetoNRelation(criteria, criteriaClass)
    }

def getBerezovskyRelation(criteria, classes):
    size = len(criteria)

    bRelations = [getParetoIPNRelation(criteria, classes[0])]

    for c in range(1, len(classes)):
        paretoIPN = getParetoIPNRelation(criteria, classes[c])

        bRelations.append({
            'I': zeros(shape = (size, size), dtype = int),
            'P': zeros(shape = (size, size), dtype = int),
            'N': zeros(shape = (size, size), dtype = int)
        })

        for i in range(size):
            for j in range(size):

                if (
                    paretoIPN['P'][i][j] == 1 and 
                    bRelations[c - 1]['P'][j][i] == 0
                ) or (
                    paretoIPN['I'][i][j] == 1 and
                    bRelations[c - 1]['P'][i][j] == 1
                ):
                    bRelations[c]['P'][i][j] = 1

                if (
                    paretoIPN['I'][i][j] == 1 and
                    bRelations[c - 1]['I'][i][j] == 1
                ): 
                    bRelations[c]['I'][i][j] = 1

        for i in range(size):
            for j in range(size):

                if not (
                    bRelations[c]['P'][i][j] == 1 or
                    bRelations[c]['P'][j][i] == 1 or
                    bRelations[c]['I'][i][j] == 1
                ): 
                    bRelations[c]['N'][i][j] = 1

    return bRelations[len(bRelations) - 1]['P']
    