"""
api/routers/advisory_router.py
--------------------------------
Irrigation advisory and moisture stress endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import random
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

STRESS_MAP = {
    "PB-01": {"crop": "Rice (Kharif)", "stress": "NONE",     "deficit": 0.0,  "irr_mm": 0},
    "PB-02": {"crop": "Cotton",        "stress": "MODERATE", "deficit": 2.1,  "irr_mm": 14},
    "PB-03": {"crop": "Wheat (Rabi)",  "stress": "SEVERE",   "deficit": 3.8,  "irr_mm": 27},
    "PB-04": {"crop": "Maize",         "stress": "CRITICAL", "deficit": 5.2,  "irr_mm": 36},
}

STRESS_COLORS = {
    "NONE": "#00ff88", "MILD": "#ffd700",
    "MODERATE": "#ffaa00", "SEVERE": "#ff6600", "CRITICAL": "#ff2222",
}


@router.get("/moisture-map")
async def get_moisture_map():
    """Return moisture stress for all zones."""
    zones = []
    for zone_id, info in STRESS_MAP.items():
        zones.append({
            "zone_id":           zone_id,
            "crop":              info["crop"],
            "stress_level":      info["stress"],
            "stress_color":      STRESS_COLORS[info["stress"]],
            "water_deficit_mm":  info["deficit"],
            "irrigation_depth_mm": info["irr_mm"],
            "et0_weekly_mm":     round(random.uniform(22, 35), 1),
            "etc_weekly_mm":     round(random.uniform(25, 42), 1),
            "eta_weekly_mm":     round(random.uniform(15, 35), 1),
            "irrigation_needed": info["irr_mm"] > 0,
        })
    return {"zones": zones}


@router.get("/advisory/{zone_id}")
async def get_advisory(zone_id: str):
    """Get full irrigation advisory for a zone."""
    info = STRESS_MAP.get(zone_id)
    if not info:
        raise HTTPException(status_code=404, detail=f"Zone {zone_id} not found")

    stress   = info["stress"]
    crop     = info["crop"]
    deficit  = info["deficit"]
    irr_mm   = info["irr_mm"]

    texts = {
        "NONE":     f"{crop} water balance is optimal. No immediate action required.",
        "MILD":     f"Mild moisture stress in {crop}. Monitor over next 72 hrs. Schedule {irr_mm} mm if no rain.",
        "MODERATE": f"Moderate deficit {deficit:.1f} mm/day in {crop}. Irrigate {irr_mm} mm within 48–72 hrs.",
        "SEVERE":   f"Severe water stress in {crop}! Irrigate {irr_mm} mm within 24–48 hrs to prevent yield loss.",
        "CRITICAL": f"CRITICAL deficit in {crop} ({deficit:.1f} mm/day). Immediate {irr_mm} mm irrigation required!",
    }

    random.seed(hash(zone_id))
    return {
        "zone_id":             zone_id,
        "crop":                crop,
        "stress_level":        stress,
        "stress_color":        STRESS_COLORS[stress],
        "water_deficit_mm":    deficit,
        "irrigation_depth_mm": irr_mm,
        "advisory_text":       texts[stress],
        "confidence":          round(random.uniform(0.87, 0.97), 3),
        "kc":                  round(random.uniform(0.8, 1.2), 2),
        "et0_daily_mm":        round(random.uniform(3.2, 5.8), 2),
        "etc_daily_mm":        round(random.uniform(3.5, 7.0), 2),
        "eta_daily_mm":        round(random.uniform(1.5, 5.0), 2),
        "effective_rain_mm":   round(random.uniform(0, 5), 2),
    }


@router.get("/weekly-demand")
async def get_weekly_demand():
    """District-wide weekly crop water demand summary."""
    data = []
    crops = ["Rice (Kharif)", "Cotton", "Wheat (Rabi)", "Maize"]
    for i, crop in enumerate(crops):
        random.seed(i * 99)
        data.append({
            "crop":           crop,
            "etc_weekly_mm":  round(random.uniform(25, 55), 1),
            "eta_weekly_mm":  round(random.uniform(15, 45), 1),
            "deficit_mm":     round(random.uniform(0, 20), 1),
            "area_1000_ha":   round(random.uniform(50, 500), 1),
            "total_demand_mm3": round(random.uniform(100, 2000), 0),
        })
    return {"weekly_demand": data}
