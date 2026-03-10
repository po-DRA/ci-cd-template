import joblib
import numpy as np

def test_prediction():
    model = joblib.load("model.joblib")
    pred = model.predict([[5]])
    assert np.isclose(pred[0], 10)