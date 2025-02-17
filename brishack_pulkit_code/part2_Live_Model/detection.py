import cv2
import numpy as np
import tensorflow as tf

# Load the saved .h5 model
model = tf.keras.models.load_model("your_model.h5")

# Define labels (Ensure these match the labels your model was trained on)
class_labels = ['Person', 'Plastic', 'Paper', 'Cardboard', 'Metal']  # Update with actual class names

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Use 0 for default webcam

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Resize the frame to (150, 150) as expected by the model
    input_size = (150, 150)  # Update the size to match model's expected input
    resized_frame = cv2.resize(frame, input_size)

    # Normalize and preprocess the frame
    normalized_frame = resized_frame / 255.0  # Normalize if required
    input_data = np.expand_dims(normalized_frame, axis=0)  # Add batch dimension

    # Make prediction
    predictions = model.predict(input_data)
    predicted_class = np.argmax(predictions[0])  # Get class index
    confidence = np.max(predictions[0])  # Get confidence score

    # Display only if confidence is greater than 80%
    if confidence > 0.80:
        label = f"{class_labels[predicted_class]} ({confidence:.2f})"
        cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the live feed
    cv2.imshow("Object Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
