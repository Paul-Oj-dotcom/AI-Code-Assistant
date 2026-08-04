class QualityScorer:

    @staticmethod
    def score(features, code_smells):

        quality_score = 100

        if features["lines"] > 100:
            quality_score -= 20

        if features["functions"] > 10:
            quality_score -= 20

        if features["classes"] > 5:
            quality_score -= 20

        if features["imports"] > 10:
            quality_score -= 10

        if features["complexity"] == "High":
            quality_score -= 20
        elif features["complexity"] == "Medium":
            quality_score -= 10

        # Penalties based on detected smells
        for smell in code_smells:

            if "missing a docstring" in smell:
                quality_score -= 5

            elif "missing type hints" in smell:
                quality_score -= 3      

            elif "bare 'except:'" in smell:
                 quality_score -= 10

            elif "too many parameters" in smell:
                 quality_score -= 5

            elif "too long" in smell:
                 quality_score -= 10

              

        quality = "Poor"

        if quality_score >= 90:
            quality = "Excellent"
        elif quality_score >= 75:
            quality = "Good"
        elif quality_score >= 50:
            quality = "Fair"

        return quality_score, quality