import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

df = pd.read_csv("data/data.csv")
X = df[["x"]]
y = df["y"]

model = LinearRegression().fit(X, y)
# Save the model
joblib.dump(model, "model.joblib")
print("model trained & saved !")