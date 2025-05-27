from visitor import Visitor

class Flatten(Visitor):

    def __init__(self, node):
        self.node = node
        self.linear = []

    def _tag_enter(self, node): 
        self.linear.append(node)
    
    def result(self):
        super().visit(self.node)
        return self.linear

if __name__ =='__main__':
    import sys
    from bs4 import BeautifulSoup, NavigableString, Tag
    from dom import display
    with open(sys.argv[1], 'r') as reader :
        text = reader.read()
    doc = BeautifulSoup(text, "html.parser")

    for node in Flatten(doc.html).result():
        print(node)


