# app.py
# Advanced Phishing Detector - Flask backend (self-contained feature extraction)
# Put rf_phishing_model.joblib in same folder before running.

from flask import Flask, render_template, request
import joblib
import pandas as pd
import re
import os

app = Flask(__name__)

MODEL_FILE = "rf_phishing_model.joblib"

# Try to load model if present
rf = None
feature_cols = None
if os.path.exists(MODEL_FILE):
    try:
        model_data = joblib.load(MODEL_FILE)
        if isinstance(model_data, dict) and "model" in model_data:
            rf = model_data["model"]
            feature_cols = model_data.get("feature_columns", None)
        else:
            rf = model_data
        print("Model loaded:", MODEL_FILE)
    except Exception as e:
        print("Failed to load model:", e)
else:
    print("Model file not found:", MODEL_FILE, "- predictions will be N/A")

# ---------------- Utility functions ----------------
def clean_url(u):
    if u is None:
        return ""
    u = str(u).strip().lower()
    u = u.strip('"').strip("'")
    # add scheme if input like example.com
    if re.match(r'^[a-z0-9\-]+\.[a-z\.]{2,}$', u) and not u.startswith('http'):
        u = "https://" + u
    if u.endswith('/'):
        u = u[:-1]
    return u

def extract_features(url):
    # lexical features used by model
    f = {}
    f['url_len'] = len(url)
    f['count_dot'] = url.count('.')
    f['count_at'] = url.count('@')
    f['count_dash'] = url.count('-')
    f['count_qmark'] = url.count('?')
    f['count_eq'] = url.count('=')
    f['count_slash'] = url.count('/')
    f['has_https'] = 1 if url.startswith('https') else 0
    f['count_digits'] = sum(ch.isdigit() for ch in url)
    suspicious_words = ['login','secure','update','verify','account','bank','confirm','webscr','signin']
    f['suspicious_words'] = sum(1 for w in suspicious_words if w in url)
    ip_match = re.search(r'http[s]?://\d+\.\d+\.\d+\.\d+', url)
    f['has_ip'] = 1 if ip_match else 0
    # placeholders for optional network features (kept for compatibility)
    f['redirect_count'] = 0
    f['final_url_len'] = 0
    f['ssl_valid'] = 0
    f['ssl_days_to_expiry'] = 0
    f['domain_created_days'] = 0
    return f

def model_predict_from_url(url):
    clean = clean_url(url)
    feats = extract_features(clean)
    X = pd.DataFrame([feats])
    # ensure columns order matches feature_cols if provided
    if feature_cols:
        for c in feature_cols:
            if c not in X.columns:
                X[c] = 0
        X = X[feature_cols]
    else:
        X = X.fillna(0)
    if rf is not None:
        try:
            label = int(rf.predict(X.values)[0])
            prob = float(rf.predict_proba(X.values)[0][1]) if hasattr(rf, "predict_proba") else None
        except Exception:
            label, prob = None, None
    else:
        label, prob = None, None
    return label, prob, feats

# ---------------- Routes ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    single = None
    error = None

    if request.method == "POST":
        raw = request.form.get("urls") or request.form.get("url")
        # accept single field or multiple urls separated by newline/comma
        url_list = []
        if raw:
            url_list = [u.strip() for u in re.split(r'[\n,]+', raw) if u.strip()]
        # limit to 50 for demo safety
        if len(url_list) > 50:
            error = "Please provide up to 50 URLs at once."
        else:
            for u in url_list:
                label, prob, feats = model_predict_from_url(u)
                results.append({
                    "input_url": u,
                    "clean_url": clean_url(u),
                    "label": label,
                    "prob": prob,
                    "features": feats
                })
        if len(results) == 1:
            single = results[0]

    return render_template("index.html", results=results, single=single, error=error)

if __name__ == "__main__":
    # For local testing only; in production use gunicorn or similar
    app.run(debug=True, host="0.0.0.0", port=5000)