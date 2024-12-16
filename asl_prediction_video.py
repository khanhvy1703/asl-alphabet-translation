import os
os.system("pip install opencv-python")
os.system("pip install tensorflow")

import cv2
import numpy as np
from tensorflow.keras.models import load_model


model = load_model("model2_32.keras")

def preprocess_frame(frame, target_size=(32, 32)):
    """
    Preprocess a video frame for the model.

    Args:
        frame: Input video frame.
        target_size (tuple): Target size for the frame (default: (32, 32)).

    Returns:
        np.array: Preprocessed frame ready for prediction.
    """

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = cv2.resize(gray_frame, target_size)
    normalized_frame = resized_frame.astype('float32') / 255.0
    
    input_frame = np.expand_dims(normalized_frame, axis=-1)
    input_frame = np.expand_dims(input_frame, axis=0)  # Add batch dimension
    return input_frame

video_capture = cv2.VideoCapture(0)

class_labels = ['Class1', 'Class2', 'Class3', ...]

while True:
    ret, frame = video_capture.read()
    
    if not ret:
        print("Failed to grab frame or video ended.")
        break

    input_frame = preprocess_frame(frame)
    
    predictions = model.predict(input_frame)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_label = class_labels[predicted_class_index]

    cv2.putText(frame, f"Prediction: {predicted_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Video Prediction", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
