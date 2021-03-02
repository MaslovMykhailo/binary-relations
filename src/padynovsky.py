from numpy import zeros
from pareto import getParetoRelation

def sortCriteria(criteria):
    sortedCriteria = []
    for c in criteria:
        sortedCriteria.append(
            sorted(c, reverse = True)
        )
    return sortedCriteria

def getPadynoskyRelation(criteria):
    return getParetoRelation(sortCriteria(criteria))
