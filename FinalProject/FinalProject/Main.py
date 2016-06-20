from VideoAnalizer import VideoAnalizer
from Video import save_frames
import cv2
import time

class Main(object):
    """description of class"""
    
    files_list = ("content/liraz", "content/talya", "content/riv")
    for name in list:
        start_time = time.time()
        vid_analizer = VideoAnalizer('%s.mp4'%(name),False)
        vid_analizer.read_video(name)
        f = open('%s_output.txt'%name, 'a')  
        print >> f," system running time: %s minutes"%((time.time() - start_time)/60)
        f.close()
    