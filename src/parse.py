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