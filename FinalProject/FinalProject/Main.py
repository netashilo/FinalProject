from VideoAnalizer import VideoAnalizer
from VideoAnalizer import camera_capture
import cv2
import time

class Main(object):
    """ The main class of the project.
        The class sends videos to analize. """
    # list of video files
    ## save a video usinf computer camera
    #camera_capture("content/rivka11")
    files_list = ("content/rivka11", "content/rivka12")
    for name in files_list:
        start_time = time.time()
        vid_analizer = VideoAnalizer('%s.mp4'%(name),False)
        if vid_analizer.cap is None:
            continue
        vid_analizer.read_video(name)
        f = open('%s_output.txt'%name, 'a')  
        print >> f," system running time: %s minutes"%((time.time() - start_time)/60)
        f.close()
    