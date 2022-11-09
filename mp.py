import numpy as np
import cv2
from multiprocessing import Process, Queue
from multiprocessing.shared_memory import SharedMemory
from flask import Flask, render_template, Response

def produce_frames(q):
    #get the first frame to calculate size of buffer
    cap = cv2.VideoCapture(0)
    success, frame = cap.read()
    shm = SharedMemory(create=True, size=frame.nbytes)
    framebuffer = np.ndarray(frame.shape, frame.dtype, buffer=shm.buf) #could also maybe use array.array instead of numpy, but I'm familiar with numpy
    framebuffer[:] = frame #in case you need to send the first frame to the main process
    q.put(shm) #send the buffer back to main
    q.put(frame.shape) #send the array details
    q.put(frame.dtype)
    try:
        while True:
            cap.read(framebuffer)
    except KeyboardInterrupt:
        pass
    finally:
        shm.close() #call this in all processes where the shm exists
        shm.unlink() #call from only one process

def consume_frames(q):
    shm = q.get() #get the shared buffer
    shape = q.get()
    dtype = q.get()
    framebuffer = np.ndarray(shape, dtype, buffer=shm.buf) #reconstruct the array
    try:
        while True:
            x, jpeg = cv2.imencode('.jpg', framebuffer)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            # cv2.imshow("window title", framebuffer)
            # cv2.waitKey(100)
    except KeyboardInterrupt:
        pass
    # finally:
    #     shm.close()


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    q = Queue()
    producer = Process(target=produce_frames, args=(q,))
    producer.start()
    return Response(consume_frames(q), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # q = Queue()
    # producer = Process(target=produce_frames, args=(q,))
    # producer.start()
    # consume_frames(q)
    app.run(debug=True)