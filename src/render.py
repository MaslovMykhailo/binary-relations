from graphviz import Digraph

def renderGraph(matrix, filename): 
    digraph = Digraph(filename)

    for item in range(len(matrix)):
        digraph.node(str(item + 1))

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                digraph.edge(str(i + 1), str(j + 1))

    digraph.render(filename)

def renderMatrix(matrix, filename):
    file = open(filename, 'w+')
    file.write('|---' * len(matrix) + '|\n')
    for line in matrix:
        file.write('| ' + ' | '.join(line) + ' |\n'); 
        file.write('|---' * len(line) + '|\n')
    file.close()
