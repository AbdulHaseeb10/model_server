import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)
# # Load the KNN model from a joblib file
knn_saved = joblib.load('knn_har_model.joblib')

@app.route('/')
def hello_world():
    return 'Hello, World!'


# # API endpoint to receive input and return predictions
@app.route('/predict', methods=['POST'])
def predict():
#     # Extract input data from request
    data = request.get_json()
    print(data)
    input_data = data
    predictions = knn_saved.predict(input_data)
    response = {'predictions': predictions.tolist()}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)


