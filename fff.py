from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

cam = cv2.VideoCapture(0)

def gen_frames():
    while True:
        x,frame = cam.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        print(frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') ##### ajustar

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    #photo_generator(50)
    app.run(debug=True)
    #gen_frames()
    #b = b'b\'\\1234'
    #print(b.decode('utf-8').decode('utf-8'))