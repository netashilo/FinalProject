import cv2
import numpy as np
import os
from CascadeDictionary import dict

def resizeImage(img, num):    
    height, width, a = img.shape
    dim = (width/num, height/num)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
def upload_img(file_name):    
    img = cv2.imread(file_name) # load the image
    faces = face_detection('haarcascade_frontalface_default', img, 1.48, 2)   # detect frontal-faces in the image
    faces += face_detection('haarcascade_profileface', img, 1.85, 2)          # detect profile-faces in the image
    img = resizeImage(img, 5)
    name = "%s_output.jpg"%(os.path.splitext(file_name)[0]) # define the new file name
    cv2.imwrite(name, img)

    # display image on screen
    cv2.imshow('kids', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# This function detect frontal/profile-faces in a given image and marks it with a rectangle
def face_detection(cascade, frame, scale_factor, min_neighbors):
    faces = dict.get(cascade).detectMultiScale(frame, scale_factor, min_neighbors)
    eyes = None
    for (x,y,w,h) in faces:
        face_rect = frame[y:y+h*2/3, x:x+w]
        eyes = eye_detection(face_rect)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    return (faces, eyes)

# This function detect the eyes in a given face-rectangle and marks it with a rectangle
def eye_detection(face_rect):
    eyes = dict.get('haarcascade_eye').detectMultiScale(face_rect, 1.9, 2)
    i = 0
    for (ex,ey,ew,eh) in eyes:
        i += 1
        cv2.rectangle(face_rect,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        if i == 2:
            break
    return eyes
