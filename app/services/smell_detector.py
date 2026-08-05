import ast


class SmellDetector:

    @staticmethod
    def get_max_nesting(node, depth=0):
        """
        Recursively determine the maximum nesting depth of
        control-flow statements within a node.
        """
        max_depth = depth

        for child in ast.iter_child_nodes(node):

            if isinstance(
                child,
                (
                    ast.If,
                    ast.For,
                    ast.While,
                    ast.Try,
                    ast.With,
                    ast.Match,
                ),
            ):
                max_depth = max(
                    max_depth,
                    SmellDetector.get_max_nesting(child, depth + 1),
                )
            else:
                max_depth = max(
                    max_depth,
                    SmellDetector.get_max_nesting(child, depth),
                )

        return max_depth

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

            # --------------------------
            # Imports
            # --------------------------
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

            # --------------------------
            # Used names / variables
            # --------------------------
            if isinstance(node, ast.Name):

                used_names.add(node.id)

                if isinstance(node.ctx, ast.Store):
                    assigned_variables.add(node.id)

                elif isinstance(node.ctx, ast.Load):
                    used_variables.add(node.id)

            # --------------------------
            # Function checks
            # --------------------------
            if isinstance(node, ast.FunctionDef):

                for arg in node.args.args:
                    parameters.add(arg.arg)

                # Missing docstring
                if ast.get_docstring(node) is None:
                    smells.append(
                        f"Function '{node.name}' is missing a docstring."
                    )

                # Missing parameter type hints
                missing_parameter_hints = any(
                    arg.annotation is None
                    for arg in node.args.args
                )

                if missing_parameter_hints:
                    smells.append(
                       f"Function '{node.name}' is missing parameter type hints."
                    )

                # Missing return type hint
                if node.returns is None:
                    smells.append(
                        f"Function '{node.name}' is missing a return type hint."
                  )
                # Too many parameters
                if len(node.args.args) > 5:
                    smells.append(
                        f"Function '{node.name}' has too many parameters ({len(node.args.args)}). "
                        "Consider grouping related parameters into a class or dictionary."
                    )

                # Long function
                function_length = node.end_lineno - node.lineno

                if function_length > 50:
                    smells.append(
                        f"Function '{node.name}' is too long ({function_length} lines). "
                        "Consider breaking it into smaller functions."
                    )

                # Deep nesting
                nesting_depth = SmellDetector.get_max_nesting(node)

                if nesting_depth > 4:
                    smells.append(
                        f"Function '{node.name}' is deeply nested ({nesting_depth} levels). "
                        "Consider simplifying the control flow."
                    ) 
            # --------------------------
            # Class checks
            # --------------------------
            elif isinstance(node, ast.ClassDef):

                if ast.get_docstring(node) is None:
                    smells.append(
                        f"Class '{node.name}' is missing a docstring."
             )           

            # --------------------------
            # Bare except
            # --------------------------
            elif isinstance(node, ast.ExceptHandler):

                if node.type is None:
                    smells.append(
                        "Avoid using bare 'except:' clauses. Catch specific exceptions instead."
                    )

        # --------------------------
        # Unused imports
        # --------------------------
        unused_imports = imported_modules - used_names

        for module in sorted(unused_imports):
            smells.append(
                f"Unused import: '{module}'. Consider removing it."
            )

        # --------------------------
        # Duplicate imports
        # --------------------------
        for module in sorted(duplicate_imports):
            smells.append(
                f"Duplicate import: '{module}'. Consider removing the duplicate import."
            )

        # --------------------------
        # Unused variables
        # --------------------------
        unused_variables = assigned_variables - used_variables

        for variable in sorted(unused_variables):
            smells.append(
                f"Unused variable: '{variable}'. Consider removing it."
            )

        # --------------------------
        # Unused parameters
        # --------------------------
        unused_parameters = parameters - used_variables

        for parameter in sorted(unused_parameters):
            smells.append(
                f"Unused parameter: '{parameter}'. Consider removing it if unnecessary."
            )

        return smells