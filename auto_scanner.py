import ast

def EXTRACT_PACKAGES(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
    modules = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mod = node.names[0].name.split('.')[0] if isinstance(node, ast.Import) else node.module.split('.')[0]
            modules.append(mod)
    return set(modules)
