import joblib
import pandas as pd
from pathlib import Path
from app.model import build_ai_response

# =========================
# PATH CONFIG
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "price_model.pkl"

# =========================
# LOAD TRAINED MODEL
# =========================
model = joblib.load(MODEL_PATH)

# =========================
# PREDICTION FUNCTION
# =========================
def predict_negotiation(
    base_price: float,
    offered_price: float,
    trust_score: float,
    attempt_number: int
):
    """
    Predict negotiation decision using trained ML model
    """

    # =========================
    # FEATURE ENGINEERING
    # =========================
    price_ratio = offered_price / base_price

    X = pd.DataFrame([{
        "base_price": base_price,
        "offered_price": offered_price,
        "price_ratio": price_ratio,
        "trust_score": trust_score,
        "attempt_number": attempt_number
    }])

    # =========================
    # MODEL INFERENCE
    # =========================
    probabilities = model.predict_proba(X)[0]
    classes = model.classes_

    best_index = probabilities.argmax()
    decision = classes[best_index]
    confidence = float(probabilities[best_index])

    # =========================
    # CENTRALIZED AI RESPONSE
    # =========================
    return build_ai_response(
        prediction=decision,
        probability=confidence,
        base_price=base_price,
        offered_price=offered_price,
        trust_score=trust_score,
        attempt_number=attempt_number
    )
