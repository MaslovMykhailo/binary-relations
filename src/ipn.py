from numpy import zeros

def toIPN(matrix):
    ipnMatrix = []
    for i in range(len(matrix)):
        ipnMatrix.append([None] * len(matrix))
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                if matrix[i][j] == matrix[j][i]:
                    ipnMatrix[i][j] = 'I'
                else: 
                    ipnMatrix[i][j] = 'P'
            else:
                if matrix[i][j] == matrix[j][i]:
                    ipnMatrix[i][j] = 'N'
                else:
                    ipnMatrix[i][j] = ' '
    return ipnMatrix
    
def IPNRelationToBinary(ipn): 
    size = max([len(ipn['I']), len(ipn['P']), len(ipn['N'])])
    matrix = zeros(shape = (size, size), dtype = int)

    for i in range(size):
        for j in range(size):
            if (ipn['I'][i][j] == 1 or ipn['P'][i][j] == 1):
                matrix[i][j] = 1
            if (ipn['N'][i][j] == 1):
                matrix[i][j] = 0
    
    return matrix
    