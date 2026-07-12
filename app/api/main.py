from fastapi import FastAPI
from app.services.code_analyzer import CodeAnalyzer
from app.models.code_request import CodeRequest

app = FastAPI(
    title="AI Code Assistant",
    version="1.0.0"
)

analyzer = CodeAnalyzer()


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Code Assistant",
        "lead_engineer": "Paul",
        "technical_architect": "IJALA",
        "status": "ACTIVE"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "server": "running"
    }


@app.get("/about")
def about():
    return {
        "project": "AI Code Assistant",
        "version": "1.0",
        "mission": "Assist developers with code analysis and generation"
    }


@app.post("/analyze")
def analyze(request: CodeRequest):
    return analyzer.analyze(request.code)