import os
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import json
from datetime import datetime

# ---- Mock KMS utils for local testing ----
try:
    from kms_utils import encrypt_bytes, decrypt_bytes
except ImportError:
    encrypt_bytes = lambda x: x.hex()
    decrypt_bytes = lambda x: bytes.fromhex(x)

# ---- Load model ----
MODEL_PATH = os.environ.get("MODEL_PATH", "model.pkl")
model = joblib.load(MODEL_PATH)

# ---- Initialize Flask app ----
app = Flask(__name__)

# ---- Helper to prepare features ----
def prepare_features(payload):
    order = ['base_price','demand','competition_price','time_of_day','day_of_week']
    return np.array([payload.get(k, 0) for k in order]).reshape(1, -1)

# ---- Home route with UI ----
@app.route("/", methods=["GET", "POST"])
def home():
    suggested_price = None
    if request.method == "POST":
        try:
            payload = {
                "base_price": float(request.form.get("base_price", 0)),
                "demand": float(request.form.get("demand", 0)),
                "competition_price": float(request.form.get("competition_price", 0)),
                "time_of_day": float(request.form.get("time_of_day", 0)),
                "day_of_week": float(request.form.get("day_of_week", 0))
            }
            X = prepare_features(payload)
            price = float(model.predict(X)[0])
            # guard rails
            base = payload.get("base_price", price)
            price = max(price, 0.6 * base)
            price = min(price, 3.0 * base)
            suggested_price = round(price, 2)
        except Exception as e:
            suggested_price = f"Error: {e}"
    return render_template("index.html", suggested_price=suggested_price)

# ---- API route ----
@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(force=True)
    X = prepare_features(payload)
    price = float(model.predict(X)[0])
    base = payload.get('base_price', price)
    price = max(price, 0.6 * base)
    price = min(price, 3.0 * base)
    return jsonify({"suggested_price": round(price, 2)})

# ---- Run Flask app ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
