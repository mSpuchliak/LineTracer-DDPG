import torch.nn as nn
import torch.nn.functional as F
import torch as T
import os
import datetime

class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, chkpt_dir='Results/Models/DQL'):
        super().__init__()
        self.linear =  nn.Linear(input_size, hidden_size)
        self.linear2 =  nn.Linear(hidden_size, output_size)
        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"neural_network_{current_datetime}_dql"
        self.chkpt_dir = chkpt_dir
        self.checkpoint_file = os.path.join(chkpt_dir, name)

    def forward(self, x):
        x = F.relu(self.linear(x))
        x = self.linear2(x)
        return x
    
    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self, load_model_name):
        name = f"neural_network_{load_model_name}_dql"
        checkpoint_file = os.path.join(self.chkpt_dir, name)
        self.load_state_dict(T.load(checkpoint_file))