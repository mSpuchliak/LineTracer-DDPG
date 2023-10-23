from generic_network import GenericNetwork, Actor, Critic
import torch as T
from plotting import Plotting
import torch.optim as optim

class GenericAgent(object):
    def __init__(self, input_dim, output_dim, lr=0.000005, gamma=0.99):
        self.actor = Actor(input_dim, output_dim)
        self.critic = Critic(input_dim)
        self.optimizer = optim.Adam(self.actor.parameters(), lr=lr)
        self.optimizer_c = optim.Adam(self.critic.parameters(), lr=0.00001)
        self.gamma = gamma
        self.output_dim = output_dim
        self.plot = Plotting()
        self.log_probs = []

    def select_action(self, state):
        state = T.FloatTensor(state)

        action, action2 = self.actor.forward(state) 
        
        action_probs = T.distributions.Normal(loc=action[0], scale= T.abs(action[1])) 
        action2_probs = T.distributions.Normal(loc=action2[0], scale= T.abs(action2[1])) 
        
        probs = action_probs.sample(sample_shape=T.Size([1]))
        probs2 = action2_probs.sample(sample_shape=T.Size([1]))

        action_ = T.tanh(probs)
        action2_ = T.tanh(probs2)

        self.log_probs = []
        self.log_probs.append(action_)
        self.log_probs.append(action2_)
        
        return action_, action2_
        
    def update(self, state, reward, next_state):
        self.optimizer.zero_grad()
        self.optimizer_c.zero_grad()

        state = T.FloatTensor(state)
        next_state = T.FloatTensor(next_state)
        reward = T.FloatTensor([reward])

        # Compute the TD error
        critic_next_state = self.critic(next_state)
        critic_state = self.critic(state)    

        td_error = reward + self.gamma * critic_next_state - critic_state

        # Actor loss
        actor_loss = 0

        for prob in self.log_probs:
            h = -prob*td_error
            actor_loss += h

        # Critic loss
        critic_loss = T.square(td_error)

        # Total loss
        total_loss = actor_loss + critic_loss
        total_loss = total_loss.mean()
        # Update the network
        print(total_loss)
        
        total_loss.backward()
        self.optimizer.step()
        self.optimizer_c.step()

    # Plotitng of the graph.
    def check_plot(self, laps_history):
        self.plot.plot_laps(laps_history)

import torch.nn as nn

class MADDPGAgent:
    def __init__(self, state_dim, action_dim):
        self.actor = Actor(state_dim, action_dim)
        self.plot = Plotting()
        self.critic = Critic(state_dim, action_dim)  # Joint state for both agents
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=0.00001)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=0.00001)
        self.action = None

    def select_action(self, state):
        state = T.FloatTensor(state)
        self.action =  self.actor(state)

        action_probs = T.distributions.Normal(loc=self.action[0], scale= T.abs(self.action[1])) 
        
        probs = action_probs.sample(sample_shape=T.Size([1]))

        action_ = T.tanh(probs)

        return action_

    def update(self, state, action, reward, next_state):
        state = T.FloatTensor(state)
        next_state = T.FloatTensor(next_state)
        reward = T.FloatTensor([reward])
        action = T.FloatTensor(action)

        # critic_next_state = self.critic(next_state)
        # critic_state = self.critic(state)    

        # td_error = reward + 0.99 * critic_next_state - critic_state

        # # Critic loss
        # critic_loss = T.square(td_error)

        # # Update the actor
        # actor_loss = - action * td_error
        
        # self.actor_optimizer.zero_grad()
        # self.critic_optimizer.zero_grad()

        # (critic_loss+actor_loss).backward()

        # self.actor_optimizer.step()
        # self.critic_optimizer.step()


        Q_target = reward + 0.99 * self.critic(next_state, self.actor(next_state))
        Q_current = self.critic(state, self.action)
        critic_loss = nn.MSELoss()(Q_current, Q_target)
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # Update the actor
        actor_loss = -self.critic(state, self.actor(state)).mean()
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

    # Plotitng of the graph.
    def check_plot(self, laps_history):
        self.plot.plot_laps(laps_history)