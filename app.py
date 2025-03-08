from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('model.pkl')

# Define categorical mappings (ensure they match your model training)
categories = {
    "WindGustDir": ['N', 'S', 'E', 'W'],  # Example values (update with actual ones)
    "WindDir9am": ['N', 'S', 'E', 'W'],
    "WindDir3pm": ['N', 'S', 'E', 'W'],
    "Location": ['Sydney', 'Melbourne', 'Brisbane'],  # Example values
    "RainToday": {'No': 0, 'Yes': 1}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Handle categorical encoding
    try:
        input_features = [
            categories['Location'].index(data['Location']) if data['Location'] in categories['Location'] else -1,
            float(data['MinTemp']), float(data['MaxTemp']), float(data['Rainfall']),
            float(data['Evaporation']), float(data['Sunshine']),
            categories['WindGustDir'].index(data['WindGustDir']) if data['WindGustDir'] in categories['WindGustDir'] else -1,
            float(data['WindGustSpeed']),
            categories['WindDir9am'].index(data['WindDir9am']) if data['WindDir9am'] in categories['WindDir9am'] else -1,
            categories['WindDir3pm'].index(data['WindDir3pm']) if data['WindDir3pm'] in categories['WindDir3pm'] else -1,
            float(data['WindSpeed9am']), float(data['WindSpeed3pm']),
            float(data['Humidity9am']), float(data['Humidity3pm']),
            float(data['Pressure9am']), float(data['Pressure3pm']),
            int(data['Cloud9am']), int(data['Cloud3pm']),
            float(data['Temp9am']), float(data['Temp3pm']),
            categories['RainToday'][data['RainToday']]
        ]
    except Exception as e:
        return jsonify({'error': f"Invalid input: {str(e)}"}), 400

    input_df = pd.DataFrame([input_features])

    # Make predictions
    try:
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0, 1] if hasattr(model, "predict_proba") else None

        result = {
            'Rainfall Prediction': 'Yes' if prediction == 1 else 'No',
            'Probability': f"{probability:.2f}" if probability else "N/A"
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
