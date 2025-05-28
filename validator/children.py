import sys

html ="""<html>
<head>
<title>Software Design by Example</title>
</head>
<body>
<h1>Main Title</h1>
<p>introductory paragraph</p>
<ul>
<li>first item</li>
<li>second item is <em>emphasized</em></li>
</ul>
</body>
</html>"""

def recurse(node, catalog):
    assert isinstance(node, Tag)

    if node.name not in catalog:
        catalog[node.name] = set()

    for child in node:
        if isinstance(child, Tag):
            catalog[node.name].add(child.name)
            recurse(child, catalog)

    return catalog

from bs4 import BeautifulSoup, Tag
from visitor import Visitor

doc = BeautifulSoup(html, "html.parser")
catalog = {}
catalog = recurse(doc, catalog)
#print(catalog)

# implementation using visitor pattenr
class Catalog(Visitor):
    def __init__(self):
        super().__init__()
        self.catalog = {}
    
    def _tag_enter(self, node):
        if node.name not in self.catalog:
            self.catalog[node.name] = set()
        for child in node:
            if isinstance(child, Tag):
                self.catalog[node.name].add(child.name)

if __name__ =='__main__':

    with open(sys.argv[1], "r") as reader:
        text = reader.read()
    doc = BeautifulSoup(text, "html.parser")

    catalog = Catalog()
    catalog.visit(doc.html)
    result = catalog.catalog

    for tag, contents in sorted(result.items()):
        print(f"{tag}: {', '.join(sorted(contents))}")



