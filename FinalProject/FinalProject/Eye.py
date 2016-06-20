from FaceOrgan import FaceOrgan
import cv2
import numpy as np
import math

class Eye(FaceOrgan):
    """description of class"""
    def __init__(self, frame, eye, side):
        FaceOrgan.__init__(self, eye, "eye")
        self.side = side    #'r' for right eye and 'l' for left eye
        self.find_pupil(frame)

    def find_pupil(self,frame):
        N = 6
        (x,y,w,h) = self.get_rect()
        center = (x+w/2,y+h/2)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        eye_rect = gray[y:y+h,x:x+w] 
        #print "before: ",np.average(np.array(eye_rect))
        #mask = np.zeros_like(eye_rect)
        
        equ = cv2.equalizeHist(eye_rect)
        #print "equ: ",np.average(np.array(equ))

        
        #print "after: ", np.average(np.array(mask))
        #mask = cv2.medianBlur(mask, 3)
        #mask = cv2.GaussianBlur(mask,(3,3),0)
        
        c = np.array(equ)
        med = np.median(c)
        avg = np.average(c)
        bin = np.zeros_like(equ)
        c = np.array(eye_rect)
        med = np.median(c)
        avg = np.average(c)
        bin = np.zeros_like(equ)
        cv2.threshold(equ,  avg/6, 255, cv2.THRESH_BINARY, bin)
        #res = np.hstack((eye_rect,equ)) #stacking images side-by-side
        #cv2.imshow(self.side,res)

        #cv2.imshow("eye",equ)
        points = []
        med_points = []
        for i in range(len(bin)):
            for j in range(len(bin[0])):
                if bin[i,j] == 0:
                    points.append((x+j,y+i))
                    if (h/4<i<3*h/4) and (w/4<j<3*w/4):
                        med_points.append((x+j,y+i))
        points = np.array(points)
        med_points = np.array(med_points)
        if len(med_points) == 0:
            return
        x = med_points[:,0]
        y = med_points[:,1]
        x_med = int(np.median(x))
        y_med = int(np.median(y))
        x = points[:,0]
        y = points[:,1]
        x = abs(x - x_med) < w/5
        y = abs(y - y_med) < w/5
        points = points[x == True]
        y = y[x==True]
        points = points[y==True]
        if len(points) > 0:
            (x,y),radius = cv2.minEnclosingCircle(points)
            self.center = (int(x),int(y))
            self.radius = int(radius)
          
    def get_pupil(self):
        try:
            return self.center,self.radius              # return pupil center
        except:
            return None   # if we didnt found a pupil
                
    def mark_organ(self, frame, color):
        FaceOrgan.mark_organ(self,frame,color)
        try:            
            cv2.circle(frame,self.center,self.radius,(0,255,0),1)
        except:
            return

def calc_d(point1, point2):
    x = point1[0] - point2[0]
    y = point1[1] - point2[1]
    return math.hypot(x,y)        