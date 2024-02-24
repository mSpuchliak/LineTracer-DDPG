import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from DQL.neural_network import NeuralNetwork

class Trainer:
    def __init__(self, model: NeuralNetwork = None):
        self.gamma = 0.9
        self.learnig_rate = 0.0001
        self.model = model
        self.optimazer = optim.Adam(model.parameters(), lr = self.learnig_rate)
        self.mse = nn.MSELoss()
    
    # One training step with the calculation of the Bellman equation, loss and update Neural Network with backpropagation.
    def train_step(self, state, action, reward, next_state, batch_size): 
        state = torch.tensor(state, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        batch_index = np.arange(batch_size, dtype=np.int32)
   
        q_value = self.model.forward(state)[batch_index, action]

        q_new = reward + self.gamma * torch.max(self.model.forward(next_state))

        self.optimazer.zero_grad()
        loss = self.mse(q_new, q_value)
        loss.backward()
        self.optimazer.step()
