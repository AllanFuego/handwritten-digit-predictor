from pathlib import Path
import joblib
import requests  # Add this import
from .preprocess import preprocess_image

# ----------------------------------------------------
# Paths
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
INFO_PATH = BASE_DIR / "models" / "model_info.pkl"

# ----------------------------------------------------
# Add this function to download model
# ----------------------------------------------------

def download_if_missing():
    """Download model from Hugging Face if not found locally"""
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Only download if model doesn't exist
    if not MODEL_PATH.exists():
        print("📥 Downloading model from Hugging Face (308 MB)...")
        url = "https://huggingface.co/allanfuego/handwritten-predictor/resolve/main/best_model.pkl"
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(MODEL_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("✅ Model downloaded!")
    
    # Also download info if missing
    if not INFO_PATH.exists():
        print("📥 Downloading model info...")
        url = "https://huggingface.co/allanfuego/handwritten-predictor/resolve/main/model_info.pkl"
        response = requests.get(url)
        response.raise_for_status()
        with open(INFO_PATH, "wb") as f:
            f.write(response.content)
        print("✅ Model info downloaded!")

# ----------------------------------------------------
# Load model - Only change this part
# ----------------------------------------------------

# Try to download if files are missing
download_if_missing()

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