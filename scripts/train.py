"""Train the cardiovascular risk classifier and save it to model/model.joblib."""

import os
from pathlib import Path

import joblib
import pandas as pd

from ci_cd_template.model import TARGET, train_model

# Paths resolved relative to the project root, regardless of working directory
ROOT = Path(__file__).parent.parent
DATA_PATH = ROOT / "data" / "data.csv"
MODEL_DIR = ROOT / "model"
MODEL_PATH = MODEL_DIR / "model.joblib"

# Ensure the model output directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Load data and train
df = pd.read_csv(DATA_PATH)
model = train_model(df, target=TARGET)

# Save the trained model
joblib.dump(model, MODEL_PATH)
print(f"Model trained and saved to {MODEL_PATH}")
