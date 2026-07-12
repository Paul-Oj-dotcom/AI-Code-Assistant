@app.post("/analyze")
def analyze():

    sample_code = """
import pandas as pd

def add(a, b):
    return a + b

class Calculator:
    pass
"""

    return analyzer.analyze(sample_code)