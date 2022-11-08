import subprocess
import cv2
import numpy as np
from flask import Flask, render_template, Response

p = subprocess.Popen((['python','camera.py']), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
app = Flask(__name__)


def camera():
    frame = p.communicate()
    frame = np.array(frame)
    frame = frame.tobytes()
    print(frame)
    # yield (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    # # p.stdout.flush()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(camera(), mimetype='multipart/x-mixed-replace; boundary=frame')


# output = p.communicate(b"")[0]

#print(output)
if __name__ == "__main__":
    app.run(debug=True)
    # p = subprocess.Popen((['python','camera.py']), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # for line in p.stdout:
    #     print(">>> " + str(line.rstrip().decode('utf-8')))
    #     p.stdout.flush()