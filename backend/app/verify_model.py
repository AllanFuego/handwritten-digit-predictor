from sklearn.datasets import fetch_openml
import joblib
import numpy as np

X, y = fetch_openml(
    "mnist_784",
    version=1,
    return_X_y=True,
    as_frame=False,
    parser="pandas"
)

X = X.astype(np.float32) / 255.0

model = joblib.load("models/best_model.pkl")

pred = model.predict(X[:20])

print("Prediction :", pred)
print("Actual     :", y[:20])