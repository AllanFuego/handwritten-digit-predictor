from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router

app = FastAPI(
    title="Handwritten Digit Recognition API",
    description="FastAPI backend for handwritten digit recognition using a trained KNN model.",
    version="1.0.0"
)

# ----------------------------------------------------
# CORS Configuration
# ----------------------------------------------------

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",   # preview - ADD THIS!
    "http://127.0.0.1:4173",   # preview - ADD THIS!
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Include API Routes
# ----------------------------------------------------

app.include_router(router)

# ----------------------------------------------------
# Root Endpoint
# ----------------------------------------------------

@app.get("/")
def home():
    return {
        "success": True,
        "message": "Handwritten Digit Recognition API is running 🚀",
        "documentation": "/docs",
        "predict_endpoint": "/predict"
    }

# ----------------------------------------------------
# Health Check
# ----------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }