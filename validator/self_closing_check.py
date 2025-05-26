from visitor import Visitor
from bs4 import Tag

class SelfClosing(Visitor):
    def __init__(self):
        super().__init__()
        self.could_be_optimized = []
    
    def _tag_enter(self, node:Tag):
        if len(node.contents) == 0:
            self.could_be_optimized.append((node.name, node.sourceline))
        

if __name__ == '__main__':
    import sys
    from bs4 import BeautifulSoup 
    with open(sys.argv[1] ,'r') as reader:
        text = reader.read()
    doc = BeautifulSoup(text, "html.parser")
    self_closing = SelfClosing()
    self_closing.visit(doc.html)
    print(self_closing.could_be_optimized)




