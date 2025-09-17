from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import os

app = Flask(__name__)
MODEL_PATH = "model.pkl"
SCALER_PATH = "scaler.pkl"
COLUMNS_PATH = "model_columns.pkl"

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)
    with open(COLUMNS_PATH, "rb") as f:
        feature_columns = pickle.load(f)
except FileNotFoundError:
    raise FileNotFoundError("Make sure model.pkl, scaler.pkl, and model_columns.pkl are in the same directory.")
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No input data received"}), 400

        input_data_df = pd.DataFrame([data])
        
        input_data_df = input_data_df[feature_columns]

        input_data_df[input_data_df.columns] = scaler.transform(input_data_df[input_data_df.columns])

        prediction = model.predict(input_data_df)[0]
        
        return jsonify({"prediction": float(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)