import numpy as np
import random
import torch
from collections import deque
from DeepQLearining.epsilon import Epsilon 
from DeepQLearining.neural_network import NeuralNetwork
from DeepQLearining.trainer import Trainer
from plotting import Plotting

MAX_MEMORY = 100000
BATCH_SIZE = 10000

class Agent():
    def __init__(self):
        self.memory = deque(maxlen = MAX_MEMORY)
        self.short_memory = deque(maxlen = 11)
        self.model = NeuralNetwork(516, 2500, 3)
        self.trainer = Trainer(self.model)
        self.epsilon = Epsilon()
        self.plot = Plotting()
    
    # Select actions either by chance or by experience.
    def get_action(self, state):
        self.epsilon.update_epsilon()

        if np.random.random() < self.epsilon.value:
            action = random.randint(0, 2)
        else:
            state = torch.tensor(state, dtype= torch.float)
            actions = self.model.forward(state)
            action = torch.argmax(actions).item()

        return action
            
    # Creating a command to be executed by the robot according to the action.
    def create_command(self, action):
        if action == 0:
            command = [1, 0]

        elif action == 1:
            command = [0, 1]

        elif action == 2:
            command = [1, 1]

        else:
            command = [0, 0]

        return command

    # Prepearment to batch informatons for the bellman equasion.
    def target_memory(self, state, action, reward, new_state):
        self.short_memory.append((state, action, reward, new_state))
        self.memory.append((state, action, reward, new_state))
        state, action, reward , new_state = zip(*self.short_memory)

        self.trainer.train_step(state, action, reward, new_state, len(self.short_memory))
    
    # Use of replay memory.
    def replay_memory(self):
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = self.memory
        state, action, reward, next_state = zip(*sample)
        
        self.trainer.train_step(state, action, reward, next_state, len(sample))

    # Plotitng of the graph.
    def check_plot(self, laps_history):
        if (self.epsilon.value == self.epsilon.epsilon_min):
            self.plot.plot_laps(laps_history)
