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
        x = T.softmax(self.fc3(x), dim=-1)

        return x