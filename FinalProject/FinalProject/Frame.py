import numpy as np
from CascadeDictionary import d
from Face import Face

class Frame:
    """description of class"""
    def __init__(self, img, prev_frame):
        self.img = img
        self.prev_frame = prev_frame
        self.faces = []
        self.face_detection()

    # This function detect frontal/profile-faces in a given image and marks it with a rectangle
    def face_detection(self):
        faces = d.get('haarcascade_frontalface_default').detectMultiScale(self.img, 1.48, 2)
        p_faces = d.get('haarcascade_profileface').detectMultiScale(self.img, 1.85, 2)
        if len(faces) == 0:
            faces = p_faces
        elif len(p_faces) != 0:
            faces = np.concatenate((faces, p_faces), 0)
        for face in faces:
            self.faces.append(Face(face, self.img))

    def mark_faces(self):
        for face in self.faces:
            face.mark_face(self.img)
            
