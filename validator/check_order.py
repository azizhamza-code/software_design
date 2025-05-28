from bs4 import BeautifulSoup, NavigableString, Tag
from travel import Flatten

text = """<html lang="en">
<body class="outline narrow">
<p align="left" align="right">paragraph</p>
</body>
</html>"""

def check_h1_first_and_only_one(node:Tag):
    list_ = [node for node in Flatten(doc.body).result() if node.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']]
    if not list_:
        return False    
    h1_list = [e for e in list_ if  e.name =='h1']
    number_of_h1 = len(h1_list)
    if number_of_h1 != 1:
        return  False
    if list_[0].name != 'h1':
        return False
    return True

def check_heading_increse_logic(node):
    list_ = [node.name for node in Flatten(doc.body).result() if node.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']]
    list_index = [int(i[1]) for i in list_]
    for index in range(len(list_index) - 1):
        current = list_index[index]
        next_level = list_index[index + 1]
        if next_level > current + 1:
            return False


if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'r') as reader :
        text = reader.read()
    doc = BeautifulSoup(text, "html.parser")
    resu = check_h1_first_and_only_one(doc.body)
    if resu : 
        print ("the header is respected")
    resu_order = check_h1_first_and_only_one(doc)
    if resu_order:
        print("ok for order")
    
    

