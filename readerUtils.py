from structures import Element
import re

insideElements = ['*', '!', '`', '[', '<', '_']

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

def getEmphasis(line, pos):
    count = 0
    while count < 3 or pos == len(line):
        if line[pos] != '_' and line[pos] != '*':
            break
        count += 1
        pos += 1
    return count
# 1 - italic, 2 - strong, 3 - italic & strong, 4 code, 5 - double code, 6 - image, 7 - links, 8 - direct links
def getTypeOfInsideElement(line, pos):
    if line[pos] == '*' or line[pos] == '_':
        return getEmphasis(line, pos)
    elif line[pos] == '`':
        if len(line) > pos + 1 and line[pos + 1] == '`':
            return 5
        return 4
    elif line[pos] == '!':
        return 6
    elif line[pos] == '[':
        return 7
    elif line[pos] == '<':
        return 8

def solveImage(line, pos):
    if line[pos+1] != '[':
        return -1, -1
    end = pos+2
    while end < len(line) and line[end] != ']':
        end += 1
    title = line[pos+2:end]
    if end == len(line) or line[end+1] != '(':
        return -1, -1
    endSource = end + 2
    while endSource < len(line) and line[endSource] != ')':
        endSource += 1
    if endSource == len(line):
        return -1, -1
    source = line[end+2:endSource]
    return Element('img', [], params=[f"src={source}", f"title=\"{title}\""]), endSource

def solveLink(line, pos):
    end = pos + 1
    while end < len(line) and line[end] != "]":
        end += 1
    if end == len(line) or line[end+1] != '(':
        return -1, -1
    name = line[pos+1:end]
    secEnd = end + 2
    while secEnd < len(line) and line[secEnd] != ')':
        secEnd += 1
    inside = line[end+2:secEnd].split('"')
    param = []
    param.append(f"href={inside[0]}")
    if len(inside) > 1:
        param.append(f"title=\"{inside[1]}\"")
    return Element('a', solveInsideLine(name), params=param), secEnd

def solveForType(number, line, pos):
    if number == 1:
        end = pos + 1
        while end < len(line) and (line[end] != '*' and line[end] != '_'):
            end += 1
        return Element("em", solveInsideLine(line[pos+1:end])), end
    if number == 2:
        end = pos + 2
        while end < len(line) and (line[end] != '*' and line[end] != '_') or (line[end-1] != '*' and line[end-1] != '_'):
            end += 1
        return Element('strong', solveInsideLine(line[pos+2:end-1])), end
    if number == 3:
        end = pos + 3
        while end < len(line) and (line[end] != '*' and line[end] != '_') or (line[end-1] != '*' and line[end-1] != '_') or (line[end-2] != '*' and line[end-2] != '_'):
            end += 1
        return Element('em', [Element('strong', solveInsideLine(line[pos+3:end-2]))]),end
    if number == 4:
        end = pos + 1
        while end < len(line) and line[end] != '`':
            end += 1
        return Element('code', solveInsideLine(line[pos+1:end])), end
    if number == 5:
        end = pos + 2
        while end < len(line) and (line[end] != '`' or line[end-1] != '`'):
            end += 1
        return Element('code', solveInsideLine(line[pos+2:end-1], ['`'])), end
    if number == 6:
        return solveImage(line, pos)
    if number == 7:
        return solveLink(line, pos)
    if number == 8:
        end = pos + 1
        while end < len(line) and line[end] != '>':
            end += 1
        a = Element('a', [Element('string', line[pos+1:end])], params=[f"href={line[pos+1:end]}"])
        return a, end
    return -1, -1

def solveInsideLine(line, ignored = []):
    content = []
    escape = False
    randomString = ""
    i = 0
    while i < len(line):
        if line[i] == '\\':
            escape = True
            i += 1
            continue

        escape = False

        if line[i] in insideElements and line[i] not in ignored:
            newElement, end = solveForType(getTypeOfInsideElement(line, i), line, i)
            if newElement == -1 and end == -1:
                randomString = randomString + line[i]
                i += 1
                continue
            content.append(Element("string", randomString))
            content.append(newElement)
            randomString = ""
            i = end + 1
        else:
            randomString = randomString + line[i]
            i += 1
    content.append(Element('string', randomString))
    if len(line) > 1 and line[-1] == ' ' and line[-2] == ' ':
        content.append(Element('br', ""))
    return content