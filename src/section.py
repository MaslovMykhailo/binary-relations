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
    