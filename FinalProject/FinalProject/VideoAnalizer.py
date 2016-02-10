import os
import cv2
from ImageAnalizer import ImageAnalizer

class VideoAnalizer:
    """description of class"""
    def __init__(self, file_name):
        if not self.check_file_name(file_name):
            return
        self.cap = cv2.VideoCapture(file_name)   # load video
        self.create_video_writer(file_name)
        self.read_video()
    
    def check_file_name(self, file_name):
        list = file_name.split('.')
        if list[len(list)-1] != "mp4":
            print "Invalid file. File must be a mp4 file"
            return False
        if not os.path.isfile(file_name):
            print "File dose not exists"
            return False
        return True

    # This function defines the codec and creates VideoWriter object
    def create_video_writer(self, file_name):
        name = os.path.splitext(file_name)[0]                       # define the new video name
        self.fps = self.cap.get(cv2.cv.CV_CAP_PROP_FPS)             # get video frames-per-second number
        width = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))   # get video frames width and height
        height = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        size = (height, width)                                      # define new video frame size
        fourcc = cv2.cv.CV_FOURCC(*'DIVX')
        self.out = cv2.VideoWriter("%s_output.avi"%name ,fourcc, self.fps, size)
        
    #
    def read_video(self):
        prev_img_analizer = None
        # loop to read video frame by frame
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if not ret:
                break
            #frame = self.rotate_90(frame)                       # rotate the frame
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     # change to gray scale
            img_analizer = ImageAnalizer(frame , prev_img_analizer)
            img_analizer.mark_faces()
            self.out.write(img_analizer.frame)
            cv2.imshow('frame', img_analizer.frame)             # Display the resulting frame
            if cv2.waitKey(int(self.fps)) & 0xFF == ord('q'):
                break
            prev_img_analizer = img_analizer
        self.release_memory()

    # This function rotates a given image 90 degrees to the right
    def rotate_90(self, img):
        cv2.flip(img, 0, img)
        return cv2.transpose(img)

    def release_memory(self):        
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()