from structures import Element
# 0-blank line, 1-h1, 2-h2, 4 - br, 5 - blockquotes, 6 - ordered list, 7 - unordered list, 8 - image, 9-hline, 10 - escape char
def parseLine(line):
    if len(line) == 0:
        return 0

    if line[0] == '=' or line[0] == '-':
        isWhole = isWholeLine(line, line[0])
        if isWhole and line[0] == '-':
            return 2
        elif isWhole and line[0] == '=':
            return 1
    
    if line[-1] == ' ' and line[-2] == ' ':
        #TODO e = solveInsideLine(line)
        #TODO e.append(Element('br', []))

    if line[0] == '>':
        return 5

    if line[0] == '1.':
        return 6

    if line[0] == '-' or line[0] == '*':
        x = countSymbols(line, line[0])
        if x == 1:
            return 7
        if x >= 3:
            return 9

    if line[0] == '+':
        return 7

    if line[0] == '!':
        return 8
    
    if line[0] == '\\':
        return 10
    


def getTypeOfHeader(line):
    headerCounter = 0
    for i in line:
        if i == '#':
            headerCounter += 1
        else:
            break
    tag = "error"
    if headerCounter == 1:
        tag = "h1"
    elif headerCounter == 2:
        tag = "h2"
    elif headerCounter == 3:
        tag = "h3"
    elif headerCounter == 4:
        tag = "h4"
    elif headerCounter == 5:
        tag = "h5"
    elif headerCounter >= 6:
        tag = "h6"
    content = line[headerCounter:]
    return Element(tag, parseLine(content))

def isWholeLine(line, symbol):
    for i in line:
        if i != symbol:
            return False
    return True

def countSymbols(line, symbol):
    count = 0
    for i in line:
        if i == symbol:
            count+=1
        else:
            break
    return count