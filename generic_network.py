import torch.nn as nn
import torch as T

class GenericNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(GenericNetwork, self).__init__()
        self.policy_action_value = []
        self.fc1 = nn.Linear(state_dim, 2500)
        self.fc2 = nn.Linear(2500, 516)
        self.fc3 = nn.Linear(516, action_dim)
    
    def forward(self, state):
        x = T.relu(self.fc1(state))
        x = T.relu(self.fc2(x))
        x = self.fc3(x)

        return x

class CustomActivation(nn.Module):
    def __init__(self, lower_bound, upper_bound):
        super(CustomActivation, self).__init__()
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def forward(self, x):
        sigmoid_output = T.sigmoid(x)
        scaled_output = (self.upper_bound - self.lower_bound) * sigmoid_output + self.lower_bound
        
        return scaled_output
    

