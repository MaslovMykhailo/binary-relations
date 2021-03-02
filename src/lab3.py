from os import path

from parse import parseCriteria, parseLexicographicOrder, parseClassOrder
from render import renderBinaryMatrixes
from helpers import arrayToStr, increaseEach

from pareto import getParetoRelation
from majority import getMajorityRelation
from lexicographic import getLexicographicRelation
from berezovsky import getBerezovskyRelation
from padynovsky import getPadynoskyRelation

from optimization import dominationOptimization, blockingOptimization


baseFilePath = path.dirname(__file__)

def lab3():
    criteria = parseCriteria(
        baseFilePath + 
        '/../input/lab3/var18-criteria.txt'
    );
    lexicographicOrder = parseLexicographicOrder(
        baseFilePath + 
        '/../input/lab3/var18-lexicographic-order.txt'
    )
    classOrder = parseClassOrder(
        baseFilePath + 
        '/../input/lab3/var18-class-order.txt'
    )

    outputFilename = baseFilePath + '/../output/lab3/var18.txt'

    pareto = getParetoRelation(criteria)
    majority = getMajorityRelation(criteria)
    lexicographic = getLexicographicRelation(criteria, lexicographicOrder)
    berezovsky = getBerezovskyRelation(criteria, classOrder)
    padynosky = getPadynoskyRelation(criteria)

    matrixes = [pareto, majority, lexicographic, berezovsky, padynosky]

    renderBinaryMatrixes(matrixes, outputFilename)

    for index in range(len(matrixes)):
        matrix = matrixes[index]
        print('Relation: ' + str(index + 1))

        [greatestByP, greatestByR, stronglyGreatestByR] = map(increaseEach, dominationOptimization(matrix))

        print(arrayToStr(greatestByP, 'X*P = '))
        print(arrayToStr(greatestByR, 'X*R = '))
        print(arrayToStr(stronglyGreatestByR, 'X**R = '))

        [maxByP, maxByR, stronglyMaxByR] = map(increaseEach, blockingOptimization(matrix))

        print(arrayToStr(maxByP, 'X0P = '))
        print(arrayToStr(maxByR, 'X0R = '))
        print(arrayToStr(stronglyMaxByR, 'X00R = '))

lab3()
