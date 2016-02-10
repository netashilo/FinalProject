import numpy as np
import cv2
import os
from CascadeDictionary import d
import Image

# This function captures and saves a video from computer camera, and display it on the screen
def camera_capture():
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    out = create_video_writer('neta', fps, (640,480))

    # loop to capture video frame by frame
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # Changing to gray scale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #  write the frame
            out.write(gray)

            # Display the resulting frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# This function displays a given video, where the moving objects are painted in white
def background_sub(file_name):
    cap = cv2.VideoCapture(file_name)
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

# The function saves a given number of frames as images 
def save_frames(file_name, N, freq):
    cap = cv2.VideoCapture(file_name)       # upload video
    name = os.path.splitext(file_name)[0]   # define the new video name
    for i in range(N):
        for j in range(freq):
            cap.read()
        ret, frame = cap.read()
        if not ret:
            break
        #frame = rotate_90(frame)
        new_name = "%s%d.jpg"%(name,i) # define the new file name
        cv2.imwrite(new_name, frame)

# This function rotates a given image 90 degrees to the right
def rotate_90(img):
    cv2.flip(img, 0, img)
    return cv2.transpose(img)