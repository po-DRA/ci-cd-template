from pathlib import Path

import joblib
import pandas as pd

from ci_cd_template.model import FEATURES, classify_risk

# Default path to the saved model, relative to the project root
MODEL_PATH = Path(__file__).parent.parent.parent / "model" / "model.joblib"


def predict(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }
