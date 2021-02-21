from structures import Element
from sys import argv
from mdReader import MDReader
from htmlprinter import HTMLPrinter


def checkNotFile(name):
    try:
        open(name, 'r').close()
    except IOError:
        return True
    
    return False


def main():
    nameOfFile = "test.md"
    if checkNotFile(nameOfFile):
        print("Couldn't open and/or find provided file")
        exit()
    f = open(nameOfFile, 'r')
    r = MDReader(f)
    r.readWholeFile()
    f.close()
    printer = HTMLPrinter(r.elements)
    printer.printToFile('test.html')

if __name__ == "__main__":
    main()


