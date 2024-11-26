import os
import joblib
import numpy as np
from django.conf import settings


class HealthPredictor:
    def __init__(self):
        """
        Initializes the predictor by loading the machine learning model from a .pkl file.
        """
        model_path = os.path.join(settings.BASE_DIR, 'models', 'knn_model.pkl')  # Adjust the model file name if necessary
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            raise Exception(f"Model file not found at {model_path}. Ensure the file exists.")
        except Exception as e:
            raise Exception(f"Error loading model: {e}")

    def predict(self, input_data):
        """
        Predicts the likelihood of heart disease based on input data.
        
        Args:
            input_data (dict): A dictionary containing the following keys:
                - height (float)
                - weight (float)
                - temperature (float)
                - heart_rate (int)
                - cholesterol (int)
                - blood_sugar (int)
                - systolic (int)
                - diastolic (int)
                - symptoms (str)
                - existing_conditions (str)
                - family_history (str)
                - smoking_status (str)
        
        Returns:
            dict: A dictionary containing:
                - predicted_disease (str)
                - confidence_score (float)
        """
        try:
            # Prepare the input for the model
            features = self._preprocess_input(input_data)
            
            # Predict using the model
            prediction = self.model.predict([features])[0]
            confidence_score = np.max(self.model.predict_proba([features])) * 100  # Assuming model supports predict_proba
            
            # Convert prediction to a meaningful output
            predicted_disease = "Heart Disease" if prediction == 1 else "No Heart Disease"
            
            return {
                "predicted_disease": predicted_disease,
                "confidence_score": round(confidence_score, 2)
            }
        except Exception as e:
            raise Exception(f"Error during prediction: {e}")

    def _preprocess_input(self, input_data):
        """
        Converts input data into a format suitable for the machine learning model.
        
        Args:
            input_data (dict): Raw input data from the form.
        
        Returns:
            list: Processed feature vector.
        """
        # Map categorical data to numerical values
        symptoms_mapping = {
            "Chest Pain": 1,
            "Shortness of Breath": 2,
            "Fainting": 3,
            "Nausea": 4,
            "Vomiting": 5,
            "Diarrhea": 6,
            "Unknown": 0
        }
        condition_mapping = {
            "Diabetes": 1,
            "Hypertension": 2,
            "High Cholesterol": 3,
            "Asthma": 4,
            "Unknown": 0
        }
        laboratory_test_results_mapping = {
            "High Cholesterol": 1,
            "High Blood Sugar": 2,
            "Normal": 3,
            "Low Iron": 4,
            "Unknown": 0
        }
        family_history_mapping = {"Yes": 1, "No": 0, "Unknown": -1}
        smoking_status_mapping = {"Never": 0, "Former": 1, "Current": 2, "Unknown": -1}
        
        # Extract and process input features
        try:
            features = [
                input_data['height'],
                input_data['weight'],
                input_data['temperature'],
                input_data['heart_rate'],
                input_data['cholesterol'],
                input_data['blood_sugar'],
                input_data['systolic'],
                input_data['diastolic'],
                symptoms_mapping.get(input_data['symptoms'], 0),
                condition_mapping.get(input_data['existing_conditions'], 0),
                laboratory_test_results_mapping.get(input_data['laboratory_test_results'], 0),
                family_history_mapping.get(input_data['family_history'], -1),
                smoking_status_mapping.get(input_data['smoking_status'], -1)
            ]
        except KeyError as e:
            raise Exception(f"Missing input data: {e}")
        
        return features
