from structures import Element

class HTMLPrinter:

    def __init__(self, elements):
        self.elements = elements

    def preparePrintToFile(self):
        toWriteIn = ""
        if type(self.elements) == type(Element("", [])):
            x = self.elements
            self.elements = []
            self.elements.append(x)
        for element in self.elements:
            if type(element) == type(''):
                toWriteIn = toWriteIn + element
                continue
            if  element.tag == "string":
                toWriteIn = toWriteIn + element.content
            else:
                toWriteIn = toWriteIn + f"<{element.tag}"
                for i in element.params:
                    toWriteIn += f" {i}"
                toWriteIn = toWriteIn + '>' + HTMLPrinter(element.content).preparePrintToFile()
                p = HTMLPrinter(element.content)
                x = p.preparePrintToFile()
                toWriteIn = toWriteIn + f"</{element.tag}>"
        return toWriteIn

    def printToFile(self, fileName):
        f = open(fileName, 'w+')
        f.write(self.preparePrintToFile())
        f.close()