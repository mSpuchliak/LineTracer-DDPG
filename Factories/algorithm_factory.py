from DDPG.ddpg import DDPG
from DeepQLearining.deep_q_learning import DeepQLearining

class AlgorithmFactory():
    def __init__(self, scene):
        self.scene = scene

    def choose_algorithm(self, algorithm_name):
        if (algorithm_name == 'DDPG'):
            return DDPG(self.scene)

        if (algorithm_name == 'DQL'):
            return DeepQLearining(self.scene)
        
