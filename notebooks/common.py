"""Shared helpers so every notebook uses identical data, features and metrics."""
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
DATA, PROC, MODELS, RESULTS = ROOT/"dataset", ROOT/"dataset"/"processed", ROOT/"models", ROOT/"results"
SEED = 42
CAT = ["Brand", "Model", "Gear", "Fuel Type", "Town"]
NUM = ["YOM", "Engine", "Mileage", "Leasing", "IsNew", "AC", "PS", "PM", "PW"]

def load_split(name):
    """Returns (features DataFrame, log1p(price) Series) for 'train' | 'val' | 'test'."""
    d = pd.read_csv(PROC/f"{name}.csv")
    return d[CAT + NUM], d["log_price"]

def evaluate(y_log_true, y_log_pred):
    """Metrics in ORIGINAL price units (units of LKR 100,000); models are trained on log1p(price)."""
    t, p = np.expm1(np.asarray(y_log_true)), np.expm1(np.asarray(y_log_pred))
    mse = mean_squared_error(t, p)
    return {"MAE": mean_absolute_error(t, p), "MSE": mse, "RMSE": mse**.5, "R2": r2_score(t, p)}
