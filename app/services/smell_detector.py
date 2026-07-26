import ast


class SmellDetector:

    @staticmethod
    def detect(tree):

        smells = []

        imported_modules = set()
        used_names = set()

        duplicate_imports = set()

        assigned_variables = set()
        used_variables = set()

        parameters = set()

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for alias in node.names:

                    module = alias.asname or alias.name

                    if module in imported_modules:
                        duplicate_imports.add(module)

                    imported_modules.add(module)

            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:

                    module = alias.asname or alias.name

                    if module in imported_modules:
                        duplicate_imports.add(module)

                    imported_modules.add(module)

            if isinstance(node, ast.Name):
                used_names.add(node.id)

            if isinstance(node, ast.Name):

                if isinstance(node.ctx, ast.Store):
                    assigned_variables.add(node.id)

                elif isinstance(node.ctx, ast.Load):
                    used_variables.add(node.id)            

            # Detect functions without docstrings
            if isinstance(node, ast.FunctionDef):

                for arg in node.args.args:
                    parameters.add(arg.arg)

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

        for module in sorted(duplicate_imports):
            smells.append(
                f"Duplicate import: '{module}'. Consider removing the duplicate import."
         )    
        unused_variables = assigned_variables - used_variables

        for variable in sorted(unused_variables):
            smells.append(
                f"Unused variable: '{variable}'. Consider removing it."
            )

        unused_parameters = parameters - used_variables

        for parameter in sorted(unused_parameters):
            smells.append(
                f"Unused parameter: '{parameter}'. Consider removing it if unnecessary."
          )                

        return smells