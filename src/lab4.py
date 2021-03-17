from os import path
from numpy import zeros, setdiff1d as difference, intersect1d as intersection
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np

# Parse input utils

def parseCriteria(filename): 
    matrix = []

    file = open(filename, 'r')
    for line in file:
        line = list(map(int, line.split()))
        matrix.append(line)
    file.close()

    return matrix

def parseWeights(filename):
    file = open(filename, 'r')
    weights = list(map(int, file.readline().split()))
    file.close()
    return weights

def parseThreshold(filename):
    file = open(filename, 'r')
    [c, d] = map(float, file.readline().split())
    file.close()
    return c, d

# Write into file utils 

def writeIntArray(file, array): 
    file.write(' '.join(
        list(map(str, array))) + '\n'
    )

def writeInt2dArray(file, array2d): 
    for array in array2d:
        writeIntArray(file, array)

def writeFloatArray(file, array):
    file.write(' '.join(
        list(map(lambda n : '%.3f' % n, array))) + '\n'
    )

def writeFloat2dArray(file, array2d): 
    for array in array2d:
        writeFloatArray(file, array)

# Neumann Morgenstern optimization

def getTopSection(matrix, index):
    section = list()
    for i in range(len(matrix)):
        if matrix[i][index] == 1: section.append(i)
    return section

def getBottomSection(matrix, index): 
    section = list()
    for i in range(len(matrix[index])):
        if matrix[index][i] == 1: section.append(i)
    return section

def hasCycle(matrix, targetElement, currentElement, checked = []):
    section = getBottomSection(matrix, currentElement)
    if targetElement in section: 
        return True
    else:
        for sectionElement in section:
            if sectionElement in checked:
                continue
            if hasCycle(matrix, targetElement, sectionElement, checked + [currentElement]):
                return True
    return False

def isAcyclic(matrix):
    for index in range(len(matrix)):
        if hasCycle(matrix, index, index):
            return False
    return True

def calcNeumannMorgenstern(matrix):
    if not isAcyclic(matrix):
        return []

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

# ELECTRE I

def concordance(criteria, weights):
    criteriaCount = len(weights) 
    totalWeight = sum(weights)

    size = len(criteria)
    matrix = zeros(shape = (size, size), dtype = float)

    for i in range(size):
        for j in range(size):
            if i == j:
                matrix[i][j] = 0
                continue

            greaterCriteriaWeight = sum(list(map(
                lambda c : weights[c] if criteria[i][c] >= criteria[j][c] else 0,
                range(criteriaCount)
            )))

            matrix[i][j] = greaterCriteriaWeight / totalWeight

    return matrix

def calcCriteriaDistance(criteria, index):
    indexCriteria = list(map(lambda c : c[index], criteria));
    return max(indexCriteria) - min(indexCriteria)

def discordance(criteria, weights): 
    criteriaCount = len(weights) 

    size = len(criteria)
    matrix = zeros(shape = (size, size), dtype = float)

    for i in range(size):
        for j in range(size):
            if i == j: 
                matrix[i][j] = 1 
                continue

            greater = reduce(
                lambda c, n : c and criteria[i][n] >= criteria[j][n],
                range(criteriaCount),
                True
            )

            if greater:
                matrix[i][j] = 0
                continue

            maxCriteriaDifference = max(list(map(
                lambda c : (weights[c] * (criteria[j][c] - criteria[i][c])) if criteria[i][c] < criteria[j][c] else 0,
                range(criteriaCount)
            ))) 
            maxDifference = max(list(map(
                lambda c : (weights[c] * calcCriteriaDistance(criteria, c)) if criteria[i][c] < criteria[j][c] else 0,
                range(criteriaCount)
            )))

            matrix[i][j] = maxCriteriaDifference / maxDifference

    return matrix

def toBinaryRelation(c, concordanceMatrix, d, discordanceMatrix):
    size = max(len(concordanceMatrix), len(discordanceMatrix))
    binaryRelation = zeros(shape = (size, size), dtype = int)

    for i in range(size):
        for j in range(size):
            if concordanceMatrix[i][j] >= c and discordanceMatrix[i][j] <= d:
                binaryRelation[i][j] = 1

    return binaryRelation

def electre1(criteria, weights, c, d):
    cMatrix = concordance(criteria, weights)
    dMatrix = discordance(criteria, weights)

    relation = toBinaryRelation(
        c, cMatrix,
        d, dMatrix
    )

    core = calcNeumannMorgenstern(relation)
    return core, relation, cMatrix, dMatrix

# Analyzation

def analyzeConcordanceThresholdChange(criteria, weights, discordanceThreshold, filename = None):
    fig, axs = plt.subplots()

    xrange = np.arange(start = 0.55, stop = 1, step = 0.05)
    yrange = list(map(lambda x : len(electre1(criteria, weights, x, discordanceThreshold)[0]), xrange))

    axs.plot(xrange, yrange)

    axs.set_xlabel('Поріг узгодження (c)')
    axs.set_ylabel('Розмір ядра')

    axs.set_title('Поріг неузгодження постійного значення (d = ' + str(discordanceThreshold) + ')')

    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def analyzeDiscordanceThresholdChange(criteria, weights, concordanceThreshold, filename = None):
    fig, axs = plt.subplots()

    xrange = np.arange(start = 0.05, stop = 0.5, step = 0.05)
    yrange = list(map(lambda x : len(electre1(criteria, weights, concordanceThreshold, x)[0]), xrange))

    axs.plot(xrange, yrange)

    axs.set_xlabel('Поріг неузгодження (d)')
    axs.set_ylabel('Розмір ядра')

    axs.set_title('Поріг узгодження постійного значення (c = ' + str(concordanceThreshold) + ')')

    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def analyzeThresholdsChange(criteria, weights, filename = None):
    fig, axs = plt.subplots()

    xrange = np.arange(start = 0.05, stop = 0.5, step = 0.05)
    yrange = list(map(lambda x : len(electre1(criteria, weights, 1 - x, x)[0]), xrange))

    axs.plot(xrange, yrange)

    axs.set_xlabel('Зміна порогу (с є [0.5, 1] | d є [0, 0.5])')
    axs.set_ylabel('Розмір ядра')

    axs.set_title('Одночасна зміна порогів узгодження і неузгодження')

    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def sumOfPrev(array2d, index):
    prevSum = []
    for i in range(len(array2d[0])):
        acc = 0
        for j in range(index):
            acc += array2d[j][i]
        prevSum.append(acc)
    return prevSum

def analyzeCoreConcordanceChange(criteria, weights, d, filename = None):
    fig, axs = plt.subplots()

    xrange = np.arange(start = 0.6, stop = 1, step = 0.1)

    cores = []
    for index in range(len(criteria)):
        core = list(map(lambda x : 1 if index in electre1(criteria, weights, x, d)[0] else 0, xrange))
        cores.append(core)

    for index in range(len(cores)):
        axs.bar(xrange, cores[index], 0.05, bottom = sumOfPrev(cores, index), label = str(index + 1))

    axs.set_xlabel('Поріг узгодження (c)')
    axs.set_ylabel('Склад ядра')

    axs.set_title('Поріг неузгодження постійного значення (d = ' + str(d) + ')')
    axs.legend(bbox_to_anchor = (0.975, 0.975))

    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def analyzeCoreDiscordanceChange(criteria, weights, c, filename = None):
    fig, axs = plt.subplots()

    xrange = np.arange(start = 0.1, stop = 0.5, step = 0.1)

    cores = []
    for index in range(len(criteria)):
        core = list(map(lambda x : 1 if index in electre1(criteria, weights, c, x)[0] else 0, xrange))
        cores.append(core)

    for index in range(len(cores)):
        axs.bar(xrange, cores[index], 0.05, bottom = sumOfPrev(cores, index), label = str(index + 1))

    axs.set_xlabel('Поріг неузгодження (d)')
    axs.set_ylabel('Склад ядра')

    axs.set_title('Поріг узгодження постійного значення (c = ' + str(c) + ')')
    axs.legend(bbox_to_anchor = (0.975, 0.975))

    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def analyzeCoreChange(criteria, weights, filename = None):
    fig, axs = plt.subplots()

    xrange = np.arange(start = 0.1, stop = 0.6, step = 0.1)

    cores = []
    for index in range(len(criteria)):
        core = list(map(lambda x : 1 if index in electre1(criteria, weights, 1 - x, x)[0] else 0, xrange))
        cores.append(core)

    for index in range(len(cores)):
        axs.bar(xrange, cores[index], 0.05, bottom = sumOfPrev(cores, index), label = str(index + 1))

    axs.set_xlabel('Зміна порогу (с є [0.5, 1] | d є [0, 0.5])')
    axs.set_ylabel('Склад ядра')

    axs.set_title('Одночасна зміна порогів узгодження і неузгодження')
    axs.legend(bbox_to_anchor = (0.975, 0.975))

    if filename:
        plt.savefig(filename)
    else:
        plt.show()

# Write solution into file

def writeSolution(filename, c, cm, d, dm, br, core):
    file = open(filename, 'w+')

    file.write('матриця індексів узгодження C\n')
    writeFloat2dArray(file, cm)

    file.write('матриця індексів неузгодження D\n')
    writeFloat2dArray(file, dm)

    file.write('Значення порогів для індексів узгодження та неузгодження c, d\n')
    writeFloatArray(file, [c, d])

    file.write('Відношення для порогових значень c, d:\n')
    writeInt2dArray(file, br)

    file.write('Ядро відношення:\n')
    writeIntArray(file, core)

    file.close();

# Solution 

def lab4(): 
    baseFilePath = path.dirname(__file__)

    criteria = parseCriteria(
        baseFilePath + 
        '/../input/lab4/var18-criteria.txt'
    );

    weights = parseWeights(
        baseFilePath + 
        '/../input/lab4/var18-weight.txt'
    );

    c, d = parseThreshold(
        baseFilePath + 
        '/../input/lab4/var18-threshold.txt'
    )

    core, relation, cm, dm = electre1(criteria, weights, c, d)
    core = list(map(lambda n : n + 1, core))

    outputFilename = baseFilePath + '/../output/lab4/var18.txt'
    writeSolution(
        outputFilename, 
        c, cm, 
        d, dm, 
        relation, 
        core
    )

    cChangeFilename = baseFilePath + '/../output/lab4/var18-c-change.png'
    analyzeConcordanceThresholdChange(criteria, weights, 0.49, cChangeFilename)
    cCoreChangeFilename = baseFilePath + '/../output/lab4/var18-c-core-change.png'
    analyzeCoreConcordanceChange(criteria, weights, 0.49, cCoreChangeFilename)

    dChangeFilename = baseFilePath + '/../output/lab4/var18-d-change.png'
    analyzeDiscordanceThresholdChange(criteria, weights, 0.5, dChangeFilename)
    dCoreChangeFilename = baseFilePath + '/../output/lab4/var18-d-core-change.png'
    analyzeCoreDiscordanceChange(criteria, weights, 0.5, dCoreChangeFilename)

    cdChangeFilename = baseFilePath + '/../output/lab4/var18-cd-change.png'
    analyzeThresholdsChange(criteria, weights, cdChangeFilename)
    cdCoreChangeFilename = baseFilePath + '/../output/lab4/var18-cd-core-change.png'
    analyzeCoreChange(criteria, weights, cdCoreChangeFilename)
    
lab4()
