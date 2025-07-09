import ast
import sys

from collections import Counter

class CollectNames(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.names = {}

    def visit_Assign(self, node):
        for var in node.targets:
            self.add(var, var.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.add(node, node.name)
        self.generic_visit(node)

    def add(self, node, name):
        loc = (node.lineno, node.col_offset)
        self.names[name] = self.names.get(name, set())
        self.names[name].add(loc)

    def position(self, node):
        return ({node.lineno}, {node.col_offset})


class FindDuplicateKeys(ast.NodeVisitor):
    def visit_Dict(self, node):
        seen = Counter()
        for key in node.keys:
            if isinstance(key, ast.Constant):
                seen[key.value] += 1
        problems = {k for (k, v) in seen.items() if v > 1}
        self.report(node, problems)
        self.generic_visit(node)

    def report(self, node, problems):
        if problems:
            msg = ", ".join(p for p in problems)
            print(f"duplicate key(s) {{{msg}}} at {node.lineno}")



with open(sys.argv[1], "r") as reader:
    source = reader.read()


has_duplicates = {
    "third": 3,
    "fourth": 4,
    "fourth": 5,
    "third": 6
}


tree = ast.parse(source)
names = CollectNames()
names.visit(tree)
print(names.names)
