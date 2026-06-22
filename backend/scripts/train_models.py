"""
scripts/train_models.py
------------------------
Standalone training script for all Cosmic Paradox ML models.
Run: python -m scripts.train_models --model all --samples 10000

Steps:
  1. Load / simulate labeled satellite feature data
  2. Compute vegetation indices
  3. Train RF + XGBoost crop classifiers
  4. Train LSTM / TemporalCNN for time-series
  5. Print metrics & save models to ./models/
"""

import argparse
import sys
import os
import logging
import numpy as np
import pandas as pd

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ml.crop_classifier import RandomForestCropClassifier, XGBoostCropClassifier, CROP_LABELS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("train_script")


# ──────────────────────────────────────────────
# Synthetic labeled dataset generator
# ──────────────────────────────────────────────
def generate_training_data(n_samples: int = 10000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic Sentinel-2 + SAR + temporal feature dataset.

    In production, replace with:
      - GEE-exported CSV of labeled pixels (ground-truth from field surveys)
      - Bhoonidhi ResourceSat-2 patches with ISRO crop mask labels
    """
    np.random.seed(seed)
    n_classes = len(CROP_LABELS)
    labels    = np.random.choice(list(range(n_classes)), size=n_samples)

    records = []
    for lbl in labels:
        # Class-specific spectral signature offsets
        nir   = np.random.uniform(0.3, 0.75) + lbl * 0.02
        red   = np.random.uniform(0.04, 0.12)
        blue  = np.random.uniform(0.03, 0.08)
        green = np.random.uniform(0.06, 0.15)
        re    = (nir + red) / 2 + np.random.normal(0, 0.01)
        swir1 = nir * np.random.uniform(0.4, 0.7)
        swir2 = swir1 * np.random.uniform(0.5, 0.85)
        vv    = -10 + lbl * 0.4 + np.random.normal(0, 1.5)
        vh    = -17 + lbl * 0.3 + np.random.normal(0, 1.5)

        base_ndvi = (nir - red) / (nir + red + 1e-8)

        records.append({
            # Spectral bands
            "B2_blue": blue, "B3_green": green, "B4_red": red,
            "B5_rededge": re, "B8_nir": nir,
            "B11_swir1": swir1, "B12_swir2": swir2,

            # SAR
            "VV_backscatter": vv, "VH_backscatter": vh,

            # Temporal NDVI stats
            "ndvi_mean_w1": base_ndvi + np.random.normal(0, 0.04),
            "ndvi_mean_w2": base_ndvi + np.random.normal(0, 0.04),
            "ndvi_mean_w3": base_ndvi * 1.1 + np.random.normal(0, 0.03),
            "ndvi_mean_w4": base_ndvi * 0.95 + np.random.normal(0, 0.04),
            "ndvi_std_monthly": abs(np.random.normal(0.05, 0.02)),
            "ndvi_max_monthly": base_ndvi + 0.15,
            "ndvi_min_monthly": base_ndvi - 0.10,
            "evi_mean_monthly": base_ndvi * 0.85,
            "lswi_mean_monthly": -0.1 + lbl * 0.03 + np.random.normal(0, 0.04),

            # DEM
            "elevation": np.random.uniform(180, 400),
            "slope":     np.random.uniform(0, 8),
            "aspect":    np.random.uniform(0, 360),

            # Label
            "crop_label": lbl,
        })

    df = pd.DataFrame(records)
    logger.info(f"Generated {len(df)} training samples across {n_classes} classes")
    return df


# ──────────────────────────────────────────────
# Training runners
# ──────────────────────────────────────────────
def train_random_forest(df: pd.DataFrame):
    logger.info("=" * 55)
    logger.info("TRAINING: Random Forest Crop Classifier")
    logger.info("=" * 55)

    clf = RandomForestCropClassifier(n_estimators=300, max_depth=20)
    metrics = clf.train(df)

    print(f"\n  Accuracy   : {metrics['accuracy']:.4f}")
    print(f"  F1 (wtd)   : {metrics['f1_weighted']:.4f}")
    print(f"  OOB Score  : {metrics['oob_score']:.4f}")
    print(f"  Features   : {metrics['n_features']}")
    print("\n  Top features:")
    for feat, imp in metrics["top_features"][:5]:
        print(f"    {feat:<22} {imp:.4f}")

    clf.save("models/rf_crop_classifier.pkl")
    return metrics


def train_xgboost(df: pd.DataFrame):
    logger.info("=" * 55)
    logger.info("TRAINING: XGBoost Crop Classifier")
    logger.info("=" * 55)

    clf = XGBoostCropClassifier(n_estimators=500, max_depth=6)
    metrics = clf.train(df)

    print(f"\n  Accuracy  : {metrics['accuracy']:.4f}")
    print(f"  F1 (wtd)  : {metrics['f1_weighted']:.4f}")
    print("\n  Top features:")
    for feat, imp in metrics["top_features"][:5]:
        print(f"    {feat:<22} {imp:.4f}")

    clf.save("models/xgb_crop_classifier.pkl")
    return metrics


def train_lstm_demo():
    """Demo LSTM training on synthetic time-series data."""
    try:
        import torch
        from ml.deep_models import TemporalLSTM, TimeSeriesDataset, train_model
        from torch.utils.data import DataLoader, random_split

        logger.info("=" * 55)
        logger.info("TRAINING: LSTM Temporal Classifier (demo)")
        logger.info("=" * 55)

        N, T, F = 2000, 52, 15    # samples, time steps, features per step
        X = np.random.randn(N, T, F).astype(np.float32)
        y = np.random.randint(0, 10, N)

        dataset = TimeSeriesDataset(X, y)
        n_val   = int(0.2 * N)
        train_ds, val_ds = random_split(dataset, [N - n_val, n_val])

        train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
        val_loader   = DataLoader(val_ds,   batch_size=64)

        model = TemporalLSTM(input_size=F, hidden_size=128, num_layers=2, num_classes=10)
        history = train_model(model, train_loader, val_loader, epochs=10, lr=1e-3)

        print(f"\n  Final val_acc  : {history['val_acc'][-1]:.4f}")
        print(f"  Final val_loss : {history['val_loss'][-1]:.4f}")

        os.makedirs("models", exist_ok=True)
        torch.save(model.state_dict(), "models/lstm_temporal.pt")
        logger.info("LSTM model saved → models/lstm_temporal.pt")

    except ImportError as e:
        logger.warning(f"PyTorch not available, skipping LSTM demo: {e}")


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Cosmic Paradox ML models")
    parser.add_argument("--model",   default="all",  choices=["all", "rf", "xgb", "lstm"])
    parser.add_argument("--samples", default=8000,   type=int)
    parser.add_argument("--seed",    default=42,     type=int)
    args = parser.parse_args()

    logger.info(f"Generating {args.samples} training samples (seed={args.seed}) …")
    df = generate_training_data(n_samples=args.samples, seed=args.seed)

    if args.model in ("all", "rf"):
        train_random_forest(df)

    if args.model in ("all", "xgb"):
        train_xgboost(df)

    if args.model in ("all", "lstm"):
        train_lstm_demo()

    logger.info("\nAll requested models trained successfully.")
