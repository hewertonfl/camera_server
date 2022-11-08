#Import necessary libraries
from flask import Flask, render_template, Response
import cv2
import pickle
import os
import time
#Initialize the Flask app
app = Flask(__name__)


global path
path= os.getcwd()

def video_generator():
    i = 0
    while True:
        time.sleep(0.1)
        file = open(os.getcwd()+f"\images{i}.pkl", 'rb')
        frame = pickle.load(file)
        print(os.getcwd()+f"\images{i}.pkl")

 
        file.close()
        #dec_img = cv2.imdecode(frame, 1)
        #print(frame)

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        
        # if i == 9:
        #     i=0
        os.remove(os.getcwd()+f"\images{i}.pkl")
        i+=1
        if i == 49:
            photo_generator(50)
            i=0
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') ##### ajustar

def photo_generator(x):
    camera = cv2.VideoCapture(0)
    
    for i in range(x):
        check, frame = camera.read()
        with open(f"images{i}.pkl",'wb') as f:
                    pickle.dump(frame, f)

def read ():
    with open ("images.pkl",'rb') as f:
        frame=pickle.load(f)
        for file in frame:
            #ret, jpeg = cv2.imencode('.jpg', frame)
            #frame = jpeg.tobytes()

            cv2.imshow('a',frame)
            cv2.waitKey()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    photo_generator(50)
    app.run(debug=True)
    #print(type(os.getcwd()))
    
