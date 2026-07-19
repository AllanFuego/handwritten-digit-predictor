from pathlib import Path
import joblib

from .preprocess import preprocess_image

# ----------------------------------------------------
# Paths
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
INFO_PATH = BASE_DIR / "models" / "model_info.pkl"

# ----------------------------------------------------
# Load model
# ----------------------------------------------------

model = joblib.load(MODEL_PATH)
model_info = joblib.load(INFO_PATH)


# ----------------------------------------------------
# Prediction
# ----------------------------------------------------

def predict_digit(image_bytes):
    image = preprocess_image(image_bytes)

    prediction = int(model.predict(image)[0])

    confidence = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(image)[0]
        confidence = round(float(max(probabilities)) * 100, 2)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "model": model_info.get("model_name", "Unknown"),
        "accuracy": round(model_info.get("accuracy", 0) * 100, 2),
        "precision": round(model_info.get("precision", 0) * 100, 2),
        "recall": round(model_info.get("recall", 0) * 100, 2),
        "f1_score": round(model_info.get("f1_score", 0) * 100, 2),
    }