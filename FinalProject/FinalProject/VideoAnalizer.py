import os
import cv2
from Frame import Frame

class VideoAnalizer:
    """description of class"""
    def __init__(self, file_name):
        self.cap = cv2.VideoCapture(file_name)   # load video
        self.create_video_writer(file_name)
        self.prev_frame = None
        self.read_video()


    # This function defines the codec and creates VideoWriter object
    def create_video_writer(self, file_name):
        name = os.path.splitext(file_name)[0]                       # define the new video name
        self.fps = self.cap.get(cv2.cv.CV_CAP_PROP_FPS)             # get video frames-per-second number
        width = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))   # get video frames width and height
        height = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        size = (height, width)                                      # define new video frame size
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        self.out = cv2.VideoWriter("%s.avi"%name ,fourcc, self.fps, size, False)
        
    #
    def read_video(self):
        # loop to read video frame by frame
        while(self.cap.isOpened()):
            ret, img = self.cap.read()
            if not ret:
                break
            img = self.rotate_90(img)                       # rotate the frame
            #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)     # change to gray scale
            self.frame = Frame(img , self.prev_frame)
            self.frame.mark_faces()
            self.out.write(self.frame.img)
            cv2.imshow('frame', self.frame.img)             # Display the resulting frame
            if cv2.waitKey(int(self.fps)) & 0xFF == ord('q'):
                break
            self.prev_frame = self.frame
        self.release_memory()

    # This function rotates a given image 90 degrees to the right
    def rotate_90(self, img):
        cv2.flip(img, 0, img)
        return cv2.transpose(img)

    def release_memory(self):        
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()