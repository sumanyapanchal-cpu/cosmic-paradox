"""
api/routers/ml_router.py
-------------------------
REST endpoints for ML model training, prediction, and results.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# ── Mock data helpers (replace with real model calls in production) ──────────

ZONES = {
    "PB-01": {"crop": "Rice (Kharif)",  "lat": 31.1, "lon": 75.3, "district": "Ludhiana"},
    "PB-02": {"crop": "Cotton",         "lat": 30.2, "lon": 74.8, "district": "Bathinda"},
    "PB-03": {"crop": "Wheat (Rabi)",   "lat": 30.9, "lon": 76.5, "district": "Patiala"},
    "PB-04": {"crop": "Maize",          "lat": 31.6, "lon": 74.2, "district": "Amritsar"},
}

STRESS_COLORS = {
    "NONE": "#00ff88", "MILD": "#ffd700",
    "MODERATE": "#ffaa00", "SEVERE": "#ff6600", "CRITICAL": "#ff2222",
}


# ── Request / Response schemas ────────────────────────────────────────────────

class TrainRequest(BaseModel):
    model_type:     str  = Field("RandomForest", description="'RandomForest' | 'XGBoost'")
    n_estimators:   int  = Field(300, ge=50, le=2000)
    n_samples:      int  = Field(5000, ge=100, le=100000)
    random_state:   int  = Field(42)


class PredictRequest(BaseModel):
    zone_id:    str
    model_type: str = "RandomForest"
    week:       Optional[int] = None   # 1–52; None = current


class TimeSeriesRequest(BaseModel):
    zone_id:    str
    start_date: str   # YYYY-MM-DD
    end_date:   str
    interval:   str = "weekly"    # weekly | fortnightly | monthly


# ── Synthetic data generator (for demo / testing) ────────────────────────────

def _synthetic_training_data(n: int = 5000) -> pd.DataFrame:
    """
    Generate synthetic multi-spectral + temporal training data.
    In production, replace with real Bhoonidhi / GEE-extracted features.
    """
    np.random.seed(42)

    n_classes = 8
    labels    = np.random.choice(list(range(n_classes)), size=n)
    records   = []

    for lbl in labels:
        # Simulate crop-specific spectral signatures
        base_ndvi  = 0.2 + lbl * 0.07 + np.random.normal(0, 0.05)
        base_evi   = base_ndvi * 0.85
        base_ndwi  = -0.1 + lbl * 0.03 + np.random.normal(0, 0.04)
        blue  = 0.05 + np.random.normal(0, 0.01)
        green = 0.08 + base_ndvi * 0.2
        red   = 0.06 + np.random.normal(0, 0.02)
        nir   = red + base_ndvi * (red + nir if False else 0) + np.random.uniform(0.2, 0.6)
        nir   = np.random.uniform(0.3, 0.7)
        swir1 = nir - base_ndwi * (nir + np.random.uniform(0.05, 0.3))
        swir2 = swir1 * np.random.uniform(0.6, 0.9)
        re    = (nir + red) / 2

        records.append({
            "B2_blue": blue, "B3_green": green, "B4_red": red,
            "B5_rededge": re, "B8_nir": nir,
            "B11_swir1": swir1, "B12_swir2": swir2,
            "VV_backscatter": -10 + lbl * 0.5 + np.random.normal(0, 1.5),
            "VH_backscatter": -17 + lbl * 0.4 + np.random.normal(0, 1.5),
            "ndvi_mean_w1": base_ndvi + np.random.normal(0, 0.03),
            "ndvi_mean_w2": base_ndvi + np.random.normal(0, 0.03),
            "ndvi_mean_w3": base_ndvi * 1.1 + np.random.normal(0, 0.03),
            "ndvi_mean_w4": base_ndvi * 0.95 + np.random.normal(0, 0.03),
            "ndvi_std_monthly":  abs(np.random.normal(0.05, 0.02)),
            "ndvi_max_monthly":  base_ndvi + 0.15,
            "ndvi_min_monthly":  base_ndvi - 0.10,
            "evi_mean_monthly":  base_evi,
            "lswi_mean_monthly": base_ndwi,
            "elevation": np.random.uniform(200, 350),
            "slope":     np.random.uniform(0, 5),
            "aspect":    np.random.uniform(0, 360),
            "crop_label": lbl,
        })

    return pd.DataFrame(records)


def _make_timeseries(zone_id: str, n_weeks: int = 52) -> List[Dict]:
    """Generate synthetic NDVI time series for a zone."""
    np.random.seed(hash(zone_id) % 2**31)
    base  = 0.3 + np.random.uniform(0, 0.3)
    trend = []

    for w in range(n_weeks):
        phase    = (w / n_weeks) * 2 * np.pi
        ndvi     = base + 0.35 * np.sin(phase - 1) + np.random.normal(0, 0.03)
        evi      = ndvi * 0.85
        moisture = 0.4 + 0.2 * np.sin(phase) + np.random.normal(0, 0.04)
        trend.append({
            "week":     w + 1,
            "ndvi":     round(max(0.05, min(0.95, ndvi)), 3),
            "evi":      round(max(0.05, min(0.90, evi)), 3),
            "moisture": round(max(0.10, min(0.90, moisture)), 3),
        })
    return trend


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/train")
async def train_model(req: TrainRequest, bg: BackgroundTasks):
    """
    Train a crop classification model.
    In production, loads labeled raster data from storage.
    """
    logger.info(f"Training request: {req.model_type}, samples={req.n_samples}")

    # Simulate training metrics (replace with real training in production)
    import random, time
    random.seed(req.random_state)

    accuracy  = round(random.uniform(0.88, 0.96), 4)
    f1_score  = round(random.uniform(0.86, 0.95), 4)
    oob_score = round(random.uniform(0.85, 0.94), 4) if req.model_type == "RandomForest" else None

    top_features = [
        {"feature": "NDVI",            "importance": round(random.uniform(0.10, 0.18), 4)},
        {"feature": "ndvi_mean_w3",    "importance": round(random.uniform(0.08, 0.14), 4)},
        {"feature": "EVI",             "importance": round(random.uniform(0.07, 0.12), 4)},
        {"feature": "LSWI",            "importance": round(random.uniform(0.06, 0.11), 4)},
        {"feature": "VV_backscatter",  "importance": round(random.uniform(0.05, 0.10), 4)},
        {"feature": "NDWI",            "importance": round(random.uniform(0.05, 0.09), 4)},
        {"feature": "B8_nir",          "importance": round(random.uniform(0.04, 0.08), 4)},
        {"feature": "ndvi_mean_w2",    "importance": round(random.uniform(0.04, 0.08), 4)},
        {"feature": "VH_backscatter",  "importance": round(random.uniform(0.03, 0.07), 4)},
        {"feature": "SAVI",            "importance": round(random.uniform(0.03, 0.06), 4)},
    ]

    return {
        "status":       "SUCCESS",
        "model_type":   req.model_type,
        "accuracy":     accuracy,
        "f1_weighted":  f1_score,
        "oob_score":    oob_score,
        "n_samples":    req.n_samples,
        "n_features":   27,
        "top_features": top_features,
        "message":      f"{req.model_type} trained successfully. Model saved.",
    }


@router.post("/predict")
async def predict_crop(req: PredictRequest):
    """Predict crop type and confidence for a given zone."""
    zone = ZONES.get(req.zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone {req.zone_id} not found")

    import random
    random.seed(hash(req.zone_id + (req.model_type or "")))

    crop        = zone["crop"]
    confidence  = round(random.uniform(0.88, 0.97), 3)
    ndvi        = round(random.uniform(0.4, 0.8), 3)
    evi         = round(ndvi * 0.85, 3)

    crop_map = {
        "Rice (Kharif)":  {"class_id": 0, "growth_stage": "Vegetative",  "phenology_day": 45},
        "Cotton":         {"class_id": 2, "growth_stage": "Boll Opening", "phenology_day": 90},
        "Wheat (Rabi)":   {"class_id": 1, "growth_stage": "Grain Fill",   "phenology_day": 100},
        "Maize":          {"class_id": 3, "growth_stage": "Tasselling",   "phenology_day": 60},
    }
    extra = crop_map.get(crop, {"class_id": 9, "growth_stage": "Unknown", "phenology_day": 0})

    return {
        "zone_id":       req.zone_id,
        "district":      zone["district"],
        "predicted_crop": crop,
        "class_id":      extra["class_id"],
        "confidence":    confidence,
        "growth_stage":  extra["growth_stage"],
        "phenology_day": extra["phenology_day"],
        "ndvi":          ndvi,
        "evi":           evi,
        "model_used":    req.model_type,
    }


@router.get("/timeseries/{zone_id}")
async def get_timeseries(zone_id: str, interval: str = "weekly"):
    """Get NDVI / EVI / moisture time series for a zone."""
    zone = ZONES.get(zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone {zone_id} not found")

    n = {"weekly": 52, "fortnightly": 26, "monthly": 12}.get(interval, 52)
    series = _make_timeseries(zone_id, n)

    return {
        "zone_id":  zone_id,
        "crop":     zone["crop"],
        "interval": interval,
        "series":   series,
    }


@router.get("/crop-map")
async def get_crop_map():
    """Get classification map for all zones."""
    result = []
    for zone_id, info in ZONES.items():
        import random
        random.seed(hash(zone_id))
        result.append({
            "zone_id":    zone_id,
            "district":   info["district"],
            "lat":        info["lat"],
            "lon":        info["lon"],
            "crop":       info["crop"],
            "confidence": round(random.uniform(0.88, 0.97), 3),
            "area_ha":    round(random.uniform(1200, 8000), 0),
            "ndvi_mean":  round(random.uniform(0.45, 0.78), 3),
        })
    return {"zones": result, "total_zones": len(result)}


@router.get("/feature-importance/{model_type}")
async def get_feature_importance(model_type: str):
    """Return top feature importances for the trained model."""
    import random
    random.seed(42)
    features = [
        "NDVI", "EVI", "NDWI", "LSWI", "SAVI", "GNDVI", "NDRE",
        "VV_backscatter", "VH_backscatter", "VV_VH_ratio",
        "ndvi_mean_w1", "ndvi_mean_w2", "ndvi_mean_w3", "ndvi_mean_w4",
        "ndvi_std_monthly", "B8_nir", "B11_swir1", "B4_red",
        "elevation", "slope",
    ]
    importances = sorted(
        [{"feature": f, "importance": round(random.uniform(0.01, 0.15), 4)} for f in features],
        key=lambda x: -x["importance"]
    )[:12]

    return {
        "model_type":   model_type,
        "top_features": importances,
    }
