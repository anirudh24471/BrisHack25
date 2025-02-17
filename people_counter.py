from flask import Flask, Response
import cv2
from ultralytics import YOLO
import sqlite3
import csv
from datetime import datetime

app = Flask(__name__)

# Initialize the camera
camera = cv2.VideoCapture(0)

# Load the YOLOv8 model (pre-trained on COCO dataset)
model = YOLO('yolov8n.pt')  # You can use other models like 'yolov8s.pt' for more accuracy

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('people_count.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS people_count
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME,
                  num_people INTEGER)''')
    conn.commit()
    conn.close()

# Log data to CSV file
def log_to_csv(timestamp, num_people):
    with open('people_count.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, num_people])

# Store data in SQLite database
def store_in_db(timestamp, num_people):
    conn = sqlite3.connect('people_count.db')
    c = conn.cursor()
    c.execute("INSERT INTO people_count (timestamp, num_people) VALUES (?, ?)",
              (timestamp, num_people))
    conn.commit()
    conn.close()

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Perform object detection on the frame
            results = model(frame)

            # Count the number of people detected
            num_people = 0
            for result in results:
                boxes = result.boxes  # Get bounding boxes
                for box in boxes:
                    class_id = int(box.cls)  # Get class ID
                    if model.names[class_id] == 'person':  # Check if the detected object is a person
                        num_people += 1

            # Get current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Store data in SQLite database
            store_in_db(timestamp, num_people)

            # Log data to CSV file
            log_to_csv(timestamp, num_people)

            # Display the number of people on the frame
            cv2.putText(frame, f'People: {num_people}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Convert frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    # HTML page with video stream
    return """
    <html>
    <head>
        <title>Live Camera Feed with People Count</title>
    </head>
    <body>
        <h1>Live Camera Feed with People Count</h1>
        <img src="/video_feed" style="width: 640px; height: 480px;">
    </body>
    </html>
    """


@app.route('/video_feed')
def video_feed():
    # Return the response generated along with the specific media type (mime type)
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # Initialize the database
    init_db()

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)