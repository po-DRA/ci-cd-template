# ci_cd_template package
# Exposes the main model training and prediction functions.
from ci_cd_template.model import FEATURES, TARGET, train_model
from ci_cd_template.predict import predict

__all__ = ["train_model", "predict", "FEATURES", "TARGET"]
