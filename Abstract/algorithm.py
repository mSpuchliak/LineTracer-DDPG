from abc import ABC
from pyrep import PyRep

from DDPG.line_tracer import LineTracerModel

class Algorithm(ABC):
    def __init__(self, scene):
        self.scene = scene
        self.pyrep = PyRep()
        self.done = False

        