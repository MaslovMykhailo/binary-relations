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
    