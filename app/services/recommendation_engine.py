class RecommendationEngine:

    @staticmethod
    def generate(features, code_smells):

        recommendations = []

        # Long functions
        for smell in code_smells:
            if "too long" in smell:
                recommendations.append(
                    "Break large functions into smaller, focused functions."
                )

        # Too many parameters
        for smell in code_smells:
            if "too many parameters" in smell:
                recommendations.append(
                    "Use a configuration object, dictionary, or class to group related parameters."
                )        

        # Recommendations based on detected code smells
        for smell in code_smells:

            if "missing a docstring" in smell:
                recommendations.append(
                    "Add docstrings to improve code readability and maintainability."
                )

            elif "bare 'except:'" in smell:
                recommendations.append(
                    "Catch specific exceptions instead of using bare except clauses."
                )
            elif "too many parameters" in smell:
               recommendations.append(
                    "Reduce the number of function parameters by grouping related values into a class, dictionary, or configuration object."
        )

        # Too many lines
        if features["lines"] > 200:
            recommendations.append(
                "Consider splitting the file into smaller modules"
            )

        # Too many functions
        if features["functions"] > 10:
            recommendations.append(
                "Reduce the number of functions in a single file"
            )

        # Too many imports
        if features["imports"] > 10:
            recommendations.append(
                "Remove unnecessary imports"
            )

        # High complexity
        if features["complexity"] == "High":
            recommendations.append(
                "Simplify complex logic and refactor large functions"
            )

        # Poor quality score
        if features["quality_score"] < 70:
            recommendations.append(
                "Refactor code to improve maintainability"
            )

        # Excellent code
        if not recommendations:
            recommendations.append(
                "Code quality looks excellent"
            )

        return recommendations