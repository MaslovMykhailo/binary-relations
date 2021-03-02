def isAsymmetric(matrix):
    size = range(len(matrix))
    for i in size:
        for j in size:
            if matrix[i][j] == matrix[j][i] and matrix[i][j] == 1: 
                return False
    return True
    