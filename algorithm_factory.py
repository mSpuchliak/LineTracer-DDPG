from Algorithms.actor_critic import ActorCritic
from Algorithms.deep_q_learning import DeepQLearining

class AlgorithmFactory():
    def choose_algorithm(self, algorithm_name):
        if (algorithm_name == 'ActorCritic'):
            algorithm = ActorCritic()
            algorithm.start()

        if (algorithm_name == 'DeepQLearining'):
            algorithm = DeepQLearining()
            algorithm.start()
        
