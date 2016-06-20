import math
import cv2
from CascadeDictionary import d
from Eye import Eye
from Nose import Nose
from Mouth import Mouth
import time

class Face:
    """description of class"""   
    def __init__(self, face, img, prev_faces,color):
        self.img = img
        self.x = min(max(face[0],0),len(img[0])-1)
        self.y = min(max(face[1],0), len(img)-1)
        self.w = face[2]+min(face[0],0)
        self.h = face[3]+min(face[1],0)
        self.color = color
        self.organs_dict = {"r_eye":None, "l_eye":None, "smile":None, "nose":None, "mouth":None}
        self.organs_counter = 0
        p_nose, p_r_eye, p_l_eye = self.get_prev_organs(prev_faces)
            #cv2.circle(img,p_nose,1,(0,0,0),3)
        self.nose_detection(p_nose,img)
        self.eye_detection(p_r_eye, p_l_eye)
        if self.organs_dict["nose"] is not None or (self.organs_dict["r_eye"] is not None and self.organs_dict["l_eye"] is not None):
            self.smile_detection()

    def get_prev_organs(self, prev_faces):
        if prev_faces == []:
            return None,None,None
        nose, r_eye, l_eye = [None]*3
        for i in range(len(prev_faces)):
            if nose is None:
                try:
                    nose = prev_faces[i].organs_dict["nose"].get_center()
                except:
                    nose = None
            if r_eye is None:
                try:
                    r_eye = prev_faces[i].organs_dict["r_eye"].get_center()
                except:
                    r_eye = None
            if l_eye is None:
                try:
                    l_eye = prev_faces[i].organs_dict["l_eye"].get_center()
                except:
                    l_eye = None        
        if nose is not None:
            self.center = nose
        elif r_eye is not None and l_eye is not None:
            self.center = (l_eye[0]+(l_eye[0] - r_eye[0])/2, (r_eye[1]+l_eye[1])/2)
        else:
            self.center = (self.x+self.w/2, self.y+self.h/2)
        return nose,r_eye,l_eye           
    def get_rect(self):
        return (self.x, self.y, self.w, self.h)


    # This function detect the eyes in a given face-rectangle and marks it with a rectangle
    def eye_detection(self, p_r_eye, p_l_eye):
        x1 = self.x
        x2 = x1 + self.w
        y1 = self.y
        y2 = y1 + self.h*2/3

        self.eye_rect = self.img[y1:y2, x1:x2]
        #eyes1 = d.get('haarcascade_mcs_eyepair_big').detectMultiScale(self.eye_rect, 1.2, 1)
        eyes = d.get('haarcascade_eye').detectMultiScale(self.eye_rect, 1.2, 1)
        
        for eye in eyes:
            eye[0] += x1
            eye[1] += y1
            #print "eye_w/face_w: %d"%(int(self.w/eye[2]))
        r_eye = self.search_eye(eyes,p_r_eye,"r")
        l_eye = self.search_eye(eyes,p_l_eye,"l")
        if r_eye is not None:
            self.organs_dict["r_eye"] = Eye(self.img,r_eye,'r')
            self.organs_counter += 1
        if l_eye is not None:
            self.organs_dict["l_eye"] = Eye(self.img,l_eye,'l')
            self.organs_counter += 1
    
    def search_eye(self, eyes, prev_eye, side):
        try:
            nose = self.organs_dict["nose"]
            center = nose.get_center()
        except:
            center = self.center
        new_eye = None
        s = self.w*self.h
        d = self.w
        for eye in eyes:
            x,y,w,h = eye.ravel()
            eye_center = (x+w/2,y+h/2)
            if nose is not None and self.is_contain_point(nose.get_rect(),eye_center):
               continue
            if prev_eye is not None:
                if self.is_contain_point(eye.ravel(),prev_eye):
                    new_d = calc_d(eye_center,prev_eye)
                    if new_d < w/2 and new_d < d:
                        d = new_d
                        new_eye = eye
            else: 
                if eye_center[1] < center[1] and calc_d(eye_center,center) > w/2:
                    if side == 'r':
                        is_side = eye_center[0] < center[0]
                    else:                    
                        is_side = eye_center[0] > center[0]
                    if is_side and w*h < s:
                        new_eye = eye
                        s = w*h
                else:
                    cv2.circle(self.img,(x+w/2,y+h/2),3,(0,0,255))
        return new_eye

    def is_contain_point(self, rect, point):
        x,y,w,h = rect
        if x < point[0] < x+w:
            if y < point[1] < y+h:
                return True
        return False

    def nose_detection(self, prev_nose,frame):
        N = 6
        distance = self.h
        s = self.w*self.h
        x1,y1,x2,y2 = self.nose_rect(N) 
        nose_rect = self.img[y1:y2, x1:x2]     
 
        noses = d.get('haarcascade_mcs_nose').detectMultiScale(nose_rect, 1.2, 1)
        index = 0
        for i,nose in enumerate(noses):
            nose[0] += x1
            nose[1] += y1

        nose_d = self.w/2
        new_nose = None
        for nose in noses:
            x,y,w,h = nose.ravel()
            nose_center = (x+w/2,y+h/2)
            if prev_nose is not None:
                if self.is_contain_point((x,y,w,h),prev_nose):
                    new_d = calc_d(nose_center,prev_nose)
                    if new_d < nose_d:
                        nose_d = new_d
                        new_nose = nose
            elif nose_d == self.w/2:
                new_distance = abs(self.center[1] - y)
                if new_distance < distance:
                    new_nose = nose
                    distance = new_distance
        if new_nose is not None:
            self.organs_dict["nose"] = Nose(new_nose)
            self.organs_counter += 1
        #cv2.imshow("nose",nose_rect)
    
    def nose_rect(self,N):
        x1=self.x+int(self.w/N)
        y1=self.y+int(self.h/N)
        x2=x1+int((N-2)*self.w/N)
        y2=y1+int((N-2)*self.h/N)
        return x1,y1,x2,y2
    
    def smile_detection(self):
        x1,y1,x2,y2 = self.smile_rect()
        smile_rect = self.img[y1:y2, x1:x2]
        smiles = d.get('haarcascade_smile').detectMultiScale(smile_rect, 1.8,2)
        #mouthes = d.get('haarcascade_mcs_mouth').detectMultiScale(smile_rect, 1.5, 2)
        i = None
        if len(smiles) != 0:
            i = self.check_mouth_distance(smiles, x1, y1)
        if i != None:
            self.organs_dict["smile"] = Mouth(smiles[i],True)
            #self.organs_counter += 1
        #i = None
        #if len(mouthes) != 0:
        #    i = self.check_mouth_distance(mouthes, x1, y1)
        #if i != None:
        #    self.organs_dict["mouth"] = Mouth(mouthes[i],False)
#            self.organs_counter += 1

    def smile_rect(self):
        x1=self.x+int(self.w/5)
        y1=self.y+int(self.h/2)
        x2=x1+int(self.w*3/5)
        y2=y1+self.h/2
        return x1,y1,x2,y2

    def check_mouth_distance(self, list, x1, y1):
        try:
            nose = self.organs_dict["nose"]
            x,y,w,h = nose.get_rect()
            center = nose.get_center()
            d = h
            N = w
        except:
            center = self.center
            d = self.h/4
            N = self.w/4
        epsilon = 0.05
        index = None
        for i,mouth in enumerate(list):
            mouth[0] += x1
            mouth[1] += y1
            x,y,w,h = mouth.ravel()
            if nose is not None:
                if self.is_contain_point(nose.get_rect(),(x,y)):
                    continue
            dx = abs(x - center[0])

            if y > center[1] and dx < N: 
                smile_center = (x+w/2, y+h/2)
                new_d = calc_d(center, smile_center)
                if new_d < d or abs(new_d-d) < epsilon:
                    index = i
                    d = new_d
        return index

    def get_nose(self):
        try:
            return self.organs_dict["nose"].get_center()
        except:
            return (-1,-1)

    def get_eyes_center(self):
        try:
            r_center = self.organs_dict["r_eye"].get_center()
        except:
            r_center = (-1,-1)
        try:
            l_center = self.organs_dict["l_eye"].get_center()
        except:
            l_center = (-1,-1)
        return r_center,l_center

    def get_smile(self):
        try:
            return self.organs_dict["smile"].get_center()
        except:
            return None

    def mark_face(self, frame, color):
        point = (self.x, self.y)
        size = (self.x+self.w, self.y+self.h)
        cv2.rectangle(frame, point, size, self.color, 1)

        if self.organs_dict["r_eye"] != None:
            self.organs_dict["r_eye"].mark_organ(frame,color)
        if self.organs_dict["l_eye"] != None:
            self.organs_dict["l_eye"].mark_organ(frame,color)
        if self.organs_dict["smile"] != None:
            self.organs_dict["smile"].mark_organ(frame,(0,255,255))
        #if self.organs_dict["mouth"] != None:
        #    self.organs_dict["mouth"].mark_organ(frame,(255,0,255))
        if self.organs_dict["nose"] != None:
            self.organs_dict["nose"].mark_organ(frame,(255,255,0))

def calc_d(point1, point2):
    x = point1[0] - point2[0]
    y = point1[1] - point2[1]
    return math.hypot(x,y)