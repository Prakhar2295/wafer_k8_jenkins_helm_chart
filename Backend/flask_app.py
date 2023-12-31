from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Counter, Gauge
import os
from prediction_validation_insertion import pred_validation
from predictFromModel import prediction

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP requests')
PREDICTION_RESULT = Gauge('prediction_result', 'Prediction Result')

@app.route('/predict', methods=['POST'])
def predict():
    REQUEST_COUNTER.inc()
    
    os.makedirs("raw_data", exist_ok=True)
    uploaded_file = request.files['file']
    
    if uploaded_file:
        file_path = os.path.join("raw_data", uploaded_file.filename)
        uploaded_file.save(file_path)
        
        path = "raw_data"
        pred_valid = pred_validation(path)
        pred_valid.prediction_validation()
        
        pred = prediction()
        result = pred.predictionfrommodel()
        PREDICTION_RESULT.set(result)
        
        return jsonify({'prediction': result.tolist()})

@app.route('/get_prediction', methods=['GET'])
def get_prediction():
    REQUEST_COUNTER.inc()
    
    file_path = "default_file"
    if file_path is not None:
        pred_valid = pred_validation(file_path)
        pred_valid.prediction_validation()
        
        pred = prediction()
        result = pred.predictionfrommodel()
        #result = float(result)
        #PREDICTION_RESULT.set(result)
        
        return jsonify({'prediction': result})

if __name__ == "__main__":
    # Start Prometheus HTTP server on port 8000 to scrape metrics
    start_http_server(8000)
    app.run(host='0.0.0.0', port=5000)
