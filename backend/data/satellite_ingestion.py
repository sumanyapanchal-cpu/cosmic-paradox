"""
data/satellite_ingestion.py
-----------------------------
Satellite Data Acquisition Pipeline for Cosmic Paradox

Supported data sources:
  1. Bhuvan / Bhoonidhi (ISRO)  — ResourceSat-2/2A, RISAT-1, Cartosat
  2. Google Earth Engine (GEE)  — Sentinel-2, Sentinel-1, MODIS, Landsat
  3. Local GeoTIFF (GDAL)       — Pre-downloaded rasters

Key products:
  - Sentinel-2 L2A: 10m optical, cloud-masked, SR
  - Sentinel-1 GRD: 10m SAR (VV, VH), γ₀ calibrated
  - MODIS MOD13Q1: 250m NDVI/EVI 16-day composites
  - MODIS MOD16A2: 500m Actual ET 8-day
  - SRTM DEM: 30m elevation
"""

import os
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Bhoonidhi / Bhuvan API wrapper (REST)
# ──────────────────────────────────────────────
BHOONIDHI_BASE = "https://bhoonidhi.nrsc.gov.in/bhoonidhi/rest"
BHUVAN_WMS     = "https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms"

# ISRO Dataset codes for ordering via Bhoonidhi
ISRO_DATASETS = {
    "ResourceSat2_LISS3": {"sensor": "LISS3", "res_m": 23.5, "bands": ["G", "R", "NIR", "SWIR"]},
    "ResourceSat2_AWiFS":  {"sensor": "AWiFS",  "res_m": 56.0, "bands": ["G", "R", "NIR", "SWIR"]},
    "RISAT1_MRS":          {"sensor": "MRS",    "res_m": 3.0,  "bands": ["HH", "HV"]},
    "Cartosat2_PAN":       {"sensor": "PAN",    "res_m": 0.65, "bands": ["PAN"]},
}


class BhoonadhiClient:
    """
    Minimal REST client for Bhoonidhi catalog search & download.
    Register at https://bhoonidhi.nrsc.gov.in to get credentials.
    """

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self._token: Optional[str] = None
        try:
            import requests
            self._session = requests.Session()
        except ImportError:
            logger.warning("requests not installed. Run: pip install requests")
            self._session = None

    def login(self) -> bool:
        if self._session is None:
            return False
        resp = self._session.post(
            f"{BHOONIDHI_BASE}/user/login",
            json={"username": self.username, "password": self.password},
        )
        if resp.status_code == 200:
            self._token = resp.json().get("token")
            self._session.headers.update({"Authorization": f"Bearer {self._token}"})
            logger.info("Bhoonidhi login successful")
            return True
        logger.error(f"Bhoonidhi login failed: {resp.status_code}")
        return False

    def search_catalog(
        self,
        sensor:     str,
        bbox:       Tuple[float, float, float, float],  # (minlon, minlat, maxlon, maxlat)
        start_date: str,  # YYYY-MM-DD
        end_date:   str,
        cloud_pct:  int = 20,
    ) -> List[Dict]:
        """
        Search ISRO catalog for available imagery.
        Returns list of scene metadata dicts.
        """
        if self._session is None:
            return []
        payload = {
            "sensor":     sensor,
            "startDate":  start_date,
            "endDate":    end_date,
            "bbox":       list(bbox),
            "cloudCover": cloud_pct,
        }
        resp = self._session.post(f"{BHOONIDHI_BASE}/catalog/search", json=payload)
        if resp.status_code == 200:
            scenes = resp.json().get("results", [])
            logger.info(f"Found {len(scenes)} scenes for {sensor} [{start_date} → {end_date}]")
            return scenes
        return []

    def download_scene(self, scene_id: str, output_dir: str) -> Optional[str]:
        """Download a single scene by ID to output_dir. Returns local path."""
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, f"{scene_id}.tif")
        if os.path.exists(out_path):
            logger.info(f"Scene already downloaded: {out_path}")
            return out_path
        resp = self._session.get(
            f"{BHOONIDHI_BASE}/download/{scene_id}", stream=True
        )
        if resp.status_code == 200:
            with open(out_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f"Downloaded → {out_path}")
            return out_path
        logger.error(f"Download failed for scene {scene_id}: {resp.status_code}")
        return None


# ──────────────────────────────────────────────
# Google Earth Engine (GEE) Helper
# ──────────────────────────────────────────────
class GEEDataFetcher:
    """
    Google Earth Engine wrapper for automated satellite feature extraction.
    Requires: earthengine-api  (pip install earthengine-api)
              Service account or personal auth: ee.Authenticate()
    """

    def __init__(self, project_id: str = "cosmic-paradox"):
        self.project_id = project_id
        self._initialized = False
        self._init_gee()

    def _init_gee(self):
        try:
            import ee
            ee.Initialize(project=self.project_id)
            self._ee = ee
            self._initialized = True
            logger.info("GEE initialized successfully")
        except Exception as e:
            logger.warning(f"GEE not available: {e}. Install earthengine-api and authenticate.")

    def get_sentinel2_features(
        self,
        bbox:       Tuple[float, float, float, float],  # minlon, minlat, maxlon, maxlat
        start_date: str,
        end_date:   str,
        cloud_pct:  int = 20,
    ) -> Optional[Dict]:
        """
        Returns Sentinel-2 L2A median composite + vegetation indices as GEE Image.
        Cloud masking using SCL band (Scene Classification Layer).
        """
        if not self._initialized:
            return None

        ee = self._ee
        geom = ee.Geometry.BBox(*bbox)

        def mask_s2_clouds(image):
            scl = image.select("SCL")
            clear = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10))
            return image.updateMask(clear).divide(10000)

        s2 = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(geom)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_pct))
            .map(mask_s2_clouds)
            .median()
        )

        # Add vegetation indices
        ndvi  = s2.normalizedDifference(["B8", "B4"]).rename("NDVI")
        ndwi  = s2.normalizedDifference(["B8", "B11"]).rename("NDWI")
        evi   = s2.expression(
            "2.5*(NIR-RED)/(NIR+6*RED-7.5*BLUE+1)",
            {"NIR": s2.select("B8"), "RED": s2.select("B4"), "BLUE": s2.select("B2")}
        ).rename("EVI")

        composite = s2.select(["B2", "B3", "B4", "B5", "B8", "B11", "B12"]).addBands([ndvi, ndwi, evi])

        return composite

    def get_sentinel1_sar(
        self,
        bbox:       Tuple[float, float, float, float],
        start_date: str,
        end_date:   str,
    ) -> Optional[object]:
        """Sentinel-1 GRD SAR composite (VV, VH in dB)."""
        if not self._initialized:
            return None

        ee = self._ee
        geom = ee.Geometry.BBox(*bbox)

        s1 = (
            ee.ImageCollection("COPERNICUS/S1_GRD")
            .filterBounds(geom)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV"))
            .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VH"))
            .filter(ee.Filter.eq("instrumentMode", "IW"))
            .select(["VV", "VH"])
            .median()
        )
        return s1

    def get_modis_et(
        self,
        bbox:       Tuple[float, float, float, float],
        start_date: str,
        end_date:   str,
    ) -> Optional[object]:
        """MODIS MOD16A2 Actual Evapotranspiration."""
        if not self._initialized:
            return None

        ee = self._ee
        geom = ee.Geometry.BBox(*bbox)

        et = (
            ee.ImageCollection("MODIS/006/MOD16A2")
            .filterBounds(geom)
            .filterDate(start_date, end_date)
            .select("ET")
            .sum()
            .multiply(0.1)           # scale factor → mm
        )
        return et

    def export_to_drive(
        self, image, description: str, scale: int = 10, region=None
    ):
        """Export GEE image to Google Drive as GeoTIFF."""
        if not self._initialized:
            return

        ee = self._ee
        task = ee.batch.Export.image.toDrive(
            image=image,
            description=description,
            scale=scale,
            region=region,
            fileFormat="GeoTIFF",
            maxPixels=1e10,
        )
        task.start()
        logger.info(f"GEE export task started: {description}")
        return task


# ──────────────────────────────────────────────
# GDAL Raster Processing
# ──────────────────────────────────────────────
class RasterProcessor:
    """
    Local raster processing using GDAL / rasterio.
    Handles atmospheric correction, resampling, stacking, and feature extraction.
    """

    @staticmethod
    def read_raster(path: str) -> Tuple[np.ndarray, Dict]:
        """Read GeoTIFF → numpy array + metadata."""
        try:
            import rasterio
            with rasterio.open(path) as src:
                data = src.read().astype(np.float32)
                meta = {
                    "crs":       str(src.crs),
                    "transform": list(src.transform),
                    "nodata":    src.nodata,
                    "shape":     data.shape,
                }
            return data, meta
        except ImportError:
            logger.error("rasterio not installed. Run: pip install rasterio")
            return np.array([]), {}

    @staticmethod
    def apply_dos1_correction(band: np.ndarray, nodata: float = 0) -> np.ndarray:
        """
        Dark Object Subtraction (DOS-1) atmospheric correction.
        Suitable for ResourceSat / Landsat DN to surface reflectance proxy.
        """
        valid = band[band != nodata]
        if len(valid) == 0:
            return band
        dark_object = np.percentile(valid, 1)
        corrected = band - dark_object
        return np.clip(corrected, 0, None)

    @staticmethod
    def temporal_composite(
        arrays: List[np.ndarray],
        method: str = "median",
    ) -> np.ndarray:
        """
        Create temporal composite from a list of raster arrays.
        method: 'median', 'mean', 'max' (greenest pixel), 'min'
        """
        stack = np.stack(arrays, axis=0)     # (T, C, H, W)
        if method == "median":
            return np.nanmedian(stack, axis=0)
        elif method == "mean":
            return np.nanmean(stack, axis=0)
        elif method == "max":
            return np.nanmax(stack, axis=0)
        elif method == "min":
            return np.nanmin(stack, axis=0)
        return np.nanmedian(stack, axis=0)

    @staticmethod
    def extract_pixel_features(
        stack:  np.ndarray,      # (T, C, H, W)
        labels: Optional[np.ndarray] = None,  # (H, W) crop label mask
    ) -> pd.DataFrame:
        """
        Flatten raster stack into tabular feature DataFrame.
        Each row = one pixel, columns = band × time-step features.
        """
        T, C, H, W = stack.shape
        n_pixels   = H * W

        cols = {}
        for t in range(T):
            for c in range(C):
                cols[f"band{c+1}_t{t+1}"] = stack[t, c].flatten()

        df = pd.DataFrame(cols)
        if labels is not None:
            df["crop_label"] = labels.flatten()

        return df.replace([np.inf, -np.inf], np.nan).fillna(0)


# ──────────────────────────────────────────────
# Temporal Feature Builder
# ──────────────────────────────────────────────
def build_temporal_feature_matrix(
    ndvi_series:  List[Tuple[str, np.ndarray]],  # [(date_str, ndvi_2d), ...]
    window:       str = "weekly",                 # 'weekly' | 'fortnightly' | 'monthly'
) -> pd.DataFrame:
    """
    Build a multi-temporal feature table from an NDVI time series.
    Returns DataFrame with columns: date, mean_ndvi, std_ndvi, max_ndvi, min_ndvi, trend
    """
    records = []
    for date_str, ndvi_arr in ndvi_series:
        valid = ndvi_arr[(ndvi_arr > -1) & (ndvi_arr < 1) & (~np.isnan(ndvi_arr))]
        records.append({
            "date":       date_str,
            "mean_ndvi":  round(float(np.nanmean(valid)), 4) if len(valid) else np.nan,
            "std_ndvi":   round(float(np.nanstd(valid)),  4) if len(valid) else np.nan,
            "max_ndvi":   round(float(np.nanmax(valid)),  4) if len(valid) else np.nan,
            "min_ndvi":   round(float(np.nanmin(valid)),  4) if len(valid) else np.nan,
            "pct25_ndvi": round(float(np.nanpercentile(valid, 25)), 4) if len(valid) else np.nan,
            "pct75_ndvi": round(float(np.nanpercentile(valid, 75)), 4) if len(valid) else np.nan,
        })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Rolling trend (slope proxy)
    df["ndvi_trend"] = df["mean_ndvi"].diff().fillna(0)

    return df
