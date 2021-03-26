from os import path
from numpy import zeros, arange

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

# Write output

def writeFloatArray(file, array):
    file.write(' '.join(
        list(map(lambda n : '%.3f' % n, array))) + '\n'
    )


# Weights normalization 

def normalizeWeights(weights): 
    totalWeight = sum(weights)
    return list(map(lambda w : w / totalWeight, weights));

# Criteria normalization 

def geometricAverage(numbers):
    return sum(list(map(lambda n : n * n, numbers))) ** (1 / 2)

def normalizeCriteriaForTopsis(criteria):
    alternativesCount = len(criteria)
    criteriaCount = len(criteria[0])

    gms = list()
    for i in range(criteriaCount):
        cs = list(map(lambda c : c[i], criteria))
        gms.append(geometricAverage(cs))

    normalizedCriteria = zeros(shape = (alternativesCount, criteriaCount), dtype = float)
    for i in range(alternativesCount):
        for j in range(len(criteria[i])):
            normalizedCriteria[i][j] = criteria[i][j] / gms[j]
    
    return normalizedCriteria

def normalizeCriteriaForCriterialTopsis(criteria, benefits, costs):
    alternativesCount = len(criteria)
    criteriaCount = len(criteria[0])

    maxs = list()
    mins = list()

    for i in range(criteriaCount):
        cs = list(map(lambda c : c[i], criteria))
        maxs.append(max(cs))
        mins.append(min(cs))

    normalizedCriteria = zeros(shape = (alternativesCount, criteriaCount), dtype = float)

    for i in range(alternativesCount):
        for j in benefits:
            normalizedCriteria[i][j] = (criteria[i][j] - mins[j]) / (maxs[j] - mins[j])

    for i in range(alternativesCount):
        for j in costs:
            normalizedCriteria[i][j] = (maxs[j] - criteria[i][j]) / (maxs[j] - mins[j])

    return normalizedCriteria

def normalizeCriteriaForVikor(criteria):
    alternativesCount = len(criteria)
    criteriaCount = len(criteria[0])

    maxs = list()
    mins = list()

    for i in range(criteriaCount):
        cs = list(map(lambda c : c[i], criteria))
        maxs.append(max(cs))
        mins.append(min(cs))

    normalizedCriteria = zeros(shape = (alternativesCount, criteriaCount), dtype = float)
    for i in range(alternativesCount):
        for j in range(criteriaCount):
            normalizedCriteria[i][j] = abs(maxs[j] - criteria[i][j]) / abs(maxs[j] - mins[j])

    return normalizedCriteria

def weightNormalizedCriteria(criteria, weights):
    alternativesCount = len(criteria)
    criteriaCount = len(criteria[0])

    weightnedCriteria = zeros(shape = (alternativesCount, criteriaCount), dtype = float)
    for i in range(alternativesCount):
        for j in range(len(criteria[i])):
            weightnedCriteria[i][j] = criteria[i][j] * weights[j]

    return weightnedCriteria

# Determine PIS

def findPis(weightnedCriteria):
    criteriaCount = len(weightnedCriteria[0])

    pis = list()
    for i in range(criteriaCount):
        localPis = max(list(map(lambda c : c[i], weightnedCriteria)))
        pis.append(localPis)

    return pis

def findCriterialPis(weightnedCriteria, benefits, costs):
    criteriaCount = len(weightnedCriteria[0])

    pis = zeros(shape = (criteriaCount), dtype = float)
    for i in range(len(pis)):
        current = list(map(lambda c : c[i], weightnedCriteria))
        if i in benefits:
            pis[i] = max(current)
        if i in costs:
            pis[i] = min(current)

    return pis

# Determine NIS

def findNis(weightnedCriteria):
    criteriaCount = len(weightnedCriteria[0])

    nis = list()
    for i in range(criteriaCount):
        localNis = min(list(map(lambda c : c[i], weightnedCriteria)))
        nis.append(localNis)

    return nis

def findCriterialNis(weightnedCriteria, benefits, costs):
    criteriaCount = len(weightnedCriteria[0])

    nis = zeros(shape = (criteriaCount), dtype = float)
    for i in range(len(nis)):
        current = list(map(lambda c : c[i], weightnedCriteria))
        if i in benefits:
            nis[i] = min(current)
        if i in costs:
            nis[i] = max(current)

    return nis

# Calculate length betwee current criteria and ideal points

def calcLength(weightnedCriteria, pis, nis):
    alternativesCount = len(weightnedCriteria)
    criteriaCount = len(weightnedCriteria[0])

    lengths = list()

    for i in range(alternativesCount):
        dPs = list()
        dNs = list()

        for j in range(criteriaCount):
            dPs.append(abs(pis[j] - weightnedCriteria[i][j]) ** 2)
            dNs.append(abs(nis[j] - weightnedCriteria[i][j]) ** 2)

        dP = sum(dPs) ** (1 / 2)
        dN = sum(dNs) ** (1 / 2)

        lengths.append(dN / (dP + dN))

    return lengths

# Calculate intervals for VIKOR

def calcIntervalsForVikor(weightnedCriteria, v):
    alternativesCount = len(weightnedCriteria)

    S = zeros(shape = (alternativesCount), dtype = float)
    R = zeros(shape = (alternativesCount), dtype = float)

    for i in range(alternativesCount):
        S[i] = sum(weightnedCriteria[i])
        R[i] = max(weightnedCriteria[i])

    minS = min(S)
    maxS = max(S)

    minR = min(R)
    maxR = max(R)

    Q = zeros(shape = (alternativesCount), dtype = float)
    for i in range(alternativesCount):
        Q[i] = v * (S[i] - minS) / (maxS - minS) + (1 - v) * (R[i] - minR) / (maxR - minR)

    return S, R, Q


# TOPSIS method

def topsis(criteria, weights):
    normalizedCriteria = normalizeCriteriaForTopsis(criteria)
    weightnedCriteria = weightNormalizedCriteria(normalizedCriteria, weights)

    lengths = calcLength(
        weightnedCriteria,
        findPis(weightnedCriteria),
        findNis(weightnedCriteria)
    )

    return lengths

def criterialTopsis(criteria, weights, benefits, costs):
    normalizedCriteria = normalizeCriteriaForCriterialTopsis(criteria, benefits, costs)
    weightnedCriteria = weightNormalizedCriteria(normalizedCriteria, weights)

    lengths = calcLength(
        weightnedCriteria,
        findCriterialPis(weightnedCriteria, benefits, costs),
        findCriterialNis(weightnedCriteria, benefits, costs)
    )

    return lengths


# VIKOR method

def vikor(criteria, weights, v):
    normalizedCriteria = normalizeCriteriaForVikor(criteria)
    weightnedCriteria = weightNormalizedCriteria(normalizedCriteria, weights)
    return calcIntervalsForVikor(weightnedCriteria, v)

def analyzeVInVikor(criteria, weights):
    vrange = arange(start = 0.1, stop = 1, step = 0.1)
    vikors = list()

    for v in vrange:
        S, R, Q = vikor(criteria, weights, v);
        vikors.append(Q)
    
    stats = zeros(shape = (len(criteria), len(vrange)), dtype = float)

    for i in range(len(criteria)):
        for j in range(len(vrange)):
            stats[i][j] = vikors[j][i]

    return stats

# Solution

def lab5():
    baseFilePath = path.dirname(__file__)

    criteria = parseCriteria(
        baseFilePath + 
        '/../input/lab5/var18-criteria.txt'
    );

    weights = normalizeWeights(parseWeights(
        baseFilePath + 
        '/../input/lab5/var18-weight.txt'
    ));

    # Task 1.1
    topsisSolution = topsis(criteria, weights)

    file = open(baseFilePath + '/../output/lab5/var18-topsis.txt', 'w+')
    file.write('TOPSIS RANGE\n')
    writeFloatArray(file, topsisSolution)
    writeFloatArray(file, sorted(topsisSolution))
    file.close()

    # Task 1.2
    criteriaTopsisSolution = criterialTopsis(
        criteria,
        weights,
        range(7),
        range(7, 12)
    )

    file = open(baseFilePath + '/../output/lab5/var18-criteria-topsis.txt', 'w+')
    file.write('TOPSIS RANGE\n')
    writeFloatArray(file, criteriaTopsisSolution)
    writeFloatArray(file, sorted(criteriaTopsisSolution))
    file.close()

    # Task 2.1
    S, R, Q = vikor(criteria, weights, 0.5)

    file = open(baseFilePath + '/../output/lab5/var18-vikor.txt', 'w+')

    file.write('S\n')
    writeFloatArray(file, S)
    writeFloatArray(file, sorted(S))

    file.write('R\n')
    writeFloatArray(file, R)
    writeFloatArray(file, sorted(R))

    file.write('Q\n')
    writeFloatArray(file, Q)
    writeFloatArray(file, sorted(Q))

    file.close()

    #Task 2.2
    stats = analyzeVInVikor(criteria, weights)

    file = open(baseFilePath + '/../output/lab5/var18-analyze-vikor.txt', 'w+')
    for stat in stats:
        writeFloatArray(file, stat)
    file.close();

lab5()
