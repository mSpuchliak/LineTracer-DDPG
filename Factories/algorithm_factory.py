from DDPG.ddpg import DDPG
from DQL.deep_q_learning import DQL

class AlgorithmFactory():
    def __init__(self, scene):
        self.scene = scene

    def choose_algorithm(self, algorithm_name):
        if (algorithm_name == 'DDPG'):
            return DDPG(self.scene, algorithm_name)

        if (algorithm_name == 'DQL'):
            return DQL(self.scene, algorithm_name)
        
