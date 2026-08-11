class RecommendationEngine:

    @staticmethod
    def generate(features, code_smells):

        recommendations = set()

        # Recommendations based on detected code smells
        for smell in code_smells:

            if "too long" in smell:
                recommendations.add(
                    "Break large functions into smaller, focused functions."
                )

            if "too many parameters" in smell:
                recommendations.add(
                    "Use a configuration object, dictionary, or class to group related parameters."
                )
                recommendations.add(
                    "Reduce the number of function parameters by grouping related values into a class, dictionary, or configuration object."
                )

            if "Class" in smell and "missing a docstring" in smell:
                recommendations.add(
                    "Add docstrings to classes to improve documentation and maintainability."
                )
            elif "missing a docstring" in smell:
                recommendations.add(
                    "Add docstrings to improve code readability and maintainability."
                )

            if (
                "missing parameter type hints" in smell
                or "return type hint" in smell
            ):
                recommendations.add(
                    "Add type hints to improve readability and static analysis."
                )

            if "bare 'except:'" in smell:
                recommendations.add(
                    "Catch specific exceptions instead of using bare except clauses."
                )

            if "Unused import" in smell:
                recommendations.add(
                    "Remove unused imports to improve code cleanliness and readability."
                )

            if "Duplicate import" in smell:
                recommendations.add(
                    "Remove duplicate imports to keep the code clean and avoid redundancy."
                )

            if "Unused variable" in smell:
                recommendations.add(
                    "Remove unused variables to improve code clarity and maintainability."
                )

            if "Unused parameter:" in smell:
                recommendations.add(
                    "Remove unused parameters to simplify function interfaces."
                )

            if "deeply nested" in smell:
                recommendations.add(
                    "Reduce nested blocks by extracting helper functions or using early returns."
                )

        # File-level recommendations
        if features["lines"] > 200:
            recommendations.add(
                "Consider splitting the file into smaller modules"
            )

        if features["functions"] > 10:
            recommendations.add(
                "Reduce the number of functions in a single file"
            )

        if features["imports"] > 10:
            recommendations.add(
                "Remove unnecessary imports"
            )

        if features["complexity"] == "High":
            recommendations.add(
                "Simplify complex logic and refactor large functions"
            )

        if features["quality_score"] < 70:
            recommendations.add(
                "Refactor code to improve maintainability"
            )

        # Default recommendation
        if not recommendations:
            recommendations.add(
                "Code quality looks excellent"
            )

        # Return deterministic ordering
        return sorted(recommendations)

