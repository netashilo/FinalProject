
class OrgansTracker(object):
    """description of class"""
    def __init__(self):
        l_eyes = deque(maxlen=15)
        r_eyes = deque(maxlen=15)
        noses = deque(maxlen=15)
        no_face = 0
        no_smile = 0
        smiles_in_sequence = 0#smiles_counter
        max_smiles_in_sequence = 0
        smiles_sum = 0
        head_move = 0
        eyes_move = 0


