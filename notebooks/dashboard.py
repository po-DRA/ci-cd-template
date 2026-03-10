import marimo as mo
import joblib

model = joblib.load("../model.joblib")

prediction = model.predict([[10]])[0]

mo.md(f"""
# Model Dashboard

Prediction for **x = 10**

**{prediction}**
""")
# To run locally : pixi run marimo run notebooks/dashboard.py