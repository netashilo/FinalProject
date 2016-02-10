import cv2
from CascadeDictionary import d
from Eye import Eye
from Smile import Smile

class Face:
    """description of class"""   
    def __init__(self, face, img):
        self.x = face[0]
        self.y = face[1]
        self.w = face[2]
        self.h = face[3]
        self.eyes = []
        self.smile = None
        self.eye_detection(img)
        self.smile_detection(img)
                
    def get_rect(self):
        return (self.x, self.y, self.w, self.h)
    # This function detect the eyes in a given face-rectangle and marks it with a rectangle
    def eye_detection(self, img):
        x1 = self.x
        x2 = x1 + self.w
        y1 = self.y
        y2 = y1 + self.h*2/3
        face_rect = img[y1:y2, x1:x2]
        eyes = d.get('haarcascade_eye').detectMultiScale(face_rect, 1.9, 2)
        i = 0
        for eye in eyes:
            i += 1
            self.eyes.append(Eye(eye, self.x, self.y))
            if i == 2:
                break

    def smile_detection(self, img):
        x1 = self.x
        x2 = x1 + self.w
        y1 = self.y + self.h/2
        y2 = self.y + self.h
        face_rect = img[y1:y2, x1:x2]
        smiles = d.get('haarcascade_smile').detectMultiScale(face_rect, 2, 4)
        if len(smiles) != 0:
            self.smile = Smile(smiles[0], self.x, self.y, self.h)


    def mark_face(self, frame, color):
        point = (self.x, self.y)
        size = (self.x+self.w, self.y+self.h)
        cv2.rectangle(frame, point, size, color, 1)
        for eye in self.eyes:
            frame = eye.mark_eye(frame,color)
        if self.smile != None:
            self.smile.mark_smile(frame,color)
        