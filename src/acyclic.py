from section import getBottomSection

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
    