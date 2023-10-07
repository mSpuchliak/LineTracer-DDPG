from generic_network import GenericNetwork
import torch as T
from plotting import Plotting
import torch.optim as optim

class GenericAgent(object):
    def __init__(self, input_dim, output_dim, lr=0.000005, gamma=0.99):
        self.actor = GenericNetwork(input_dim, output_dim)
        self.critic = GenericNetwork(input_dim, 1)
        self.optimizer = optim.Adam(self.actor.parameters(), lr=lr)
        self.optimizer_c = optim.Adam(self.critic.parameters(), lr=0.00001)
        self.gamma = gamma
        self.output_dim = output_dim
        self.plot = Plotting()
        self.log_probs = None

    def select_action(self, state):
        state = T.FloatTensor(state)
        mu = self.actor.forward(state)
        

        #action_probs = T.distributions.Normal(loc=mu, scale= T.abs(sigma)) 
        action_probs = T.distributions.Categorical(mu)
        probs = action_probs.sample()

        self.log_probs = action_probs.log_prob(probs)

        return probs
    
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
        actor_loss = -self.log_probs * td_error

        # Critic loss
        critic_loss = T.square(td_error)

        # Total loss
        total_loss = actor_loss + critic_loss
        total_loss= total_loss.mean()
        # Update the network
        
        total_loss.backward()
        self.optimizer.step()
        self.optimizer_c.step()

    # Plotitng of the graph.
    def check_plot(self, laps_history):
        self.plot.plot_laps(laps_history)
    