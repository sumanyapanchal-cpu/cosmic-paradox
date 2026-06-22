"""
ml/crop_classifier.py
----------------------
Multitemporal Crop Classification using Random Forest & XGBoost.

Inputs  : Tabular feature vectors built from:
          - Optical bands (Sentinel-2 / Resourcesat-2 via Bhuvan/Bhoonidhi)
          - SAR backscatter (Sentinel-1 / RISAT-1)
          - Vegetation indices: NDVI, NDWI, EVI, SAVI, LSWI
          - Temporal composites: weekly / fortnightly / monthly
          - DEM derivatives: slope, aspect (SRTM)

Outputs : Crop type label per pixel/parcel, confidence score, feature importance map
"""

import numpy as np
import pandas as pd
import joblib
import os
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, f1_score
)
from sklearn.pipeline import Pipeline
import xgboost as xgb

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# CROP LABEL MAP  (ISRO / Bhuvan standard)
# ─────────────────────────────────────────────
CROP_LABELS = {
    0: "Rice (Kharif)",
    1: "Wheat (Rabi)",
    2: "Cotton",
    3: "Maize",
    4: "Sugarcane",
    5: "Mustard",
    6: "Soybean",
    7: "Fallow",
    8: "Orchard",
    9: "Water Body",
}

# ─────────────────────────────────────────────
# FEATURE COLUMNS
# ─────────────────────────────────────────────
SPECTRAL_FEATURES = [
    "B2_blue", "B3_green", "B4_red", "B5_rededge",
    "B8_nir", "B11_swir1", "B12_swir2"
]

VEGETATION_INDICES = [
    "NDVI", "NDWI", "EVI", "SAVI", "LSWI",
    "RVI", "GNDVI", "NDRE"
]

SAR_FEATURES = [
    "VV_backscatter", "VH_backscatter", "VV_VH_ratio",
    "SAR_NDVI"           # (VV - VH) / (VV + VH)
]

TEMPORAL_STATS = [
    "ndvi_mean_w1", "ndvi_mean_w2", "ndvi_mean_w3", "ndvi_mean_w4",
    "ndvi_std_monthly", "ndvi_max_monthly", "ndvi_min_monthly",
    "evi_mean_monthly", "lswi_mean_monthly",
]

DEM_FEATURES = ["elevation", "slope", "aspect"]

ALL_FEATURES = (
    SPECTRAL_FEATURES + VEGETATION_INDICES +
    SAR_FEATURES + TEMPORAL_STATS + DEM_FEATURES
)


# ─────────────────────────────────────────────
# VEGETATION INDEX COMPUTATION
# ─────────────────────────────────────────────
def compute_vegetation_indices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute standard vegetation / water indices from Sentinel-2 bands.
    All band values should be in [0, 1] (surface reflectance).
    """
    eps = 1e-8  # avoid divide-by-zero

    df = df.copy()

    # NDVI  – Normalized Difference Vegetation Index
    df["NDVI"]  = (df["B8_nir"] - df["B4_red"]) / (df["B8_nir"] + df["B4_red"] + eps)

    # NDWI  – Normalized Difference Water Index (Gao 1996)
    df["NDWI"]  = (df["B8_nir"] - df["B11_swir1"]) / (df["B8_nir"] + df["B11_swir1"] + eps)

    # EVI   – Enhanced Vegetation Index
    df["EVI"]   = 2.5 * (df["B8_nir"] - df["B4_red"]) / (
        df["B8_nir"] + 6 * df["B4_red"] - 7.5 * df["B2_blue"] + 1 + eps
    )

    # SAVI  – Soil Adjusted Vegetation Index (L=0.5)
    L = 0.5
    df["SAVI"]  = ((df["B8_nir"] - df["B4_red"]) / (
        df["B8_nir"] + df["B4_red"] + L + eps
    )) * (1 + L)

    # LSWI  – Land Surface Water Index
    df["LSWI"]  = (df["B8_nir"] - df["B11_swir1"]) / (df["B8_nir"] + df["B11_swir1"] + eps)

    # RVI   – Ratio Vegetation Index
    df["RVI"]   = df["B8_nir"] / (df["B4_red"] + eps)

    # GNDVI – Green NDVI
    df["GNDVI"] = (df["B8_nir"] - df["B3_green"]) / (df["B8_nir"] + df["B3_green"] + eps)

    # NDRE  – Red Edge NDVI
    df["NDRE"]  = (df["B8_nir"] - df["B5_rededge"]) / (df["B8_nir"] + df["B5_rededge"] + eps)

    # SAR NDVI proxy
    if "VV_backscatter" in df.columns and "VH_backscatter" in df.columns:
        df["VV_VH_ratio"] = df["VV_backscatter"] / (df["VH_backscatter"] + eps)
        df["SAR_NDVI"]    = (df["VV_backscatter"] - df["VH_backscatter"]) / (
            df["VV_backscatter"] + df["VH_backscatter"] + eps
        )

    return df


# ─────────────────────────────────────────────
# RANDOM FOREST TRAINER
# ─────────────────────────────────────────────
class RandomForestCropClassifier:
    """
    Supervised crop-type classification using Random Forest.
    Designed for Punjab agri-zones (PB-01 … PB-04+).
    """

    def __init__(
        self,
        n_estimators: int = 300,
        max_depth: int = 20,
        n_jobs: int = -1,
        random_state: int = 42,
    ):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features="sqrt",
            class_weight="balanced",   # handles class imbalance
            oob_score=True,
            n_jobs=n_jobs,
            random_state=random_state,
        )
        self.scaler      = StandardScaler()
        self.label_enc   = LabelEncoder()
        self.feature_names: List[str] = []
        self.is_trained  = False

    def preprocess(self, df: pd.DataFrame) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        df = compute_vegetation_indices(df)
        available = [f for f in ALL_FEATURES if f in df.columns]
        self.feature_names = available
        X = df[available].fillna(0).values

        y = None
        if "crop_label" in df.columns:
            y = self.label_enc.fit_transform(df["crop_label"])

        return X, y

    def train(self, df: pd.DataFrame) -> Dict[str, Any]:
        logger.info("Training Random Forest Crop Classifier …")
        X, y = self.preprocess(df)
        X_scaled = self.scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, stratify=y, random_state=42
        )

        self.model.fit(X_train, y_train)
        self.is_trained = True

        y_pred = self.model.predict(X_test)
        acc    = accuracy_score(y_test, y_pred)
        f1     = f1_score(y_test, y_pred, average="weighted")
        oob    = self.model.oob_score_

        report = classification_report(
            y_test, y_pred,
            target_names=[CROP_LABELS.get(i, str(i)) for i in self.label_enc.classes_],
            output_dict=True
        )

        importances = dict(
            zip(self.feature_names, self.model.feature_importances_.tolist())
        )
        top_features = sorted(importances.items(), key=lambda x: -x[1])[:10]

        logger.info(f"RF Training complete | Accuracy={acc:.4f} | F1={f1:.4f} | OOB={oob:.4f}")

        return {
            "model_type":        "RandomForest",
            "accuracy":          round(acc, 4),
            "f1_weighted":       round(f1, 4),
            "oob_score":         round(oob, 4),
            "n_features":        len(self.feature_names),
            "top_features":      top_features,
            "classification_report": report,
            "trained_at":        datetime.utcnow().isoformat(),
        }

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.is_trained:
            raise RuntimeError("Model not trained. Call train() first.")

        df = compute_vegetation_indices(df)
        available = [f for f in self.feature_names if f in df.columns]
        X = df[available].fillna(0).values
        X_scaled = self.scaler.transform(X)

        preds      = self.model.predict(X_scaled)
        proba      = self.model.predict_proba(X_scaled)
        confidence = proba.max(axis=1)

        df = df.copy()
        df["predicted_class"]  = preds
        df["predicted_crop"]   = [CROP_LABELS.get(int(p), "Unknown") for p in
                                   self.label_enc.inverse_transform(preds)]
        df["confidence"]       = confidence
        return df

    def save(self, path: str = "models/rf_crop_classifier.pkl"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(
            {
                "model":     self.model,
                "scaler":    self.scaler,
                "label_enc": self.label_enc,
                "features":  self.feature_names,
            },
            path
        )
        logger.info(f"Model saved → {path}")

    @classmethod
    def load(cls, path: str = "models/rf_crop_classifier.pkl") -> "RandomForestCropClassifier":
        obj = cls()
        data = joblib.load(path)
        obj.model        = data["model"]
        obj.scaler       = data["scaler"]
        obj.label_enc    = data["label_enc"]
        obj.feature_names = data["features"]
        obj.is_trained   = True
        return obj


# ─────────────────────────────────────────────
# XGBOOST TRAINER
# ─────────────────────────────────────────────
class XGBoostCropClassifier:
    """
    XGBoost-based multitemporal crop classification.
    Often outperforms RF on imbalanced agri datasets.
    """

    def __init__(self, n_estimators: int = 500, max_depth: int = 6):
        self.params = dict(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            use_label_encoder=False,
            eval_metric="mlogloss",
            tree_method="hist",
            random_state=42,
        )
        self.model     = None
        self.scaler    = StandardScaler()
        self.label_enc = LabelEncoder()
        self.feature_names: List[str] = []
        self.is_trained = False

    def preprocess(self, df: pd.DataFrame) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        df = compute_vegetation_indices(df)
        available = [f for f in ALL_FEATURES if f in df.columns]
        self.feature_names = available
        X = df[available].fillna(0).values
        y = None
        if "crop_label" in df.columns:
            y = self.label_enc.fit_transform(df["crop_label"])
        return X, y

    def train(self, df: pd.DataFrame) -> Dict[str, Any]:
        logger.info("Training XGBoost Crop Classifier …")
        X, y = self.preprocess(df)
        X_scaled = self.scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, stratify=y, random_state=42
        )

        n_classes = len(np.unique(y))
        self.model = xgb.XGBClassifier(
            **self.params,
            num_class=n_classes,
            objective="multi:softprob",
        )
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False,
        )
        self.is_trained = True

        y_pred = self.model.predict(X_test)
        acc    = accuracy_score(y_test, y_pred)
        f1     = f1_score(y_test, y_pred, average="weighted")

        importances = dict(zip(self.feature_names, self.model.feature_importances_.tolist()))
        top_features = sorted(importances.items(), key=lambda x: -x[1])[:10]

        logger.info(f"XGB Training complete | Accuracy={acc:.4f} | F1={f1:.4f}")

        return {
            "model_type":   "XGBoost",
            "accuracy":     round(acc, 4),
            "f1_weighted":  round(f1, 4),
            "n_features":   len(self.feature_names),
            "top_features": top_features,
            "trained_at":   datetime.utcnow().isoformat(),
        }

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.is_trained:
            raise RuntimeError("Model not trained.")
        df = compute_vegetation_indices(df)
        available = [f for f in self.feature_names if f in df.columns]
        X = df[available].fillna(0).values
        X_scaled = self.scaler.transform(X)
        preds      = self.model.predict(X_scaled)
        proba      = self.model.predict_proba(X_scaled)
        confidence = proba.max(axis=1)

        df = df.copy()
        df["predicted_class"] = preds
        df["predicted_crop"]  = [CROP_LABELS.get(int(p), "Unknown") for p in
                                  self.label_enc.inverse_transform(preds)]
        df["confidence"]      = confidence
        return df

    def save(self, path: str = "models/xgb_crop_classifier.pkl"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(
            {
                "model":     self.model,
                "scaler":    self.scaler,
                "label_enc": self.label_enc,
                "features":  self.feature_names,
            },
            path
        )

    @classmethod
    def load(cls, path: str = "models/xgb_crop_classifier.pkl") -> "XGBoostCropClassifier":
        obj = cls()
        data = joblib.load(path)
        obj.model        = data["model"]
        obj.scaler       = data["scaler"]
        obj.label_enc    = data["label_enc"]
        obj.feature_names = data["features"]
        obj.is_trained   = True
        return obj
