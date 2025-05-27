from visitor import Visitor
from bs4 import Tag, BeautifulSoup
import sys
import yaml

class Check(Visitor):
    def __init__(self, manifest):
        self.manifest = manifest
        self.problems = {}

    def _tag_enter(self, node):
        actual_children = {child.name for child in node if isinstance(child, Tag)}
        expected_children = self.manifest.get(node.name, set())
        unexpected_children = actual_children - expected_children
        if unexpected_children:
            existing_errors = self.problems.get(node.name, set())
            self.problems[node.name] = existing_errors | unexpected_children

    
def read_manifest(filename):
    with open(filename, "r") as reader:
        result = yaml.load(reader, Loader=yaml.FullLoader)
        for key in result:
            result[key] = set(result[key])
        return result

manifest = read_manifest(sys.argv[1])
with open(sys.argv[2], "r") as reader:
    text = reader.read()
doc = BeautifulSoup(text, "html.parser")

checker = Check(manifest)
checker.visit(doc.html)
for key, value in checker.problems.items():
    print(f"{key}: {', '.join(sorted(value))}")