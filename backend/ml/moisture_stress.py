"""
ml/moisture_stress.py
----------------------
Moisture Stress Detection & Irrigation Advisory Engine

Methodology:
  1. Estimate weekly crop water demand (ETc = Kc × ET₀)
  2. Compute actual evapotranspiration (ETa) from MODIS/Landsat ET product
  3. Quantify water deficit: WD = ETc - (ETa + effective rainfall)
  4. Map severity: NONE / MILD / MODERATE / SEVERE / CRITICAL
  5. Generate irrigation advisory maps (district / zone / field)

Data sources:
  - ET₀: IMD gridded weather or ERA5 reanalysis
  - Rainfall: CHIRPS / IMD gridded rainfall
  - ETa: MODIS MOD16A2 or Sentinel-2 based SEBAL
  - Kc:  FAO-56 crop coefficient tables per crop / growth stage
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# FAO-56 Crop Coefficients (Kc)
# ──────────────────────────────────────────────
#  Keys: crop name → {initial, mid, late} Kc values
KC_TABLE: Dict[str, Dict[str, float]] = {
    "Rice (Kharif)":  {"initial": 1.05, "mid": 1.20, "late": 0.90},
    "Wheat (Rabi)":   {"initial": 0.70, "mid": 1.15, "late": 0.40},
    "Cotton":         {"initial": 0.45, "mid": 1.15, "late": 0.70},
    "Maize":          {"initial": 0.30, "mid": 1.20, "late": 0.60},
    "Sugarcane":      {"initial": 0.40, "mid": 1.25, "late": 0.75},
    "Mustard":        {"initial": 0.35, "mid": 1.10, "late": 0.35},
    "Soybean":        {"initial": 0.40, "mid": 1.15, "late": 0.50},
    "Fallow":         {"initial": 0.15, "mid": 0.15, "late": 0.15},
}

# Growth stage duration (days): [initial, crop_dev, mid, late]
GROWTH_STAGES: Dict[str, List[int]] = {
    "Rice (Kharif)":  [20, 30, 60, 30],
    "Wheat (Rabi)":   [15, 25, 50, 30],
    "Cotton":         [25, 35, 50, 45],
    "Maize":          [20, 25, 40, 15],
    "Sugarcane":      [35, 60, 190, 120],
    "Mustard":        [15, 25, 35, 15],
    "Soybean":        [15, 15, 40, 15],
    "Fallow":         [0, 0, 0, 0],
}

# Stress thresholds (fraction of maximum ETc)
STRESS_LEVELS = {
    "NONE":     (0.90, 1.00),
    "MILD":     (0.75, 0.90),
    "MODERATE": (0.55, 0.75),
    "SEVERE":   (0.35, 0.55),
    "CRITICAL": (0.00, 0.35),
}

STRESS_COLORS = {
    "NONE":     "#00ff88",
    "MILD":     "#ffd700",
    "MODERATE": "#ffaa00",
    "SEVERE":   "#ff6600",
    "CRITICAL": "#ff2222",
}


# ──────────────────────────────────────────────
# Penman-Monteith ET₀ (FAO-56)
# ──────────────────────────────────────────────
def compute_et0(
    tmax: float,   # °C
    tmin: float,   # °C
    rh:   float,   # %
    wind: float,   # m/s at 2 m
    rs:   float,   # MJ m⁻² day⁻¹ solar radiation
    lat:  float,   # decimal degrees
    doy:  int,     # day of year
) -> float:
    """
    FAO-56 Penman-Monteith reference evapotranspiration [mm/day].
    """
    tmean   = (tmax + tmin) / 2.0
    elev    = 250.0               # avg Punjab elevation (m)
    P       = 101.3 * ((293 - 0.0065 * elev) / 293) ** 5.26
    gamma   = 0.000665 * P

    # Saturation / actual vapour pressure
    es_max  = 0.6108 * np.exp(17.27 * tmax / (tmax + 237.3))
    es_min  = 0.6108 * np.exp(17.27 * tmin / (tmin + 237.3))
    es      = (es_max + es_min) / 2.0
    ea      = es * rh / 100.0

    # Slope of vapour pressure curve
    delta   = 4098 * (0.6108 * np.exp(17.27 * tmean / (tmean + 237.3))) / (tmean + 237.3) ** 2

    # Net radiation (simplified)
    phi     = np.radians(lat)
    dr      = 1 + 0.033 * np.cos(2 * np.pi / 365 * doy)
    decl    = 0.409 * np.sin(2 * np.pi / 365 * doy - 1.39)
    ws      = np.arccos(-np.tan(phi) * np.tan(decl))
    Ra      = (24 * 60 / np.pi) * 0.082 * dr * (
        ws * np.sin(phi) * np.sin(decl) + np.cos(phi) * np.cos(decl) * np.sin(ws)
    )
    Rns     = (1 - 0.23) * rs
    Rnl     = 4.903e-9 * (((tmax + 273.16) ** 4 + (tmin + 273.16) ** 4) / 2) * (
        0.34 - 0.14 * np.sqrt(ea)
    ) * (1.35 * rs / (0.75 * Ra + 1e-8) - 0.35)
    Rn      = Rns - Rnl
    G       = 0.0    # soil heat flux (daily → 0)

    # ET₀
    et0 = (0.408 * delta * (Rn - G) + gamma * (900 / (tmean + 273)) * wind * (es - ea)) / (
        delta + gamma * (1 + 0.34 * wind)
    )
    return max(et0, 0.0)


# ──────────────────────────────────────────────
# Crop Water Demand (ETc) & Deficit
# ──────────────────────────────────────────────
def get_kc(crop: str, days_since_sowing: int) -> float:
    """Return interpolated Kc for current growth stage."""
    stages = GROWTH_STAGES.get(crop, [15, 25, 40, 15])
    kcs    = KC_TABLE.get(crop, {"initial": 0.5, "mid": 1.0, "late": 0.5})

    total  = sum(stages)
    if days_since_sowing >= total:
        return kcs["late"]

    # Determine stage
    cumulative = 0
    stage_names = ["initial", "initial", "mid", "late"]
    for i, dur in enumerate(stages):
        cumulative += dur
        if days_since_sowing < cumulative:
            # Linear interpolation within the stage
            start_kc = list(kcs.values())[min(i, 2)]
            end_kc   = list(kcs.values())[min(i + 1, 2)]
            frac     = (days_since_sowing - (cumulative - dur)) / max(dur, 1)
            return start_kc + frac * (end_kc - start_kc)

    return kcs["late"]


def compute_water_deficit(
    crop:              str,
    days_since_sowing: int,
    et0:               float,          # mm/day
    eta:               float,          # mm/day actual ET
    effective_rain:    float = 0.0,    # mm/day
) -> Dict:
    """
    Returns dict with ETc, water deficit, stress ratio, and stress level.
    """
    kc      = get_kc(crop, days_since_sowing)
    etc     = kc * et0                                   # crop water demand
    supply  = eta + effective_rain
    deficit = max(etc - supply, 0.0)
    ratio   = supply / (etc + 1e-8)                      # stress ratio in [0, 1]

    # Classify stress level
    stress = "NONE"
    for level, (lo, hi) in STRESS_LEVELS.items():
        if lo <= ratio < hi:
            stress = level
            break
    if ratio < 0.35:
        stress = "CRITICAL"

    return {
        "crop":              crop,
        "kc":                round(kc, 3),
        "et0":               round(et0, 2),
        "etc":               round(etc, 2),
        "eta":               round(eta, 2),
        "effective_rain":    round(effective_rain, 2),
        "water_deficit_mm":  round(deficit, 2),
        "stress_ratio":      round(ratio, 3),
        "stress_level":      stress,
        "stress_color":      STRESS_COLORS[stress],
        "irrigation_needed": deficit > 0.5,
        "irrigation_depth_mm": round(deficit * 7, 1),   # weekly depth recommendation
    }


# ──────────────────────────────────────────────
# Zone-wise Moisture Stress Map
# ──────────────────────────────────────────────
@dataclass
class ZoneMoistureReport:
    zone_id:           str
    crop:              str
    stress_level:      str
    stress_color:      str
    water_deficit_mm:  float
    etc_weekly_mm:     float
    eta_weekly_mm:     float
    irrigation_needed: bool
    irrigation_depth_mm: float
    advisory:          str
    confidence:        float
    timestamp:         str = field(default_factory=lambda: datetime.utcnow().isoformat())


def generate_zone_moisture_report(
    zone_id:           str,
    crop:              str,
    days_since_sowing: int,
    weather_records:   pd.DataFrame,   # columns: date, tmax, tmin, rh, wind, rs, rain
    eta_weekly:        float,           # mm/week from MODIS/ETa product
    lat:               float = 30.7,   # Punjab centroid
) -> ZoneMoistureReport:
    """
    Generate weekly moisture stress report for a zone.
    """
    # Aggregate daily weather to weekly ET₀
    et0_daily = []
    for _, row in weather_records.iterrows():
        doy   = pd.to_datetime(row["date"]).day_of_year
        et0_d = compute_et0(
            tmax=row["tmax"], tmin=row["tmin"],
            rh=row["rh"],   wind=row["wind"],
            rs=row["rs"],   lat=lat, doy=doy,
        )
        et0_daily.append(et0_d)

    et0_weekly      = sum(et0_daily)
    effective_rain  = weather_records["rain"].sum() * 0.8   # 80% effective
    et0_daily_mean  = et0_weekly / max(len(et0_daily), 1)

    deficit_info = compute_water_deficit(
        crop=crop,
        days_since_sowing=days_since_sowing,
        et0=et0_daily_mean,
        eta=eta_weekly / 7.0,
        effective_rain=effective_rain / 7.0,
    )

    # Advisory text
    stress  = deficit_info["stress_level"]
    deficit = deficit_info["water_deficit_mm"]
    irr_mm  = deficit_info["irrigation_depth_mm"]

    if stress == "NONE":
        advisory = f"{zone_id} — {crop} water balance is optimal. No immediate action required."
    elif stress == "MILD":
        advisory = f"{zone_id} — Mild moisture stress detected. Monitor over next 72 hrs. Consider {irr_mm:.0f} mm irrigation if no rain forecast."
    elif stress == "MODERATE":
        advisory = f"{zone_id} — Moderate deficit of {deficit:.1f} mm/day. Schedule {irr_mm:.0f} mm irrigation within 48–72 hrs."
    elif stress == "SEVERE":
        advisory = f"{zone_id} — Severe water stress! Irrigate {irr_mm:.0f} mm within 24–48 hrs to prevent yield loss."
    else:
        advisory = f"{zone_id} — CRITICAL moisture deficit ({deficit:.1f} mm/day). Immediate irrigation of {irr_mm:.0f} mm required. High yield risk."

    confidence = min(0.95, 0.75 + np.random.uniform(0, 0.20))   # placeholder; replace with model posterior

    return ZoneMoistureReport(
        zone_id=zone_id,
        crop=crop,
        stress_level=stress,
        stress_color=STRESS_COLORS[stress],
        water_deficit_mm=deficit,
        etc_weekly_mm=round(deficit_info["etc"] * 7, 1),
        eta_weekly_mm=round(eta_weekly, 1),
        irrigation_needed=deficit_info["irrigation_needed"],
        irrigation_depth_mm=irr_mm,
        advisory=advisory,
        confidence=round(confidence, 3),
    )


# ──────────────────────────────────────────────
# Multi-zone batch runner
# ──────────────────────────────────────────────
def run_district_advisory(zones_config: List[Dict]) -> List[Dict]:
    """
    Process multiple zones and return sorted advisory list.
    zones_config items must have:
        zone_id, crop, days_since_sowing, weather_df, eta_weekly, lat
    """
    reports = []
    priority_order = {"CRITICAL": 0, "SEVERE": 1, "MODERATE": 2, "MILD": 3, "NONE": 4}

    for cfg in zones_config:
        report = generate_zone_moisture_report(**cfg)
        reports.append(report)

    reports.sort(key=lambda r: priority_order.get(r.stress_level, 99))
    return [vars(r) for r in reports]
