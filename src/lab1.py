from parse import parseFile
from acyclic import isAcyclic
from render import renderGraph, renderMatrix
from ipn import toIPN
from os import path

baseFilePath = path.dirname(__file__)

def lab1():
    matrixList = parseFile(baseFilePath + '/../input/lab1/var18.txt')

    for matrix in matrixList:
        index = matrixList.index(matrix) + 1
        outDir = baseFilePath + '/../output/lab1/matrix-' + str(index) + '/'

        renderGraph(matrix, outDir + 'graph.gv')
        renderMatrix(toIPN(matrix), outDir + 'ipn.txt')

        print('Matrix #' + str(index))
        print('Acyclic: ' + str(isAcyclic(matrix)))

lab1()
            