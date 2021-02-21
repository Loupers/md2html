from structures import Element
import re

def isWholeLine(line, symbol):
    for i in line:
        if i == '\n':
            break

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
    return Element(tag, solveInsideLine(content))

# 0-blank line, 1-h1, 2-h2, 4 - br, 5 - blockquotes, 6 - ordered list, 7 - unordered list, 8 - line with header, 9-hline, 10 - table
def getTypeOfLine(line):
    if line == '\n':
        return 0

    if line[0] == '=' or line[0] == '-':
        isWhole = isWholeLine(line, line[0])
        if isWhole and line[0] == '-':
            return 2
        elif isWhole and line[0] == '=':
            return 1

    if line[0] == '>':
        return 5

    if checkForOl(line):
        return 6

    if line[0] == '-' or line[0] == '*':
        x = countSymbols(line, line[0])
        if x == 1:
            return 7
        if x >= 3:
            return 9
        return -1

    if line[0] == '+':
        return 7

    if line[0] == '#':
        return 8
        
    if line[0] == '|':
        return 10

    return -1

def checkForOl(line):
    l = line.split('.')
    if len(l[0]) > 0 and l[0].isdigit():
        return True
    return False

def solveList(block):
    el = []
    for i in block:
        el.append(Element("li", solveInsideLine(i)))
    return el


def solveInsideLine(line):
    return line