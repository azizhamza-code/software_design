from collections import Counter
import ast
import sys

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

with open(sys.argv[1], "r") as module:
    file = module.read()

tree = ast.parse(file)
find_deplucate = FindDuplicateKeys()
find_deplucate.travers()

