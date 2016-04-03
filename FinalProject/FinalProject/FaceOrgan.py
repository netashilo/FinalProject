import cv2

class FaceOrgan(object):

    """description of class"""
    def __init__(self, organ, x, y):
        self.x = organ[0] + x
        self.y = organ[1] + y
        self.w = organ[2]
        self.h = organ[3]

    def mark_organ(self, frame, color):
        point = (self.x, self.y)
        size = (self.x+self.w, self.y+self.h)
        cv2.rectangle(frame, point, size, color, 1)
