import pandas as pd
from sklearn.linear_model import LinearRegression

def train_model(df: pd.DataFrame, target: str):
    X = df.drop(columns=[target])
    y = df[target]
    model = LinearRegression()
    model.fit(X, y)
    return model