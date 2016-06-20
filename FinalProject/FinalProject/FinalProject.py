from VideoAnalizer import VideoAnalizer
from Video import save_frames
import cv2
import time

class Main(object):
    """description of class"""
    
    start_time = time.time()
    vid_analizer = VideoAnalizer('content/talya.mp4',False)
    vid_analizer.read_video()
    f = open('content/output.txt', 'w')  

    print >> " system running time: %s minutes"%((time.time() - start_time)/60)
    f.close()