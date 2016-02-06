import cv2

class Smile:
    """description of class"""
    def __init__(self, smile, x, y, h):
        self.x = smile[0] + x
        self.y = smile[1] + y + h/2
        self.w = smile[2]
        self.h = smile[3]

    def mark_smile(self, frame):
        point = (self.x, self.y)
        size = (self.x+self.w, self.y+self.h)
        cv2.rectangle(frame, point, size, (0,255,0), 1)
