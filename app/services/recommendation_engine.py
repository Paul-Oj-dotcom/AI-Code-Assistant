class RecommendationEngine:

    @staticmethod
    def generate(features, code_smells):

        recommendations = set()

        # Long functions
        for smell in code_smells:
            if "too long" in smell:
                recommendations.add(
                    "Break large functions into smaller, focused functions."
                )

        # Too many parameters
        for smell in code_smells:
            if "too many parameters" in smell:
                recommendations.add(
                    "Use a configuration object, dictionary, or class to group related parameters."
                )        

        # Recommendations based on detected code smells
        for smell in code_smells:


            if "missing a docstring" in smell:
                recommendations.add(
                    "Add docstrings to improve code readability and maintainability."
                )
    

            elif "missing parameter type hints" in smell or "return type hint" in smell:
                 recommendations.add(
                     "Add type hints to improve readability and static analysis."
                )    

            elif "bare 'except:'" in smell:
                recommendations.add(
                    "Catch specific exceptions instead of using bare except clauses."
                )
            elif "too many parameters" in smell:
               recommendations.add(
                    "Reduce the number of function parameters by grouping related values into a class, dictionary, or configuration object."
            )
               
            elif "Unused import" in smell:
                recommendations.add(
                    "Remove unused imports to improve code cleanliness and readability."
                )

            elif "Duplicate import" in smell:
                recommendations.add(
                    "Remove duplicate imports to keep the code clean and avoid redundancy."
                )    

            elif "Unused variable" in smell:
                recommendations.add(
                    "Remove unused variables to improve code clarity and maintainability."
               )

            elif "deeply nested" in smell:
                recommendations.add(
                    "Reduce nested blocks by extracting helper functions or using early returns."
               )           

        # Too many lines
        if features["lines"] > 200:
            recommendations.add(
                "Consider splitting the file into smaller modules"
            )

        # Too many functions
        if features["functions"] > 10:
            recommendations.add(
                "Reduce the number of functions in a single file"
            )

        # Too many imports
        if features["imports"] > 10:
            recommendations.add(
                "Remove unnecessary imports"
            )

        # High complexity
        if features["complexity"] == "High":
            recommendations.add(
                "Simplify complex logic and refactor large functions"
            )

        # Poor quality score
        if features["quality_score"] < 70:
            recommendations.add(
                "Refactor code to improve maintainability"
            )

        # Excellent code
        if not recommendations:
            recommendations.add(
                "Code quality looks excellent"
            )

        for smell in code_smells:
            if "Unused parameter:" in smell:
                recommendations.add(
                    "Remove unused parameters to simplify function interfaces."
            )           

        return list(recommendations)