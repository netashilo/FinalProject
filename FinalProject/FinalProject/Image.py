import cv2
import numpy as np
import os

def resizeImage(img, num):    
    height, width, a = img.shape
    dim = (width/num, height/num)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
def upload_img(file_name):
    #load the appropriate xml file
    face_cascade = cv2.CascadeClassifier('C:\Users\owner\Documents\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('C:\Users\owner\Documents\opencv\sources\data\haarcascades\haarcascade_eye.xml')
    
    img = cv2.imread(file_name)                             #load the image and resize it
    img = resizeImage(img, 5)
    img = face_detection(img, face_cascade, eye_cascade)    #detect faces in the image 
    name = "%s_output.jpg"%(os.path.splitext(file_name)[0])                  #define the new video name
    cv2.imwrite(name, img)

    #display image on screen
    cv2.imshow('kids', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#This function detect faces&eyes in a given image and marks it with a rectangle
def face_detection(frame, face_cascade, eye_cascade):
    faces = face_cascade.detectMultiScale(frame, 1.2, 1)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        face_rect = frame[y:y+h, x:x+w]
        eye_detection(face_rect, eye_cascade)
    return frame

#This function detect the eyes in a given face-rectangle and marks it with a rectangle
def eye_detection(face_rect, eye_cascade):
    eyes = eye_cascade.detectMultiScale(face_rect, 1.2, 3)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(face_rect,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
