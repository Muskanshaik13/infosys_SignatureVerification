# predict.py

import numpy as np
import cv2
import pickle
import os

# Load the Pickle model once when the module is loaded
model_path = os.path.join(os.path.dirname(__file__), '../models/signature_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

def preprocess_image(image_path):
    """
    Load and preprocess the image for prediction.
    - Loads the image, converts it to grayscale, resizes, normalizes, and reshapes.
    """
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Failed to load image. Please check the file path.")

    # Resize to the model's expected input size (e.g., 256x256)
    processed_image = cv2.resize(image, (256, 256))

    # Normalize pixel values to range [0, 1]
    processed_image = processed_image / 255.0

    # Flatten or reshape as needed for your model's input format
    processed_image = processed_image.astype(np.float32).reshape(1, -1)  # Example for a flat input

    return processed_image

def predict_signature(image):
    """
    Predict whether the signature is real or forged using the Pickle model.
    
    Parameters:
        image (np.array): Preprocessed image ready for the model.
    
    Returns:
        tuple: A tuple containing:
            - label (int): 0 for Real, 1 for Forged.
            - accuracy (float): Confidence score (if applicable).
    """
    # Run the prediction
    predicted_label = model.predict(image)[0]  # Get the label (assuming 0 = Real, 1 = Forged)
    
    # If the model supports probability predictions, get confidence
    if hasattr(model, "predict_proba"):
        confidence = model.predict_proba(image)[0][predicted_label]
    else:
        confidence = 0.85  # Mock accuracy if probability not available

    return predicted_label, round(confidence * 100, 2)
