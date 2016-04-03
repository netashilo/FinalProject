import cv2

class Eye:
    """description of class"""
    def __init__(self, eye, x, y):
        self.x = eye[0] + x
        self.y = eye[1] + y
        self.w = eye[2]
        self.h = eye[3]
    
    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def mark_eye(self, frame, color):
        point = (self.x, self.y)
        size = (self.x+self.w, self.y+self.h)
        cv2.rectangle(frame, point, size, color, 1)
