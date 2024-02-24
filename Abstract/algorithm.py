from abc import ABC
from pyrep import PyRep

class Algorithm(ABC):
    def __init__(self, scene, name):
        self.name = name
        self.scene = scene
        self.pyrep = PyRep()
        

        