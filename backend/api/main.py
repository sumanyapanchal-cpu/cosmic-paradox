"""
Cosmic Paradox - FastAPI Backend
Geospatial ML Pipeline for Crop Classification & Moisture Stress Detection
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import logging

from .routers import ml_router, data_router, advisory_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cosmic_paradox")

app = FastAPI(
    title="Cosmic Paradox API",
    description="Geospatial AI/ML Backend — Crop Classification & Moisture Stress Detection",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ml_router.router,       prefix="/api/ml",       tags=["ML Models"])
app.include_router(data_router.router,     prefix="/api/data",     tags=["Satellite Data"])
app.include_router(advisory_router.router, prefix="/api/advisory", tags=["Irrigation Advisory"])


@app.get("/")
async def root():
    return {
        "status": "ONLINE",
        "mission": "COSMIC PARADOX",
        "modules": ["crop_classification", "moisture_stress", "irrigation_advisory", "time_series"],
    }


@app.get("/health")
async def health():
    return {"status": "OK", "satellite_link": "ACTIVE", "ai_core": "READY"}


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
