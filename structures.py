#store of md tags
class Element:
    #name of type of element, sets what element it is
    tag = "string"
    #other elements inside of this element
    content = []

    def __init__(self, tag, content):
        self.tag = tag
        self.content = content