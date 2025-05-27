from bs4 import BeautifulSoup, NavigableString, Tag

text = """<html lang="en">
<body class="outline narrow">
<p align="left" align="right">paragraph</p>
</body>
</html>"""

def display(node):
    if isinstance(node, NavigableString):
        print(f"string: {repr(node.string)}")
        return
    else:
        print(f"node: {node.name}, {node.attrs}")
        for child in node:
            display(child)

if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'r') as reader :
        text = reader.read()
    doc = BeautifulSoup(text, "html.parser")
    display(doc)

