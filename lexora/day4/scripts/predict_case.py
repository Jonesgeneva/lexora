import joblib
import numpy as np
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "models"

VECTORIZER_FILE = MODEL_DIR / "tfidf_vectorizer.pkl"
MODEL_FILE = MODEL_DIR / "case_prediction_model.pkl"

# -----------------------------
# Load Model
# -----------------------------
vectorizer = joblib.load(VECTORIZER_FILE)
model = joblib.load(MODEL_FILE)

# -----------------------------
# Prediction Function
# -----------------------------
def predict_case(text):
    vec = vectorizer.transform([text])
    prob = model.predict_proba(vec)[0]

    prediction = "Convicted" if prob[1] >= 0.5 else "Acquitted"

    return prediction, prob[1]

# -----------------------------
# Explainability
# -----------------------------
def explain_prediction(text, top_n=5):
    vec = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    coefs = model.coef_[0]

    scores = vec.toarray()[0] * coefs
    top_indices = np.argsort(scores)[-top_n:][::-1]

    explanation = [(feature_names[i], round(scores[i], 3)) for i in top_indices if scores[i] > 0]
    return explanation

# -----------------------------
# CLI
# -----------------------------
if __name__ == "__main__":
    print("\n⚖️ Court Case Outcome Predictor\n")

    case_text = input("📝 Enter case facts:\n")

    result, probability = predict_case(case_text)
    explanation = explain_prediction(case_text)

    print(f"\n📊 Prediction: {result}")
    print(f"📈 Conviction Probability: {round(probability * 100, 2)}%\n")

    print("🧠 Key Influencing Words:")
    for word, score in explanation:
        print(f"  - {word} ({score})")
