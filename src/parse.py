def parseFile(filename): 
    matrixList = list()

    file = open(filename, 'r')

    for line in file:
        if '-' in line: 
            matrix = list();
            matrixList.append(matrix)
            continue

        line = list(map(int, line.split()))
        matrix.append(line)
    
    file.close()

    return matrixList

def parseCriteria(filename): 
    matrix = []

    file = open(filename, 'r')
    for line in file:
        line = list(map(int, line.split()))
        matrix.append(line)
    file.close()

    return matrix

def parseLexicographicOrder(filename):
    file = open(filename, 'r')
    line = file.readline()

    rawOrder = map(lambda p: p.split('k')[1], line.split('>'))
    order = map(lambda i: int(i) - 1, rawOrder)

    file.close()
    return order

def parseClassOrder(filename):
    file = open(filename, 'r')
    line = file.readline()

    rawOrder = map(lambda c: c[1:-1], line.split('<'))
    order = map(
        lambda c: map(
            lambda p: int(p.split('k')[1]) - 1,
            c.split(',')
        ), 
        rawOrder
    )

    file.close()
    return order
    