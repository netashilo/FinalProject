from VideoAnalizer import VideoAnalizer
from Video import save_frames
from OpticFlow import optic_flow
import cv2

class Main(object):
    """description of class"""
    vid_analizer = VideoAnalizer('content/shirel.mp4')
    vid_analizer.read_video()

