import ast


class SmellDetector:

    @staticmethod
    def detect(tree):

        smells = []

        for node in ast.walk(tree):

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

        return smells