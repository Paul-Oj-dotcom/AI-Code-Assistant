import ast
from app.services.recommendation_engine import RecommendationEngine
from app.services.smell_detector import SmellDetector
from app.services.quality_scorer import QualityScorer


class CodeAnalyzer:

    def analyze(self, code: str):

        try:
            tree = ast.parse(code)

        except SyntaxError as e:
            return {
                "status": "error",
                "message": str(e)
            }
        code_smells = SmellDetector.detect(tree)

        functions = 0
        classes = 0
        imports = 0

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):
                functions += 1

            elif isinstance(node, ast.ClassDef):
                classes += 1

            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports += 1

        lines = len(code.splitlines())

        complexity = "Low"

        if functions > 5:
            complexity = "Medium"

        if functions > 10:
            complexity = "High"

        features = {
             "lines": lines,
             "functions": functions,
             "classes": classes,
             "imports": imports,
             "complexity": complexity,
       }

        quality_score, quality = QualityScorer.score(
            features,
            code_smells
     )

        features["quality_score"] = quality_score

        recommendations = RecommendationEngine.generate(
            features,
            code_smells
     )
        return {
            **features,
            "quality": quality,
            "recommendations": recommendations,
            "code_smells": code_smells
        }
    # Sprint 010 WatchFiles test

    