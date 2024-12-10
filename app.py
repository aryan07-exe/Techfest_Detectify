from flask import Flask, render_template, Response, jsonify, request
from ultralytics import YOLO
import cv2

app = Flask(__name__)

# Load YOLO model
model = YOLO('yolov8n.pt')

# Global variables for webcam
video_capture = None
running = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_detection', methods=['POST'])
def start_detection():
    global video_capture, running
    if not running:
        video_capture = cv2.VideoCapture(0)  # Open webcam
        running = True
        return jsonify({'status': 'Detection started'})
    return jsonify({'status': 'Detection is already running'})


@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    global video_capture, running
    if running and video_capture:
        video_capture.release()
        running = False
        return jsonify({'status': 'Detection stopped'})
    return jsonify({'status': 'Detection is not running'})


@app.route('/video_feed')
def video_feed():
    def generate_frames():
        global video_capture, running
        while running and video_capture.isOpened():
            success, frame = video_capture.read()
            if not success:
                break

            # Perform object detection using YOLO
            results = model(frame)
            annotated_frame = results[0].plot()  # Annotate the frame with detections

            # Encode the frame to JPEG
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            if not ret:
                break

            # Yield the frame as a response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
