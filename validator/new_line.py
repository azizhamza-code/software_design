from visitor import Visitor
from bs4 import BeautifulSoup, NavigableString, Tag


class Document(Visitor):
    def __init__(self):
        super().__init__()
        self.nodes_to_remove = []

    def _text(self, node):
        if node.string.strip() == "":
            print("i am in new line")
            self.nodes_to_remove.append(node)
    
    def remove_newline_nodes(self):
        for node in self.nodes_to_remove:
            node.extract()

if __name__ =='__main__':

    import sys
    from bs4 import BeautifulSoup, NavigableString, Tag
    from dom import display
    with open(sys.argv[1], 'r') as reader :
        text = reader.read()
    doc = BeautifulSoup(text, "html.parser")
    docu = Document()
    display(doc)
    docu.visit(doc)
    docu.remove_newline_nodes()
    display(doc)


