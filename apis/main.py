from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
from tensorflow.keras.models import load_model
import numpy as np
import os
import tensorflow as tf

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the model
model_path = os.path.join(os.path.dirname(__file__), "model2_32.keras")
model = load_model(model_path)
print(f"DEBUG: Model loaded from {model_path}")

# Define ASL classes
asl_classes = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ['del', 'nothing', 'space']

def preprocess_image(image, target_size=(32, 32)):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    img = cv2.resize(img, target_size) 
    img = img / 255.0 
    img = np.expand_dims(img, axis=-1) 
    img = np.expand_dims(img, axis=0)
    return img

@app.route('/image-predict', methods=['POST'])
def image_predict():
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
        image_np = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        predicted_index = np.argmax(predictions, axis=1)[0]
        predicted_label = asl_classes[predicted_index]
        
        return jsonify({'prediction': predicted_label})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
