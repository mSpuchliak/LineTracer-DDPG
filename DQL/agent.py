from DQL.epsilon import Epsilon 
from DQL.neural_network import NeuralNetwork
from DQL.trainer import Trainer
from Utilities.replay_buffer import ReplayBuffer
import numpy as np
import random
import torch as T

class Agent():
    def __init__(self, input_dims, n_actions, hidden_dims, batch_size, mem_size):
        self.batch_size = batch_size
        self.model = NeuralNetwork(input_dims, hidden_dims, n_actions)
        self.trainer = Trainer(self.model)
        self.epsilon = Epsilon()
        self.memory = ReplayBuffer(mem_size, [input_dims], 1)
    
    # Select actions either by chance or by experience.
    def get_action(self, state):
        self.epsilon.update_epsilon()

        if np.random.random() < self.epsilon.value:
            action = random.randint(0, 2)
        else:
            state = T.tensor(state, dtype= T.float)
            actions = self.model.forward(state)
            action = T.argmax(actions).item()

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
    
    def learn(self, state, action, reward, new_state):
        self.memory.store_transition(state, action, reward, new_state)
        self.trainer.train_step([state], action, [reward], [new_state], 1)
    
    # Use of replay memory.
    def replay_memory(self):
        if self.memory.mem_cntr < self.batch_size:
            states, actions, rewards, states_ = self.memory.sample_buffer(self.memory.mem_cntr)
            self.trainer.train_step(states, actions, rewards, states_, self.memory.mem_cntr)
        else:
            states, actions, rewards, states_ = self.memory.sample_buffer(self.batch_size)        
            self.trainer.train_step(states, actions, rewards, states_, self.batch_size)
    
    def save_model(self):
        self.model.save_checkpoint()
    
    def load_model(self, load_model_name):
        self.model.load_checkpoint(load_model_name)