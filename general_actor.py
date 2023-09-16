class GenericActor(object):
    def __init__(self, alph, beta, input_dims, gamma =0.99, n_actions=2, layer_size=64, layer2_size=64, n_outputs=1):
        self.gamma = gamma