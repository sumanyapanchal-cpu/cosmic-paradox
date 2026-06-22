"""
ml/deep_models.py
------------------
Deep Learning Models for Cosmic Paradox:

1. TemporalLSTM   — LSTM for crop phenology / time-series dynamics
                    Input: (batch, time_steps, n_features)
                    Output: crop class logits

2. TemporalCNN    — 1-D Temporal CNN (faster than LSTM, competitive accuracy)
                    Input: (batch, time_steps, n_features)

3. MiniUNet       — Lightweight U-Net for pixel-wise spatial classification
                    Input: (batch, C, H, W) — multi-band raster patch
                    Output: (batch, n_classes, H, W) segmentation mask

Framework: PyTorch  (TensorFlow alternative provided as comments)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np
import logging
from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 1.  LSTM Temporal Crop Classifier
# ──────────────────────────────────────────────
class TemporalLSTM(nn.Module):
    """
    Bidirectional LSTM for multitemporal satellite time-series classification.

    Architecture:
        Input → BiLSTM (2 layers) → Attention Pool → FC → Softmax

    Input shape : (batch, T, F)
                  T = number of time steps  (e.g., 52 weeks)
                  F = number of features per step (spectral + VI + SAR)
    """

    def __init__(
        self,
        input_size:  int = 20,     # features per time step
        hidden_size: int = 128,
        num_layers:  int = 2,
        num_classes: int = 10,
        dropout:     float = 0.3,
    ):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        lstm_out_size = hidden_size * 2   # bidirectional doubles dim

        # Temporal attention
        self.attention = nn.Sequential(
            nn.Linear(lstm_out_size, 64),
            nn.Tanh(),
            nn.Linear(64, 1),
        )

        self.classifier = nn.Sequential(
            nn.Linear(lstm_out_size, 256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, T, F)
        lstm_out, _ = self.lstm(x)                  # (B, T, 2H)
        attn_w = F.softmax(self.attention(lstm_out), dim=1)  # (B, T, 1)
        ctx    = (attn_w * lstm_out).sum(dim=1)     # (B, 2H)
        return self.classifier(ctx)                 # (B, n_classes)


# ──────────────────────────────────────────────
# 2.  Temporal CNN
# ──────────────────────────────────────────────
class TemporalCNN(nn.Module):
    """
    1-D Convolutional network for crop time-series.
    Faster to train than LSTM; good for fortnightly/monthly composites.

    Input : (batch, F, T)  — channels first for Conv1d
    """

    def __init__(
        self,
        in_channels: int = 20,
        num_classes: int = 10,
        dropout:     float = 0.3,
    ):
        super().__init__()
        self.encoder = nn.Sequential(
            # block 1
            nn.Conv1d(in_channels, 64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Conv1d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(2),

            # block 2
            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Conv1d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),   # global average pool
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, F, T)
        return self.classifier(self.encoder(x))


# ──────────────────────────────────────────────
# 3.  Mini U-Net — Spatial Segmentation
# ──────────────────────────────────────────────
class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.block(x)


class MiniUNet(nn.Module):
    """
    Lightweight U-Net for pixel-wise crop segmentation.

    Input : (B, C, H, W)
            C = number of satellite bands / composited indices
            H, W = patch size (e.g., 64×64 pixels @ 10m → 640m)
    Output: (B, n_classes, H, W)

    Recommended patch size: 128×128 or 256×256
    """

    def __init__(self, in_channels: int = 12, num_classes: int = 10):
        super().__init__()
        # Encoder
        self.enc1 = DoubleConv(in_channels, 64)
        self.enc2 = DoubleConv(64, 128)
        self.enc3 = DoubleConv(128, 256)
        self.pool  = nn.MaxPool2d(2)

        # Bottleneck
        self.bottleneck = DoubleConv(256, 512)

        # Decoder
        self.up3    = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.dec3   = DoubleConv(512, 256)
        self.up2    = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.dec2   = DoubleConv(256, 128)
        self.up1    = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec1   = DoubleConv(128, 64)

        self.head   = nn.Conv2d(64, num_classes, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Encode
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))

        # Bottleneck
        b  = self.bottleneck(self.pool(e3))

        # Decode
        d3 = self.dec3(torch.cat([self.up3(b),  e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))

        return self.head(d1)   # (B, n_classes, H, W)


# ──────────────────────────────────────────────
# Dataset Wrappers
# ──────────────────────────────────────────────
class TimeSeriesDataset(Dataset):
    """
    Dataset for temporal crop classification.
    Each sample: (T, F) time-series → class label
    """
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class PatchDataset(Dataset):
    """
    Dataset for U-Net spatial segmentation.
    Each sample: (C, H, W) raster patch → (H, W) label mask
    """
    def __init__(self, patches: np.ndarray, masks: np.ndarray):
        self.patches = torch.tensor(patches, dtype=torch.float32)
        self.masks   = torch.tensor(masks,   dtype=torch.long)

    def __len__(self):
        return len(self.masks)

    def __getitem__(self, idx):
        return self.patches[idx], self.masks[idx]


# ──────────────────────────────────────────────
# Generic Training Loop
# ──────────────────────────────────────────────
def train_model(
    model:       nn.Module,
    train_loader: DataLoader,
    val_loader:   DataLoader,
    epochs:       int = 30,
    lr:           float = 1e-3,
    device:       str = "cuda" if torch.cuda.is_available() else "cpu",
) -> Dict[str, list]:
    """
    Train any classification / segmentation model.
    Returns loss/accuracy history for dashboard plotting.
    """
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.OneCycleLR(
        optimizer, max_lr=lr, epochs=epochs, steps_per_epoch=len(train_loader)
    )
    criterion = nn.CrossEntropyLoss()

    history: Dict[str, list] = {"train_loss": [], "val_loss": [], "val_acc": []}

    for epoch in range(1, epochs + 1):
        # ── Train ──
        model.train()
        running_loss = 0.0
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            logits = model(xb)
            loss   = criterion(logits, yb)
            loss.backward()
            optimizer.step()
            scheduler.step()
            running_loss += loss.item()

        train_loss = running_loss / len(train_loader)

        # ── Validate ──
        model.eval()
        val_loss_sum, correct, total = 0.0, 0, 0
        with torch.no_grad():
            for xb, yb in val_loader:
                xb, yb = xb.to(device), yb.to(device)
                logits  = model(xb)
                val_loss_sum += criterion(logits, yb).item()
                preds    = logits.argmax(dim=1)
                correct += (preds == yb).sum().item()
                total   += yb.numel()

        val_loss = val_loss_sum / len(val_loader)
        val_acc  = correct / total

        history["train_loss"].append(round(train_loss, 4))
        history["val_loss"].append(round(val_loss, 4))
        history["val_acc"].append(round(val_acc, 4))

        if epoch % 5 == 0 or epoch == 1:
            logger.info(
                f"Epoch {epoch:3d}/{epochs} | "
                f"train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_acc={val_acc:.4f}"
            )

    return history


def save_torch_model(model: nn.Module, path: str):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save(model.state_dict(), path)
    logger.info(f"PyTorch model saved → {path}")


def load_torch_model(model: nn.Module, path: str, device: str = "cpu") -> nn.Module:
    model.load_state_dict(torch.load(path, map_location=device))
    model.eval()
    return model
