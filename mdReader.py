from structures import Element
from readerUtils import *
import random
import string

class MDReader:

    def __init__(self, file):
        self.file = file
        self.elements = []
        self.currentLine = ""

    def readWholeFile(self):
        while True:
            line = self.file.readline()

            if not line:
                break
            self.currentLine = line
            self.solveLine(getTypeOfLine(line), line)

    def setLastToParagraph(self):
        content = []
        for i in range(len(self.elements) - 1, -1, -1):
            if self.elements[i].tag == 'p':
                break
            content.append(self.elements.pop(i))
        self.elements.append(Element('p', reversed(content)))      

    def solveLine(self, number, line):
        if number == 0:
            self.setLastToParagraph()
        elif number == 1:
            self.setLastToHeader(1)
        elif number == 2:
            self.setLastToHeader(2)
        elif number == 5:
            self.elements.append(Element("blockquote", self.solveBlockAsFile(self.readSymbolBlock(['>']))))
        elif number == 6:
            self.elements.append((Element("ol", solveList(self.readOrderedList()))))
        elif number == 7:
            self.elements.append((Element("ul", solveList(self.readSymbolBlock(['+', '-', '*'])))))
        elif number == 8:
            self.elements.append(getTypeOfHeader(line))
        elif number == 9:
            self.elements.append((Element("hr", [])))
        elif number == 10:
            self.elements.append(Element("table", solveTable(self.readTable())))
        elif number == -1:
            self.elements.append(Element('div', solveInsideLine(line)))


    def setLastToHeader(self, typ):
        x = self.elements.pop(-1)
        e = Element("", [])
        e.content = x
        if typ == 1:
            e.tag = "h1"
        elif typ == 2:
            e.tag = "h2"
        else:
            print("error in setting last header")
            exit()
        self.elements.append(e)

    def readSymbolBlock(self, symbol):
        block = [self.currentLine[1:]]
        self.currentLine = self.file.readline()
        while self.currentLine and (self.currentLine[0] in symbol):
            if type(symbol) == type(''):
                block.append(self.currentLine[len(symbol):].lstrip())
            else:
                block.append(self.currentLine[1:])
            self.currentLine = self.file.readline()
        return block

    def solveBlockAsFile(self, block):
        newFileName = "/tmp/" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
        f = open(newFileName, 'w+')
        for i in block:
            f.write(i[1:])
        f.close()
        r = MDReader(open(newFileName, 'r'))
        r.readWholeFile()
        return r.elements

    def readOrderedList(self):
        block = [''.join(self.currentLine.split('.')[1:])]
        self.currentLine = self.file.readline()
        while checkForOl(self.currentLine.lstrip()):
            if self.currentLine[0:4] == '    ':
                block.append(Element('ol', solveList(x.lstrip().split('.')[1:] for x in self.readSymbolBlock('    '))))
            block.append(''.join(self.currentLine.split('.')[1:]))
            self.currentLine = self.file.readline()
        return block

    def readTable(self):
        block = []
        while self.currentLine and self.currentLine[0] == '|':
            block.append(self.currentLine)
            self.currentLine = self.file.readline()
        return block