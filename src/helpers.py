def increase(num):
    return num + 1

def increaseEach(array):
    return map(increase, array);

def arrayToStr(array, prefix = '', postfix = ''):
    separator = ', '
    return prefix + '{' + separator.join(map(str, array)) +  '}' + postfix
    
def intToStr(n):
    return ' ' + str(n) + ' ';
    