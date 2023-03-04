import numpy as np
import random
import torch
from collections import deque
from epsilon import Epsilon 
from neuralNetwork import NeuralNetwork
from trainer import Trainer

MAX_MEMORY = 100000
BATCH_SIZE = 10000

class Agent():
    def __init__(self):
        self.memory = deque(maxlen = MAX_MEMORY)
        self.shortMemory = deque(maxlen = 11)
        self.model = NeuralNetwork(512 ,2500, 3)
        self.trainer = Trainer(self.model)
        self.epsilon = Epsilon()
    
    def getAction(self, state):
        self.epsilon.update_epsilon()
        print("Epsilon: ", self.epsilon.value)
        if np.random.random() < self.epsilon.value:
            action = random.randint(0, 2)
        else:
            state = torch.tensor(state, dtype= torch.float)
            actions = self.model.forward(state)
            action = torch.argmax(actions).item()
        return action

    def targetMemory(self, state, action, reward, newState):
        self.shortMemory.append((state, action, reward, newState))
        self.memory.append((state, action, reward, newState))
        state, action, reward , newState = zip(*self.shortMemory)
        self.trainer.trainStep(state, action, reward, newState, len(self.shortMemory))
    
    def replayMemory(self):
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = self.memory
        state, action, reward, next_state = zip(*sample)
        self.trainer.trainStep(state, action, reward, next_state, len(sample))

