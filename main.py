from fastapi import FastAPI

app = FastAPI(
    title="AI Research Hub",
    description="An API for managing, organizing, and exploring research papers.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Research Hub!",
        "description": "Your platform for managing and exploring research papers."
    }


@app.get("/about")
def about():
    return {
        "name": "AI Research Hub",
        "description": "A research paper management platform built with FastAPI.",
        "purpose": "To help users organize, explore, and analyze research papers."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "AI Research Hub is up and running."
    }


@app.get("/version")
def version():
    return {
        "application": "AI Research Hub",
        "version": "1.0.0"
    }

