import cv2

class Eye:
    """description of class"""
    def __init__(self, eye, x, y):
        self.x = eye[0] + x
        self.y = eye[1] + y
        self.w = eye[2]
        self.h = eye[3]

    def mark_eye(self, frame):
        point = (self.x, self.y)
        size = (self.x+self.w, self.y+self.h)
        cv2.rectangle(frame, point, size, (0,255,0), 1)
        return frame
