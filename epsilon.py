class Epsilon:
    def __init__(self, epsilon_min: float = 0.01, epsilon_dec: float = 0.000005, epsilon: float = 1):
        self.epsilon_min = epsilon_min
        self.epsilon_dec = epsilon_dec
        self.value = epsilon
        self.start_epsilon = epsilon

    def update_epsilon(self):
        if self.value > self.epsilon_min:
            self.value -= self.epsilon_dec 
        else:
            self.value = self.epsilon_min
