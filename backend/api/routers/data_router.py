"""api/routers/data_router.py — Satellite data endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List
import random, logging

logger = logging.getLogger(__name__)
router = APIRouter()

ZONES = {
    "PB-01": {"district": "Ludhiana",  "lat": 31.1, "lon": 75.3},
    "PB-02": {"district": "Bathinda",  "lat": 30.2, "lon": 74.8},
    "PB-03": {"district": "Patiala",   "lat": 30.9, "lon": 76.5},
    "PB-04": {"district": "Amritsar",  "lat": 31.6, "lon": 74.2},
}


@router.get("/satellite-passes")
async def get_satellite_passes():
    """Recent satellite acquisition metadata."""
    passes = [
        {"satellite": "Sentinel-2A", "date": "2025-06-20", "cloud_pct": 5,  "sensor": "MSI",   "source": "GEE"},
        {"satellite": "Sentinel-1B", "date": "2025-06-19", "cloud_pct": 0,  "sensor": "SAR",   "source": "GEE"},
        {"satellite": "ResourceSat-2", "date": "2025-06-18", "cloud_pct": 8, "sensor": "LISS3", "source": "Bhoonidhi"},
        {"satellite": "MODIS Terra",  "date": "2025-06-17", "cloud_pct": 12, "sensor": "MOD16", "source": "GEE"},
        {"satellite": "Landsat-9",    "date": "2025-06-15", "cloud_pct": 3,  "sensor": "OLI",   "source": "GEE"},
    ]
    return {"passes": passes, "total": len(passes)}


@router.get("/indices/{zone_id}")
async def get_indices(zone_id: str):
    """Current spectral indices for a zone."""
    if zone_id not in ZONES:
        raise HTTPException(404, detail=f"Zone {zone_id} not found")
    random.seed(hash(zone_id))
    return {
        "zone_id":  zone_id,
        "NDVI":     round(random.uniform(0.40, 0.80), 3),
        "NDWI":     round(random.uniform(-0.10, 0.35), 3),
        "EVI":      round(random.uniform(0.30, 0.70), 3),
        "SAVI":     round(random.uniform(0.35, 0.65), 3),
        "LSWI":     round(random.uniform(0.10, 0.50), 3),
        "VV_dB":    round(random.uniform(-15, -6), 2),
        "VH_dB":    round(random.uniform(-22, -12), 2),
        "updated":  "2025-06-20",
    }


@router.get("/zones")
async def list_zones():
    return {"zones": [{"zone_id": k, **v} for k, v in ZONES.items()]}
