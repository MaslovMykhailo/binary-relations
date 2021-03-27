from os import path
from numpy import zeros
from graphviz import Digraph

# Parse input file

def parseInputRelations(filename):
    relations = list()

    file = open(filename, 'r')
    
    for line in file:
        if 'R' in line:
            relations.append(list())
            continue

        values = list(map(lambda n : float(n.replace(',', '.')), line.split()))
        relations[len(relations) - 1].append(values)

    return relations

# Render relation

def renderRelation(relation, filename): 
    digraph = Digraph(filename)

    for item in range(len(relation)):
        digraph.node(str(item + 1))

    for i in range(len(relation)):
        for j in range(len(relation[i])):
            if relation[i][j] > 0:
                digraph.edge(str(i + 1), str(j + 1), label = str(relation[i][j]))

    digraph.render(filename)

def writeFloatArray(file, array):
    file.write(' '.join(
        list(map(lambda n : '%.1f' % n, array))) + '\n'
    )

def writeFloat2dArray(file, array2d): 
    for array in array2d:
        writeFloatArray(file, array)

# Operations

def disjunction(r1, r2):
    size = min(len(r1), len(r2))
    r = zeros(shape = (size, size), dtype = float)
    for i in range(size):
        for j in range(size):
            r[i][j] = max(r1[i][j], r2[i][j])
    return r

def conjunction(r1, r2):
    size = min(len(r1), len(r2))
    r = zeros(shape = (size, size), dtype = float)
    for i in range(size):
        for j in range(size):
            r[i][j] = min(r1[i][j], r2[i][j])
    return r

def negation(r):
    size = len(r)
    n = zeros(shape = (size, size), dtype = float)
    for i in range(size):
        for j in range(size):
            n[i][j] = 1 - r[i][j]
    return n

def advantage(r):
    size = len(r)
    c = zeros(shape = (size, size), dtype = float)
    for i in range(size):
        for j in range(size):
            c[i][j] = max(r[i][j] - r[j][i], 0)
    return c

def including(r1, r2):
    size = min(len(r1), len(r2))
    n = zeros(shape = (size, size), dtype = float)
    for i in range(size):
        for j in range(size):
            if r1[i][j] < r2[i][j]:
                return False;
    return True

def composition(r1, r2):
    h = len(r2)
    w = len(r1[0])

    r = zeros(shape = (h, w), dtype = float)
    for i in range(h):
        for j in range(w):
            r[i][j] = max(list(map(lambda n : min(n, r1[j][i]), r2[i])))
    return r

def alphaLevel(r, alpha):
    size = len(r)
    a = zeros(shape = (size, size), dtype = float)
    for i in range(size):
        for j in range(size):
            a[i][j] = 1 if r[i][j] >= alpha else 0
    return a

# Properties

def isReflexive(relation):
    size = len(relation)
    for i in range(size):
        if relation[i][i] != 1:
            return False
    return True

def isStrongReflexive(relation):
    if not isReflexive(relation):
        return False;
    
    size = len(relation)
    for i in range(size):
        for j in range(size):
            if i == j: 
                continue
            if relation[i][j] == 1:
                return False
    return True

def isWeakReflexive(relation):
    return isReflexive(relation) and not isStrongReflexive(relation)

def isAntireflexive(relation):
    size = len(relation)
    for i in range(size):
        if relation[i][i] != 0:
            return False
    return True

def isStrongAntireflexive(relation):
    if not isAntireflexive(relation):
        return False;
    
    size = len(relation)
    for i in range(size):
        for j in range(size):
            if i == j: 
                continue
            if relation[i][j] == 0:
                return False
    return True

def isWeakAntireflexive(relation):
    return isAntireflexive(relation) and not isStrongAntireflexive(relation)

def isSymmetric(relation):
    size = len(relation)
    for i in range(size):
        for j in range(size):
            if relation[i][j] != relation[j][i]:
                return False
    return True

def isAntisymmetric(relation):
    size = len(relation)
    for i in range(size):
        for j in range(size):
            if relation[i][j] == relation[j][i] and i != j:
                return False
    return True

def isAsymmetric(relation):
    size = len(relation)
    for i in range(size):
        for j in range(size):
            if relation[i][j] == relation[j][i]:
                return False
    return True

def isStrongConnective(relation):
    size = len(relation)
    for i in range(size):
        for j in range(size):
            if relation[i][j] != 1 and relation[j][i] != 1:
                return False
    return True

def isWeakConnective(relation):
    size = len(relation)
    for i in range(size):
        for j in range(size):
            if relation[i][j] == 0 and relation[j][i] == 0:
                return False
    return True

def isConnective(relation):
    return isWeakConnective(relation) or isStrongConnective(relation)

def isTransitive(relation):
    return including(relation, composition(relation, relation))

# Rational evaluation

def rationalEvaluation(relation):
    advantageRelation = advantage(relation)
    maxAlternatives = list(map(
        lambda i : max(list(map(lambda line : line[i], advantageRelation))), 
        range(len(relation[0]))
    ))
    reversedMaxAlternatives = list(map(
        lambda n : 1 - n,
        maxAlternatives
    ))

    return advantageRelation, maxAlternatives, reversedMaxAlternatives

# Solution

def lab6():
    baseFilePath = path.dirname(__file__)

    inputFilename = baseFilePath + '/../input/lab6/var18.txt';
    outputFilename = baseFilePath + '/../output/lab6/var18.txt';

    [r1, r2] = parseInputRelations(inputFilename)

    file = open(outputFilename, 'w+')

    file.write('R1 properties\n')

    file.write('Reflexive: ' + str(isReflexive(r1)) + '\n')
    file.write('Strong reflexive: ' + str(isStrongReflexive(r1)) + '\n')
    file.write('Weak reflexive: ' + str(isWeakReflexive(r1)) + '\n')

    file.write('Antireflexive: ' + str(isAntireflexive(r1)) + '\n')
    file.write('Strong antireflexive: ' + str(isStrongAntireflexive(r1)) + '\n')
    file.write('Weak antireflexive: ' + str(isWeakAntireflexive(r1)) + '\n')

    file.write('Symmetric: ' + str(isSymmetric(r1)) + '\n')
    file.write('Asymmetric: ' + str(isAsymmetric(r1)) + '\n')
    file.write('Antisymmetric: ' + str(isAntisymmetric(r1)) + '\n')

    file.write('Connective: ' + str(isConnective(r1)) + '\n')
    file.write('Transitive: ' + str(isTransitive(r1)) + '\n')

    file.write('\n')

    file.write('R1 R2 disjunction \n')
    writeFloat2dArray(file, disjunction(r1, r2));  
    
    file.write('R1 R2 conjunction \n')
    writeFloat2dArray(file, conjunction(r1, r2));  

    file.write('R1 R2 composition \n')
    writeFloat2dArray(file, composition(r1, r2));  

    file.write('R2 R1 composition \n')
    writeFloat2dArray(file, composition(r2, r1));  

    file.write('R1 negation \n')
    writeFloat2dArray(file, negation(r1));  

    file.write('R1 alpha level 0.5 \n')
    writeFloat2dArray(file, alphaLevel(r1, 0.5));  

    file.write('R1 advantage \n')
    writeFloat2dArray(file, advantage(r1));  

    file.write('\n')

    file.write('R1 rational evaluation \n')
    ar, maxAlternatives, reversedMaxAlternatives = rationalEvaluation(r1)

    file.write('R1 max alternatives \n')
    writeFloatArray(file, maxAlternatives);

    file.write('R1 reversed max alternatives \n')
    writeFloatArray(file, reversedMaxAlternatives);

    file.close()

    renderRelation(r1, baseFilePath + '/../output/lab6/var18-relation-r1.gv')
    renderRelation(r2, baseFilePath + '/../output/lab6/var18-relation-r2.gv')

lab6()
