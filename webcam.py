from flask import Flask, Response
import cv2

app = Flask(__name__)

# Initialize camera
camera = cv2.VideoCapture(0)


def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
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
        <title>Live Camera Feed</title>
    </head>
    <body>
        <h1>Live Camera Feed</h1>
        <img src="/video_feed" style="width: 640px; height: 480px;">
    </body>
    </html>
    """


@app.route('/video_feed')
def video_feed():
    # Return the response generated along with the specific media
    # type (mime type)
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
