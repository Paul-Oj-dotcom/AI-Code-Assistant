from app.services.code_analyzer import CodeAnalyzer


def test_simple_function_analysis():
    analyzer = CodeAnalyzer()

    code = """
def hello():
    print("Hello")
"""

    result = analyzer.analyze(code)

    assert result["functions"] == 1
    assert result["classes"] == 0
    assert result["imports"] == 0
    assert result["complexity"] == "Low"

def test_missing_docstring_detection():
    analyzer = CodeAnalyzer()

    code = """
def calculate(a, b):
    return a + b
"""

    result = analyzer.analyze(code)

    assert "missing a docstring" in result["code_smells"][0].lower()

def test_long_function_detection():
    analyzer = CodeAnalyzer()

    body = "\n".join(["    print('line')"] * 60)

    code = f'''
def big_function():
{body}
'''

    result = analyzer.analyze(code)

    assert any(
        "too long" in smell.lower()
        for smell in result["code_smells"]
    ) 

def test_long_function_recommendation():
    analyzer = CodeAnalyzer()

    body = "\n".join(["    print('line')"] * 60)

    code = f'''
def big_function():
{body}
'''

    result = analyzer.analyze(code)

    assert any(
        "break large functions" in recommendation.lower()
        for recommendation in result["recommendations"]
    )

def test_invalid_python_code():
    analyzer = CodeAnalyzer()

    code = """
def hello(
"""

    result = analyzer.analyze(code)

    assert result["status"] == "error"
    assert "message" in result           