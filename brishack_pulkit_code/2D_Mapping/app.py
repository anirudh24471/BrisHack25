from flask import Flask, render_template, Response
import cv2
import get_frames
from create_map import load_images_from_folder, check_for_turn

# start the flask app
app = Flask(__name__)

# Initialize camera
camera = cv2.VideoCapture(0)
x_coord, y_coord = 0, 0


def generate_frames():

    # Create a directory to store the frames
    get_frames.manage_directory("statics/frames")

    # Loop to capture frames
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Convert frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_buffer = buffer.tobytes()

            # Define folder path and number of frames to check
            folder_path = 'statics/frames'  # Update with your folder path
            num_frames = 5

            # Load the latest frames from the folder
            frames = load_images_from_folder(folder_path, num_frames)
            #print(frames)
            # Check for a turn
            #print(frames)
            turn = check_for_turn(frames)
            #turn =1
            global x_coord
            global y_coord

            if turn==1:
                x_coord = x_coord + 1
                y_coord = y_coord + 1
                print("Turn detected!")
            else:
                y_coord = y_coord + 1
                print("No turn detected.")
            
            get_frames.generate_2d_map(x_coord, y_coord, frame)
            
            # Yield the frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_buffer + b'\r\n')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video')
def video():
    """Page that displays the live video feed."""
    return render_template('video_feed.html')

@app.route('/video_feed')
def video_feed():
    """Provides the live video stream."""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)