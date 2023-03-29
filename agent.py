import numpy as np
import random
import torch
from collections import deque
from epsilon import Epsilon 
from neuralNetwork import NeuralNetwork
from trainer import Trainer
from plotting import Plotting

MAX_MEMORY = 100000
BATCH_SIZE = 10000

class Agent():
    def __init__(self):
        self.memory = deque(maxlen = MAX_MEMORY)
        self.short_memory = deque(maxlen = 11)
        self.model = NeuralNetwork(515 , 2500, 3)
        self.trainer = Trainer(self.model)
        self.epsilon = Epsilon()
        self.plot = Plotting();
    
    def get_action(self, state):
        self.epsilon.update_epsilon()
        #print("Epsilon: ", self.epsilon.value)
        if np.random.random() < self.epsilon.value:
            action = random.randint(0, 2)
        else:
            state = torch.tensor(state, dtype= torch.float)
            actions = self.model.forward(state)
            action = torch.argmax(actions).item()
        return action
    
    def create_command(self, action):
        if action == 0:
            command = [1, 0]
        elif action == 1:
            command = [0, 1]
        elif action == 2:
            command = [1, 1]

        return command
    
    def normalize_state(self, sensor_state):
        state = []
        for rows in sensor_state:
            for pixel in rows:
                if(pixel[0] == 1.0):
                    state.append(1)
                else:
                    state.append(0)
        return state

    def targetMemory(self, state, action, reward, new_state):
        self.short_memory.append((state, action, reward, new_state))
        self.memory.append((state, action, reward, new_state))
        state, action, reward , new_state = zip(*self.short_memory)
        self.trainer.trainStep(state, action, reward, new_state, len(self.short_memory))
    
    def replayMemory(self):
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = self.memory
        state, action, reward, next_state = zip(*sample)
        self.trainer.trainStep(state, action, reward, next_state, len(sample))

    def check_plot(self, laps_history):
        if (self.epsilon.value == self.epsilon.epsilon_min):
            self.plot.plot_laps(laps_history)
