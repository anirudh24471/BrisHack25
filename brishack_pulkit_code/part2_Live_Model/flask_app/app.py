from flask import Flask, render_template, request, Response
import cv2
import numpy as np
import tensorflow as tf
import os
from werkzeug.utils import secure_filename

# Load the saved model
model = tf.keras.models.load_model("your_model.h5")

# Define labels
class_labels = ['Person', 'Plastic', 'Paper', 'Cardboard', 'Metal']  # Update with actual labels

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to process image
def predict_image(image_path):
    input_size = (150, 150)  # Expected size for model
    image = cv2.imread(image_path)
    image = cv2.resize(image, input_size)
    image = image / 255.0  # Normalize
    input_data = np.expand_dims(image, axis=0)
    
    predictions = model.predict(input_data)
    predicted_class = np.argmax(predictions[0])
    confidence = np.max(predictions[0])
    
    return class_labels[predicted_class], confidence

# Function for real-time object detection
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            input_size = (150, 150)
            resized_frame = cv2.resize(frame, input_size)
            normalized_frame = resized_frame / 255.0
            input_data = np.expand_dims(normalized_frame, axis=0)
            
            predictions = model.predict(input_data)
            predicted_class = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            
            if confidence > 0.50:
                label = f"{class_labels[predicted_class]} ({confidence:.2f})"
                cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            label, confidence = predict_image(filepath)
            return render_template('index.html', image=filepath, label=label, confidence=confidence)
    
    return render_template('index.html', image=None)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)