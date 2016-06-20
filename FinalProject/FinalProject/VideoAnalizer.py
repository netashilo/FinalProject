import os
import cv2
import numpy as np
import json
from ImageAnalizer import ImageAnalizer
from subprocess import call
import time
from Face import calc_d
from collections import deque

class VideoAnalizer(object):
    """description of class"""
    def __init__(self, file_name, rotate):
        if not self.check_file(file_name):
            return
        self.rotate = rotate
        self.cap = cv2.VideoCapture(file_name)
        self.create_video_writer(file_name)
        self.video_dict = {}

    # This function validates the input video
    def check_file(self, file_name):
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
        if width > 640:
            num = float(width)/640
            height = int(height/num)
            width = int(width/num)         
        if self.rotate:
            size = (height,width)                                      # define new video frame size
        else:
            size = (width,height)
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        self.out = cv2.VideoWriter("%s_output.avi"%name ,fourcc, self.fps, size)

    # The function reads the video frame after frame
    def read_video(self, name):
        self.all_faces = {}
        prev_frame = None
        prev_faces = deque(maxlen=3)       
        frame_num = 0
        # loop to read video frame by frame
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if not ret:
                break
            faces = []
            frame_num += 1
            while frame_num < 150:
                ret, frame = self.cap.read()
                if not ret:
                    break
                faces = []
                frame_num += 1
            if frame_num > 400:
                break
            if self.rotate:
                frame = self.rotate_90(frame)                    # rotate the frame
            if len(frame) > 640:
                frame = self.resize_image(frame,int(len(frame)/640))            
            img_analizer = ImageAnalizer(frame , prev_frame, prev_faces, frame_num)
            prev_frame = frame.copy()
            img_analizer.mark_faces()
            faces = img_analizer.faces
            head = "head: %s"
            text = "eyes: %s"
            smile = ""
            nose_dir = ""
            direction = ""
            if len(faces) == 0:
                faces = []
                no_faces += 1
            else:
                d = self.calc_frame_dict(faces[0])
                self.video_dict[frame_num] = d
                nose = faces[0].get_nose()
                r_eye, l_eye = faces[0].get_eyes_center()
                self.update_centers_list(noses, nose)
                self.update_centers_list(r_eyes, r_eye)
                self.update_centers_list(l_eyes, l_eye)
                x_direct = ""
                y_direct = ""
                nose_x = ""
                nose_y = ""
                if frame_num >= 10:
                    n_x_direct, n_y_direct = self.track_object(frame,noses)
                    r_x_direct, r_y_direct = self.track_object(frame,r_eyes)
                    l_x_direct, l_y_direct = self.track_object(frame,l_eyes)
                    if n_x_direct == -1:
                        nose_x = "left"
                    elif n_x_direct == 1:
                        nose_x = "right"
                    if n_y_direct == -1:
                        nose_y = "upwards"
                    elif n_y_direct == 1:
                        nose_y = "downwards"
                    if r_x_direct == -1 or l_x_direct == -1:
                        x_direct = "left"
                    elif r_x_direct == 1 or l_x_direct == 1:
                        x_direct = "right"
                    if r_y_direct == -1 or l_y_direct == -1:
                        y_direct = "upwards"
                    elif r_y_direct == 1 or l_y_direct == 1:
                        y_direct = "downwards"
                    if x_direct != "" and y_direct != "":
                        direction = "%s-%s"%(x_direct,y_direct)
                    else:
                        direction = x_direct if x_direct != "" else y_direct
                    if nose_x != "" and nose_y != "":
                        nose_dir =  "%s-%s"%(nose_x,nose_y)
                    else:
                        nose_dir = nose_x if nose_x != "" else nose_y
                    if nose_dir != "":
                        head_move += 1
                    if direction != "":
                        eyes_move += 1
                if faces[0].get_smile() is not None:
                    smile = "smile"
                    smiles_counter += 1
                else:
                    smile = ""
                    no_smile += 1
                    if no_smile > 3:

                        no_smile = 0
                        max_smiles = max(max_smiles, smiles_counter)
                        smiles_sum += smiles_counter
                        smiles_counter = 0
                prev_faces.appendleft(faces[0])
            cv2.putText(frame, head%nose_dir, (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1)
            cv2.putText(frame, text%direction, (10, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1)
            cv2.putText(frame, smile, (10, 90), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1)
                #cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
            self.out.write(frame)
            cv2.imshow('frame', frame)             # Display the resulting frame
            if cv2.waitKey(int(self.fps)) & 0xFF == ord('q'):
                break
        f = open('%s_output.txt'%(name), 'w')  
        max_smiles = max(max_smiles, smiles_counter)  
        print >> f, "frames with no faces: ",no_faces
        print >> f, "smiles in sequence: {0}% of the frames".format(int(float(max_smiles)/frame_num*100))
        print >> f, "smiles: {0}% of the frames".format(int(float(smiles_sum)/frame_num*100))
        print >> f, "eyes moves in {0}% of the frames".format(int(float(eyes_move)/frame_num*100))
        print >> f, "head moves in {0}% of the frames".format(int(float(head_move)/frame_num*100))
        print >> f, "number of frames: ",frame_num
        f.close()      
        objects_json = json.dumps(self.video_dict)  #create jason
        f = open('%s_objects.json'%(name), 'w')
        print >> f, objects_json
        f.close()
        self.release_memory()

    def save_video(self):
        self.cap = cv2.VideoCapture(file_name)   # load video
        # loop to read video frame by frame
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if not ret:
                break
            faces = []
            frame_num += 1
            if self.rotate:
                frame = self.rotate_90(frame)                    # rotate the frame
            frame = res

            self.out.write(frame)
            cv2.imshow('frame', frame)             # Display the resulting frame
            if cv2.waitKey(int(self.fps)) & 0xFF == ord('q'):
                break

    # This function rotates a given image 90 degrees to the right
    def rotate_90(self, img):
        cv2.flip(img, 0, img)
        return cv2.transpose(img)
    
    def resize_image(self, img, num):    
        height, width, a = img.shape
        dim = (width/num, height/num)
        return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    def update_centers_list(self, list, object):
        if len(list) < 3 or object == (-1,-1):
            list.appendleft(object)
            return
        l = np.array(list)


        x = l[:,0]
        y = l[:,1]
        
        is_none = x == -1
        x = np.delete(x,np.where(is_none == True))
        y = np.delete(y,np.where(is_none == True))
        
        if len(x) < 3:
            list.appendleft(object)
            return
        x_med = int(np.median(x))
        y_med = int(np.median(y))
        d = calc_d((x_med,y_med),object)
        if d < 80:
            list.appendleft(object)
            
    def track_object(self, frame, list):
        epsilon = 5     # the minimum delta for movement
        x_direct, y_direct = 0,0
        for i in range(len(list)):
            if list[i-1] == (-1,-1) or list[i] == (-1,-1):
                continue
            if i == 1 and list[-1] is not None:
                dx = list[i-1][0] - list[-1][0]
                dy = list[i-1][1] - list[-1][1]
                if abs(dx) > epsilon:
                    x_direct = abs(dx)/dx
                if abs(dy) > epsilon:
                    y_direct = abs(dy)/dy
            thickness = min(2,int(np.sqrt(len(list) / float(i + 1))))
            cv2.line(frame, list[i - 1], list[i], (0, 0, 255), thickness)
        return x_direct,y_direct

    def calc_frame_dict(self, face):
        d = {}
        r_pupil = None
        l_pupil = None
        d['face'] = face.get_rect()
        for key,value in face.organs_dict.iteritems():
            if value != None:
                d[key] = value.get_rect()
                if key == 'r_eye':
                    r_pupil = value.get_pupil()
                    if r_pupil is not None:
                         d["r_pupil"] = r_pupil
                elif key == 'l_eye':
                    l_pupil = value.get_pupil()
                    if l_pupil is not None:
                        d["l_pupil"] = l_pupil
        return d

    def release_memory(self):        
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()