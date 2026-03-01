from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict_disease

app = Flask(__name__)
# Enable CORS so our React frontend can talk to the Flask backend
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    # Note: We keep the route as /analyze to match our existing frontend code
    # and use the key 'image' instead of 'file' for consistency
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    
    try:
        result = predict_disease(file)
        return jsonify(result)
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "serving"})

import os

if __name__ == "__main__":
    # Use environment-defined port for deployment (default to 5001 locally)
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
