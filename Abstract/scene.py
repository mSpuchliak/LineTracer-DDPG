from abc import ABC

class Scene(ABC):
    def __init__(self):
        self.name = str
        self.path = str
        self.starting_position = []
        self.checkpoint_1 = []
        self.checkpoint_2 = []
        self.checkpoint_3 = []
        