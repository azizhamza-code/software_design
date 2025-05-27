from visitor import Visitor

class ImageAtt(Visitor):

    def __init__(self, node):
        self.node = node
        self.img_to_be_reported = []
        self.figure_to_be_reported = []
        self.img_caption_duplicate = []

    def _tag_enter(self, node): 
        if node.name =='img':
            if 'alt' not in node.attrs:
                self.img_to_be_reported.append(node)
        if node.name == 'figure':
            caption_number = 0
            for child in node:
                if isinstance(child, Tag):
                    if child.name == 'figcaption':
                        caption_number = caption_number + 1
            if caption_number > 1 : 
                self.figure_to_be_reported.append(node)
        if node.name == 'figure':
            we_have_img = True
            img_txt = ''
            for child in node:
                if isinstance(child, Tag):
                    if child.name == 'img':
                        we_have_img = True
                        img_txt = child.attrs['alt']
                if isinstance(child, Tag):
                    if child.name == 'figcaption' and we_have_img:
                        if child.string == img_txt:
                            self.img_caption_duplicate.append(node)

    def result(self):
        self.visit(self.node)
        return self.img_to_be_reported, self.figure_to_be_reported, self.img_caption_duplicate


if __name__ =='__main__':
    import sys
    from bs4 import BeautifulSoup, NavigableString, Tag
    from dom import display
    with open(sys.argv[1], 'r') as reader :
        text = reader.read()
    doc = BeautifulSoup(text, "html.parser")
    img, figure, dup = ImageAtt(doc).result()
    print(img)
    print(figure)
    print(dup)
    

