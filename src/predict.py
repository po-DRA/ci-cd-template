import joblib

def predict(x):
    # Load the model you trained earlier
    model = joblib.load("model/model.joblib")
    return model.predict([[x]])[0]