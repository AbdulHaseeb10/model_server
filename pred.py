# import pandas as pd
# from flask import Flask, request, jsonify
# # from flask_cors import CORS
# import joblib

# app = Flask(__name__)
# # CORS(app)
# # # Load the KNN model from a joblib file
# knn_saved = joblib.load('knn_har_model.joblib')

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


# # # API endpoint to receive input and return predictions
# @app.route('/predict', methods=['POST'])
# def predict():
# #     # Extract input data from request
#     inputData = request.get_json()
#     print(inputData)
#     inputData=inputData.data
#     # inputData = pd.read_csv('jogging_activity.csv')
#     predictions = knn_saved.predict(inputData)
#     response = {'predictions': predictions.tolist()}
#     return jsonify(response)

# if __name__ == '__main__':
#     app.run(debug=True)

# import json
# import pandas as pd
# import statistics
# from flask import Flask, request, jsonify
# import joblib

# app = Flask(__name__)

# def getMostProbableActivity(predictions):
#     mostProbableActivity = statistics.mode(predictions)
#     if(mostProbableActivity==0):
#         mostProbableActivity="Jogging"
#     elif(mostProbableActivity==1):
#         mostProbableActivity="Sitting"
#     elif(mostProbableActivity==2):
#         mostProbableActivity="Standing"
#     else: mostProbableActivity="Walking"
#     return mostProbableActivity

# def getActivityObj(predictions):
#       dict_obj = {"jogging": 0.0, "sitting": 0.0, "standing": 0.0, "walking": 0.0}
#       for prediction in predictions:
#         if prediction == 0:
#             dict_obj["jogging"] += 1
#         elif prediction == 1:
#             dict_obj["sitting"] += 1
#         elif prediction == 2:
#             dict_obj["standing"] += 1
#         elif prediction == 3:
#             dict_obj["walking"] += 1
#       return dict_obj

# # Load the KNN model from a joblib file
# knn_saved = joblib.load('knn_har_model.joblib')
# decision_model = joblib.load('decision_tree_model.joblib')
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


# # API endpoint to receive input and return predictions
# @app.route('/predict', methods=['POST'])
# def predict():
#     # Extract input data from request
#     input_data = request.get_json()
#     print(request.headers.get('Content-Type'))
#     print(input_data)
#     # Convert JSON string to a Python dictionary
#     # input_data = json.loads(input_data)
#     print(input_data)
#     # Create a DataFrame from the input data
#     input_df = pd.DataFrame.from_dict(input_data)

#     # Make predictions using the model
#     predictions = knn_saved.predict(input_df)
#     decision_model_predictions =decision_model.predict(input_df)

#     dict_obj_knn = getActivityObj(predictions)
#     mostProbableActivityKnn= getMostProbableActivity(predictions)

#     dict_obj_decision_tree = getActivityObj(decision_model_predictions)
#     mostProbableActivityDecisionTree= getMostProbableActivity(decision_model_predictions)
#     # Convert predictions to a list and return as a JSON response
#     response = {'knn':{'mostProbableActivity': mostProbableActivityKnn, 'activities': {k: int(v) for k, v in dict_obj_knn.items()}},
#                 'decisonTree':{'mostProbableActivity': mostProbableActivityDecisionTree,'activities': {k: int(v) for k, v in dict_obj_decision_tree.items()}}}
#     return jsonify(response)

# if __name__ == '__main__':
#     app.run(debug=True)


import statistics
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
app = Flask(__name__)
CORS(app)


def getMostProbableActivity(predictions):
    mostProbableActivity = statistics.mode(predictions)
    if mostProbableActivity == 0:
        mostProbableActivity = "Jogging"
    elif mostProbableActivity == 1:
        mostProbableActivity = "Sitting"
    elif mostProbableActivity == 2:
        mostProbableActivity = "Standing"
    else:
        mostProbableActivity = "Walking"
    return mostProbableActivity

def getActivityObj(predictions):
    dict_obj = {"jogging": 0.0, "sitting": 0.0, "standing": 0.0, "walking": 0.0}
    for prediction in predictions:
        if prediction == 0:
            dict_obj["jogging"] += 1
        elif prediction == 1:
            dict_obj["sitting"] += 1
        elif prediction == 2:
            dict_obj["standing"] += 1
        elif prediction == 3:
            dict_obj["walking"] += 1
    return dict_obj

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract input data from request
        input_data = request.get_json()
        # Create a DataFrame from the input data
        input_df = pd.DataFrame.from_dict(input_data)
        
        # Load the KNN model from a joblib file
        knn_saved = joblib.load('knn_har_model.joblib')
        decision_model = joblib.load('decision_tree_model.joblib')

        # Make predictions using the models
        predictions = knn_saved.predict(input_df)
        decision_model_predictions = decision_model.predict(input_df)

        dict_obj_knn = getActivityObj(predictions)
        mostProbableActivityKnn = getMostProbableActivity(predictions)

        dict_obj_decision_tree = getActivityObj(decision_model_predictions)
        mostProbableActivityDecisionTree = getMostProbableActivity(decision_model_predictions)

        # Convert predictions to a list and return as a JSON response
        response = {
            'knn': {
                'mostProbableActivity': mostProbableActivityKnn,
                'activities': {k: int(v) for k, v in dict_obj_knn.items()}
            },
            'decisionTree': {
                'mostProbableActivity': mostProbableActivityDecisionTree,
                'activities': {k: int(v) for k, v in dict_obj_decision_tree.items()}
            }
        }
        return jsonify(response)
    except Exception as e:
        # Handle any errors that occur during the prediction process
        error_message = str(e)
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=False)

