from parse import parseFile
from render import renderGraph, renderMatrix

from optimization import dominationOptimization, blockingOptimization
from neumann_morgenstern import optimizationNeumannMorgenstern
from k_optimization import optimizationK

from acyclic import isAcyclic
from ipn import toIPN

from helpers import increase, increaseEach, arrayToStr
from os import path


baseFilePath = path.dirname(__file__)

def task1():
    matrixList = parseFile(baseFilePath + '/../input/lab1/var18.txt')

    outputFilename = baseFilePath + '/../output/lab2/task1var18.txt'
    outputFile = open(outputFilename, 'w+')

    for matrix in matrixList:
        outputFile.write('\nR' + str(matrixList.index(matrix) + 1) + ':\n')

        [greatestByP, greatestByR, stronglyGreatestByR] = map(increaseEach, dominationOptimization(matrix))

        outputFile.write(arrayToStr(greatestByP, 'X*P = ', '\n'))
        outputFile.write(arrayToStr(greatestByR, 'X*R = ', '\n'))
        outputFile.write(arrayToStr(stronglyGreatestByR, 'X**R = ', '\n'))

        [maxByP, maxByR, stronglyMaxByR] = map(increaseEach, blockingOptimization(matrix))

        outputFile.write(arrayToStr(maxByP, 'X0P = ', '\n'))
        outputFile.write(arrayToStr(maxByR, 'X0R = ', '\n'))
        outputFile.write(arrayToStr(stronglyMaxByR, 'X00R = ', '\n'))

    outputFile.close()

def task2():
    matrixList = parseFile(baseFilePath + '/../input/lab2/var18.txt')

    outputFilename = baseFilePath + '/../output/lab2/task2var18.txt'
    outputFile = open(outputFilename, 'w+')

    for matrix in matrixList:
        index = matrixList.index(matrix) + 1

        outDir = baseFilePath + '/../output/lab2/matrix-' + str(index) + '/'
        renderGraph(matrix, outDir + 'graph.gv')
        renderMatrix(toIPN(matrix), outDir + 'ipn.txt')

        outputFile.write('\nR' + str(index) + ':\n')

        if isAcyclic(matrix):    
            optimization = map(increase, optimizationNeumannMorgenstern(matrix))
            outputFile.write(arrayToStr(optimization, 'HM = ', '\n')) 
        else:
            kOptimization = optimizationK(matrix)
            for family, results in kOptimization.items():
                [max, opt] = map(increaseEach, results)
                outputFile.write(arrayToStr(max, 'max-' + family + ' = ', '\n'))
                outputFile.write(arrayToStr(opt, 'opt-' + family + ' = ', '\n\n')) 

    outputFile.close()
    
def lab2():
    task2()
    task1()

lab2()
