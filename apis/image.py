from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load the model
model_path = "/Users/victoriale/Documents/ASL-Translation/model2_32.keras"
model = load_model(model_path)

# Define ASL classes
asl_classes = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ['del', 'nothing', 'space']

def preprocess_image(image, target_size=(32, 32)):
    """
    Preprocess the uploaded image:
    - Convert it to grayscale.
    - Resize to the target size.
    - Normalize pixel values.
    """
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    img = cv2.resize(img, target_size) 
    img = img / 255.0 
    img = np.expand_dims(img, axis=-1) 
    img = np.expand_dims(img, axis=0)
    return img

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict ASL character from uploaded image.
    """
    if 'image' not in request.files:
        print("DEBUG: No 'image' in request.files")
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        print("DEBUG: Empty filename")
        return jsonify({'error': 'No selected file'}), 400

    print(f"DEBUG: Received file: {image_file.filename}")
    
    try:
        # Read the image file
        image_np = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        
        # Preprocess the image
        processed_image = preprocess_image(image)
        
        # Make prediction
        predictions = model.predict(processed_image)
        predicted_index = np.argmax(predictions, axis=1)[0]
        predicted_label = asl_classes[predicted_index]
        
        return jsonify({'prediction': predicted_label})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
