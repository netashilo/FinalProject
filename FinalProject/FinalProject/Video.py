import numpy as np
import cv2
import os
from CascadeDictionary import dict
import Image

# This function upload an existing video, detect faces&eyes, and display it on the screen
def upload_video(file_name):
    
    cap = cv2.VideoCapture(file_name)                       # upload video
    name = os.path.splitext(file_name)[0]                   # define the new video name
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)                   # get video frames-per-second number
    width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))    # get video frames width and height
    height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    size = (height, width)                                  # define new video frame size
    out = create_video_writer(name, fps, size)              

    # loop to read video frame by frame
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        frame = rotate_90(frame)                            # rotate the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      # change to gray scale
        frame = Image.frontal_face_detection(gray)
        frame = Image.profile_face_detection(frame)
        out.write(frame)
        cv2.imshow('frame', frame)                          # Display the resulting frame
        if cv2.waitKey(int(fps)) & 0xFF == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# This function defines the codec and creates VideoWriter object
def create_video_writer(file_name, fps, size):
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter("%s.avi"%file_name ,fourcc, fps, size, False)
    return out

# This function rotates a given image 90 degrees to the right
def rotate_90(img):
    cv2.flip(img, 0, img)
    return cv2.transpose(img)

# This function captures and saves a video from computer camera, and display it on the screen
def camera_capture():
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    out = create_video_writer('neta', fps, (640,480))

    while(cap.isOpened()):
        # Capture frame by frame
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

# This function displays a given video where the moving objects are painted in white
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