import numpy as np
import cv2
import os

#This function captures and saves a video from computer camera, and display it on the screen
def camera_capture():
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)

    #Define the codec and create VideoWriter object
    out = create_video_writer('neta', fps, (640,480))

    while(cap.isOpened()):
        #Capture frame by frame
        ret, frame = cap.read()
        if ret == True:
            #Changing to gray scale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # write the frame
            out.write(gray)

            #Display the resulting frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
         
    cap.release()
    out.release()
    cv2.destroyAllWindows()

#This function defines the codec and creates VideoWriter object
def create_video_writer(file_name, fps, size):
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter("%s.avi"%file_name ,fourcc, fps, size, False)
    return out

#This function upload an existing video, detect faces&eyes, and display it on the screen
def upload_video():
    #load the xml file
    face_cascade = cv2.CascadeClassifier('C:\Users\owner\Documents\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('C:\Users\owner\Documents\opencv\sources\data\haarcascades\haarcascade_eye.xml')
    
    cap = cv2.VideoCapture('shirel.mp4')
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    size = (height, width)
    print cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
    out = create_video_writer('shirel', fps, size)
    while(True):
        ret = [None]*10
        frame = [None]*10
        gray = [None]*10
        #Capture 10 frames
        for i in range(10):
            ret[i], frame[i] = cap.read()
            if not ret[i]:
                break

            #rotate the frame
            cv2.flip(frame[i], 0, frame[i])
            frame[i] = cv2.transpose(frame[i])
            gray[i] = cv2.cvtColor(frame[i], cv2.COLOR_BGR2GRAY)

        frame = face_detection(gray, face_cascade, eye_cascade)
        for i in range(10):
            if(frame[i] == None):
                break
            out.write(frame[i])
            #Display the resulting frame
            cv2.imshow('frame', frame[i])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        if i != 9:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

#This function displays a given video where the moving objects are painted in white
def background_sub():
    cap = cv2.VideoCapture('output.avi')
    fgbg = cv2.BackgroundSubtractorMOG()

    while(1):
        ret, frame = cap.read()
        if ret == True:
            fgmask = fgbg.apply(frame)

            cv2.imshow('frame',fgmask)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

#This function marks faces&eyes in a given image with a rectangle
def face_detection(frames, face_cascade, eye_cascade):
    roi = [None]*10
    faces = face_cascade.detectMultiScale(frames[0], 1.2, 1)
    for (x,y,w,h) in faces:
        for i in range(10):
            if(frames[i] == None):
                break
            cv2.rectangle(frames[i],(x,y),(x+w,y+h),(255,0,0),2)
            roi[i] = frames[i][y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]
        eye_detection(roi, eye_cascade)
    return frames

#This function mark the eyes in a given face-rectangle
def eye_detection(roi, eye_cascade):
    eyes = eye_cascade.detectMultiScale(roi[0])
    for (ex,ey,ew,eh) in eyes:
        for i in range(10):
            if(roi[i] == None):
                break
            cv2.rectangle(roi[i],(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

upload_video()

