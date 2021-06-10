import os, sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#stderr = sys.stderr
#sys.stderr = open(os.devnull, 'w')
import cv2
import numpy as np
from PIL import Image
import time
#sys.stderr = stderr

vc = cv2.VideoCapture(0)
print("Reading the Frame from the Camera")

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False
    print("Could not open the camera...")
    
print("Can I see through the video camera?", rval)
classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
folder = "Images/"

frame_num = 0
frame_pause_num = -1
last_frame_detected = 0
try:
    while rval:
        if frame_num > last_frame_detected + 5:
            faces = classifier.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.3, 5)
            for face in range(len(faces)):
                x,y,w,h = faces[face]
                last_frame_detected = frame_num
                Image.fromarray(frame[y:y+h,x:x+w][:,:,::-1]).save(folder + str(time.time())[5:] + ".png")
                frame_pause_num = -1
        rval, frame = vc.read()
        frame_num+=1
except:
    vc.release()
