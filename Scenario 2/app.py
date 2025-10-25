# app.py
from flask import Flask, request, jsonify
from ai_model import SimpleAIModel

app = Flask(__name__)
model = SimpleAIModel()

@app.route('/')
def home():
    return "🤖 Simple AI Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        value = float(data.get("input"))
        result = model.predict(value)
        return jsonify({"input": value, "prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
