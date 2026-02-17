import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from pathlib import Path

# =========================
# PATH CONFIG
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "negotiations.csv"
MODEL_PATH = BASE_DIR / "models" / "price_model.pkl"

print("📥 Loading dataset...")
df = pd.read_csv(DATA_PATH)

# =========================
# FEATURE ENGINEERING
# =========================
df["price_ratio"] = df["offered_price"] / df["base_price"]

# =========================
# MULTI-CLASS LABELING
# =========================
def label_decision(row):
    if row["price_ratio"] >= 0.95:
        return "ACCEPTED"
    elif row["price_ratio"] >= 0.88:
        return "COUNTER"
    else:
        return "REJECTED"

df["label"] = df.apply(label_decision, axis=1)

FEATURES = [
    "base_price",
    "offered_price",
    "price_ratio",
    "trust_score",
    "attempt_number"
]

X = df[FEATURES]
y = df["label"]

# =========================
# TRAIN / TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# MODEL TRAINING (MULTI-CLASS)
# =========================
print("🤖 Training 3-class ML model...")
model = LogisticRegression(
    solver="lbfgs",
    max_iter=1000
)

model.fit(X_train, y_train)

# =========================
# EVALUATION
# =========================
y_pred = model.predict(X_test)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# =========================
# SAVE MODEL
# =========================
MODEL_PATH.parent.mkdir(exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"\n✅ Model saved at {MODEL_PATH}")
print("STEP-6.2.1 COMPLETED")
