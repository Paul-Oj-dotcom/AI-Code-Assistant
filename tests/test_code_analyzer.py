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

def test_deeply_nested_function_detected():

    analyzer = CodeAnalyzer()

    code = """
def process():
    if True:
        for i in range(5):
            if i > 0:
                while i < 3:
                    try:
                        print(i)
                    except Exception:
                        pass
"""

    result = analyzer.analyze(code)

    assert any(
        "deeply nested" in smell
        for smell in result["code_smells"]
    )

    assert any(
        "Reduce nested blocks"
        in recommendation
        for recommendation in result["recommendations"]
    )

def test_missing_type_hints_recommendation():

    analyzer = CodeAnalyzer()

    code = """
def add(a, b):
    return a + b
"""

    result = analyzer.analyze(code)

    assert any(
        "type hints" in recommendation.lower()
        for recommendation in result["recommendations"]
    )

def test_missing_type_hints_affects_quality_score():

    analyzer = CodeAnalyzer()

    code = """
def add(a, b):
    return a + b
"""

    result = analyzer.analyze(code)

    assert result["quality_score"] < 100

def test_missing_return_type_hint_detected():

    analyzer = CodeAnalyzer()

    code = """
def add(a: int, b: int):
    return a + b
"""

    result = analyzer.analyze(code)

    assert any(
        "return type hint" in smell.lower()
        for smell in result["code_smells"]
    )
def test_missing_class_docstring_detected():

    analyzer = CodeAnalyzer()

    code = """
class Person:
    def __init__(self, name):
        self.name = name
"""

    result = analyzer.analyze(code)

    assert any(
        "class" in smell.lower() and "missing a docstring" in smell.lower()
        for smell in result["code_smells"]
    )
def test_missing_class_docstring_recommendation():

    analyzer = CodeAnalyzer()

    code = """
class Person:
    def __init__(self, name):
        self.name = name
"""

    result = analyzer.analyze(code)

    assert any(
        "classes" in recommendation.lower()
        and "docstrings" in recommendation.lower()
        for recommendation in result["recommendations"]
    )
def test_missing_class_docstring_affects_quality_score():

    analyzer = CodeAnalyzer()

    code = """
class Person:
    def __init__(self, name):
        self.name = name
"""

    result = analyzer.analyze(code)

    assert result["quality_score"] < 100 

def test_class_with_docstring_not_flagged():

    analyzer = CodeAnalyzer()

    code = """
class Person:
    \"\"\"Represent a person.\"\"\"

    def __init__(self, name: str) -> None:
        self.name = name
"""

    result = analyzer.analyze(code)

    assert not any(
        "class" in smell.lower()
        and "missing a docstring" in smell.lower()
        for smell in result["code_smells"]
    )

def test_complete_type_hints_not_flagged():

    analyzer = CodeAnalyzer()

    code = """
def add(a: int, b: int) -> int:
    '''Add two integers.'''
    return a + b
"""

    result = analyzer.analyze(code)

    assert not any(
        "type hint" in smell.lower()
        for smell in result["code_smells"]
    )

def test_clean_code_has_excellent_quality():

    analyzer = CodeAnalyzer()

    code = """
def add(a: int, b: int) -> int:
    \"\"\"Add two integers.\"\"\"
    return a + b
"""

    result = analyzer.analyze(code)

    assert result["code_smells"] == []
    assert result["quality_score"] >= 90
    assert result["quality"] == "Excellent"                           