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

def test_unused_import_detected():
    analyzer = CodeAnalyzer()

    code = """
import math
import random

print(math.pi)
"""

    result = analyzer.analyze(code)

    assert "Unused import: 'random'. Consider removing it." in result["code_smells"]
    assert "Unused import: 'math'. Consider removing it." not in result["code_smells"] 

def test_used_import_not_reported():
    analyzer = CodeAnalyzer()

    code = """
import math

print(math.pi)
"""

    result = analyzer.analyze(code)

    assert result["code_smells"] == []

def test_unused_variable_detected():
    analyzer = CodeAnalyzer()

    code = """
x = 10
y = 20

print(x)
"""

    result = analyzer.analyze(code)

    assert "Unused variable: 'y'. Consider removing it." in result["code_smells"]
    assert "Unused variable: 'x'. Consider removing it." not in result["code_smells"]

def test_unused_parameter_detected():
    analyzer = CodeAnalyzer()

    code = """
def greet(name, age):
    print(name)
"""

    result = analyzer.analyze(code)

    assert (
        "Unused parameter: 'age'. Consider removing it if unnecessary."
        in result["code_smells"]
    )

    assert (
        "Remove unused parameters to simplify function interfaces."
        in result["recommendations"]
    )
def test_duplicate_import_detected():

    analyzer = CodeAnalyzer()

    code = """
import math
import random
import math
"""

    result = analyzer.analyze(code)

    assert (
        "Duplicate import: 'math'. Consider removing the duplicate import."
        in result["code_smells"]
    )                           