from structures import Element
from sys import argv

elements = []

def readMD(file):
    x = file.readline()

def setLastToHeader(typ):
    global elements
    x = elements.pop(-1)
    e = Element()
    e.content = x
    if typ == -1:
        e.tag = "h1"
    elif typ == -2:
        e.tag = "h2"
    else:
        #TODO throw exception
    elements.append(e)


def setLastToParagraph():
    global elements
    content = []
    i = -1
    for i in range(len(elements) - 1, -1, -1):
        if elements[i].tag == 'p':
            break
        content.append(elements.pop(i))
    elements.append(Element('p', content))      

def checkNotFile(name):
    try:
        open(name, 'r').close()
    except IOError:
        return True
    
    return False


def __main__():
    nameOfFile = argv[1]
    if checkNotFile(nameOfFile):
        print("Couldn't open and/or find provided file")
        exit()
    f = open(nameOfFile, 'r')
    readMD(f)

