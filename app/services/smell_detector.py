import ast


class SmellDetector:

    @staticmethod
    def detect(tree):

        smells = []

        imported_modules = set()
        used_names = set()

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_modules.add(alias.asname or alias.name)

            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported_modules.add(alias.asname or alias.name)

            if isinstance(node, ast.Name):
                used_names.add(node.id)        

            # Detect functions without docstrings
            if isinstance(node, ast.FunctionDef):

                if ast.get_docstring(node) is None:
                    smells.append(
                        f"Function '{node.name}' is missing a docstring."
                    )
                # Detect functions with too many parameters
                if len(node.args.args) > 5:
                    smells.append(
                        f"Function '{node.name}' has too many parameters ({len(node.args.args)}). Consider grouping related parameters into a class or dictionary."
                    )
                 # Detect long functions
                function_length = (
                    node.end_lineno - node.lineno
               )

                if function_length > 50:
                    smells.append(
                        f"Function '{node.name}' is too long ({function_length} lines). Consider breaking it into smaller functions."
                   )       

            # Detect bare except clauses
            elif isinstance(node, ast.ExceptHandler):

                if node.type is None:
                    smells.append(
                        "Avoid using bare 'except:' clauses. Catch specific exceptions instead."
                    )

        unused_imports = imported_modules - used_names

        for module in sorted(unused_imports):
            smells.append(
                f"Unused import: '{module}'. Consider removing it."
            )        

        return smells