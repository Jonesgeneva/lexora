import json
from pathlib import Path
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
MODEL_DIR = BASE_DIR.parent / "models"

DATA_FILE = DATA_DIR / "cases_processed" / "cases_ml.json"

VECTORIZER_FILE = MODEL_DIR / "tfidf_vectorizer.pkl"
MODEL_FILE = MODEL_DIR / "case_prediction_model.pkl"

MODEL_DIR.mkdir(exist_ok=True)

# -----------------------------
# Load Data
# -----------------------------
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["text"] for item in data]
labels = [item["label"] for item in data]

# -----------------------------
# Train / Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)

# -----------------------------
# TF-IDF Vectorizer
# -----------------------------
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -----------------------------
# Train Model
# -----------------------------
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_vec, y_train)

# -----------------------------
# Evaluation
# -----------------------------
preds = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, preds)

print("\n📊 Model Evaluation")
print("Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:")
print(classification_report(y_test, preds))

# -----------------------------
# Save Model & Vectorizer
# -----------------------------
joblib.dump(vectorizer, VECTORIZER_FILE)
joblib.dump(model, MODEL_FILE)

print("\n✅ Model training complete")
print(f"📁 Saved vectorizer to: {VECTORIZER_FILE}")
print(f"📁 Saved model to     : {MODEL_FILE}")
