import cv2
import time
import numpy
import sys
numpy.set_printoptions(threshold=sys.maxsize)
cam = cv2.VideoCapture(0)

def gen_frames():
   #while True:
    time.sleep(0.5)
    x,frame = cam.read()
    ret, jpeg = cv2.imencode('.jpg', frame)
    #frame = jpeg.tobytes()
    print (jpeg)
gen_frames()


# def doideira():
#     i=12
#     while True:
#         i=i+1
    
#         #yield i
#         print(i)

# doideira()
