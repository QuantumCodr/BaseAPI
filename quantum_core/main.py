from fastapi import FastAPI

from quantum_core.core.config import settings


# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)


# Root endpoint (system check)
@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "status": "running",
        "version": "1.0.0"
    }


# Health check endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }