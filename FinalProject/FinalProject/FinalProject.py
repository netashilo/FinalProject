import cv2
import Image
from Video import upload_video
from Video import save_frames
from Video import background_sub
from OpticFlow import optic_flow


#Image.upload_img('content/kids.JPG')
#files_list = ['content/IMG_5952.JPG', 'content/IMG_5953.JPG', 'content/IMG_5954.JPG', 'content/IMG_5955.JPG', 'content/IMG_5956.JPG']
#optic_flow(files_list)
#upload_video('content/shirel1.mp4')
save_frames('content/OpticFlow/shirel.mp4', 10, 3)
frames_list = []
name = "content/OpticFlow/shirel"
for i in range(10):
    frames_list.append(cv2.imread("%s%d.jpg"%(name, i)))
optic_flow(frames_list, name)
