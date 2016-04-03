import cv2
from CascadeDictionary import d
from Eye import Eye
from Smile import Smile
from FaceOrgan import FaceOrgan

class Face:
    """description of class"""   
    def __init__(self, face, img):
        self.x = face[0]
        self.y = face[1]
        self.w = face[2]
        self.h = face[3]
        self.right_eye = None
        self.left_eye = None
        self.smile = None
        self.nose = None
        self.mouth = None
        self.eye_detection(img)
        self.smile_detection(img)
        self.face_organ_detection(img)
                
    def get_rect(self):
        return (self.x, self.y, self.w, self.h)
    # This function detect the eyes in a given face-rectangle and marks it with a rectangle
    def eye_detection(self, img):
        x1 = self.x
        x2 = x1 + self.w
        y1 = self.y
        y2 = y1 + self.h*2/3
        face_rect = img[y1:y2, x1:x2]
        eyes = d.get('haarcascade_eye').detectMultiScale(face_rect, 1.2, 2)
        for eye in eyes:
            if eye[0] < self.w/2:
                if self.right_eye == None:
                    self.right_eye = Eye(eye, self.x, self.y)
            else:
                if self.left_eye == None:
                    self.left_eye = Eye(eye, self.x, self.y)
            if self.right_eye != None and self.left_eye != None:
                return

    def smile_detection(self, img):
        x1 = self.x
        x2 = x1 + self.w
        y1 = self.y + self.h/2
        y2 = self.y + self.h
        face_rect = img[y1:y2, x1:x2]
        smiles = d.get('haarcascade_smile').detectMultiScale(face_rect, 2, 4)
        if len(smiles) != 0:
            self.smile = Smile(smiles[0], self.x, self.y, self.h)

    def face_organ_detection(self, img):
        x1 = self.x
        x2 = x1 + self.w
        y1 = max(self.y, 0)
        y2 = self.y + self.h
        face_rect = img[y1:y2, x1:x2]
        mouthes = d.get('haarcascade_mcs_mouth').detectMultiScale(face_rect, 2, 4)
        noses = d.get('haarcascade_mcs_nose').detectMultiScale(face_rect, 1.5, 2)
        if len(mouthes) != 0:
            self.mouth = FaceOrgan(mouthes[0], self.x, self.y)
        if len(noses) != 0:
            self.nose = FaceOrgan(noses[0], self.x, self.y)

    def mark_face(self, frame, color):
        point = (self.x, self.y)
        size = (self.x+self.w, self.y+self.h)
        cv2.rectangle(frame, point, size, color, 1)

        if self.right_eye != None:
            self.right_eye.mark_eye(frame,color)
        if self.left_eye != None:
            self.left_eye.mark_eye(frame,color)
        if self.smile != None:
            self.smile.mark_smile(frame,color)
#        if self.mouth != None:
#            self.mouth.mark_organ(frame,(0,255,255))
        if self.nose != None:
            self.nose.mark_organ(frame,(255,255,0))