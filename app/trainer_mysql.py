import pandas as pd
import joblib
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from app.db import engine

# ============================
# 📁 PATHS
# ============================
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "price_model.pkl"

print("📥 Loading negotiation data from MySQL...")

# ============================
# 📥 LOAD DATA FROM MYSQL
# ============================
query = """
SELECT
    n.offered_price,
    p.base_price,
    u.trust_score,
    n.attempt_number,
    n.status
FROM negotiations n
JOIN products p ON p.product_id = n.product_id
JOIN users u ON u.user_id = n.user_id
WHERE n.status IN ('ACCEPTED', 'REJECTED')
"""

df = pd.read_sql(query, engine)

if df.empty:
    raise Exception("❌ No training data found")

# ============================
# 🔄 PREPROCESSING
# ============================
df["price_ratio"] = df["offered_price"] / df["base_price"]

df["label"] = df["status"].map({
    "ACCEPTED": "ACCEPTED",
    "REJECTED": "REJECTED"
})

FEATURES = [
    "base_price",
    "offered_price",
    "price_ratio",
    "trust_score",
    "attempt_number"
]

X = df[FEATURES]
y = df["label"]

# ============================
# 🧪 TRAIN / TEST SPLIT
# ============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# CLASS BALANCE CHECK
# =========================
class_counts = df["status"].value_counts()
print("\n📊 Class distribution:")
print(class_counts)

if len(class_counts) < 2:
    print("\n⚠️ Not enough class diversity to train model.")
    print("➡️ Skipping training. Existing model retained.")
    exit(0)


# ============================
# 🤖 TRAIN MODEL
# ============================
print("🤖 Training AI model from MySQL data...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)
model.fit(X_train, y_train)

# ============================
# 📊 EVALUATION
# ============================
y_pred = model.predict(X_test)
print("\n📊 Model Performance:")
print(classification_report(y_test, y_pred))

# ============================
# 💾 SAVE MODEL
# ============================
MODEL_PATH.parent.mkdir(exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"\n✅ Model retrained & saved at: {MODEL_PATH}")
print("STEP-9C COMPLETED ✅")
