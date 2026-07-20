import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from xgboost import XGBRegressor


def train_model(df):

    df = df.copy()

    df["Date"] = pd.to_datetime(df["Date"])

    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()
    df["EMA20"] = df["Close"].ewm(span=20).mean()

    df.dropna(inplace=True)

    features = [
        "Open",
        "High",
        "Low",
        "Volume",
        "SMA20",
        "SMA50",
        "EMA20"
    ]

    X = df[features]
    y = df["Close"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        shuffle=False,
        test_size=0.2
    )

    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        objective="reg:squarederror",
        random_state=42
    )

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    rmse = mean_squared_error(y_test, prediction) ** 0.5
    mae = mean_absolute_error(y_test, prediction)
    r2 = r2_score(y_test, prediction)

    return (
        model,
        prediction,
        rmse,
        mae,
        r2,
        features,
        X_train,
        X_test,
        y_train,
        y_test,
        df
    )