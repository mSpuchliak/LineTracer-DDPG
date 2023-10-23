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

# class Actor(nn.Module):
#     def __init__(self, state_dim, action_dim):
#         super(Actor, self).__init__()
        
#         # Shared feature extraction layers
#         self.shared_fc1 = nn.Linear(state_dim, 2500)
#         self.shared_fc2 = nn.Linear(2500, 2500)
        
#         # Separate heads for each wheel
#         self.head1 = nn.Linear(2500, action_dim)
#         self.head2 = nn.Linear(2500, action_dim)

#     def forward(self, state):
#         x = T.relu(self.shared_fc1(state))
#         x = T.relu(self.shared_fc2(x))
        
#         # Separate actions for each wheel
#         action1 = T.tanh(self.head1(x))
#         action2 = T.tanh(self.head2(x))
        
#         return action1, action2

# # Define the critic network
# class Critic(nn.Module):
#     def __init__(self, state_dim):
#         super(Critic, self).__init__()
        
#         self.fc1 = nn.Linear(state_dim, 2500)
#         self.fc2 = nn.Linear(2500, 1)

#     def forward(self, state):
#         x = T.relu(self.fc1(state))
#         value = self.fc2(x)
#         return value
    

# Define the Actor and Critic networks
class Actor(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(Actor, self).__init__()
        self.fc1 = nn.Linear(state_dim, 1000)
        self.fc2 = nn.Linear(1000,500)
        self.fc3 = nn.Linear(500, action_dim)

    def forward(self, state):
        x = T.relu(self.fc1(state))
        x = T.relu(self.fc2(x))
        return T.tanh(self.fc3(x))

class Critic(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(Critic, self).__init__()
        self.fc1 = nn.Linear(state_dim + action_dim, 1000)
        self.fc2 = nn.Linear(1000, 500)
        self.fc3 = nn.Linear(500, 1)

    def forward(self, state, action):
        x = T.cat([state, action], dim=-1)
        x = T.relu(self.fc1(x))
        x = T.relu(self.fc2(x))
        return self.fc3(x)