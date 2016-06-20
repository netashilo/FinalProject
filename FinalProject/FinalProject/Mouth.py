from FaceOrgan import FaceOrgan

class Mouth(FaceOrgan):
    """description of class"""
    def __init__(self, mouth, is_smile):
        FaceOrgan.__init__(self, mouth, "mouth")
        self.is_smile = is_smile





