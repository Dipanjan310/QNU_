# generate_requirements.py
import ast

with open("my_script.py") as f:
    tree = ast.parse(f.read())

imports = sorted({
    node.names[0].name.split('.')[0]
    for node in ast.walk(tree)
    if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)
})

with open("requirements.txt", "w") as f:
    for lib in imports:
        if lib not in ("os", "sys", "math", "json", "time", "random", "re"):  # skip standard libraries
            f.write(f"{lib}\n")
