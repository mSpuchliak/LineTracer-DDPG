class IterationCounter():
    def __init__(self):
        self.value = 0
        self.iteration_incrementer = 0.1
        self.iteration_counter_max = 100

    def get_norm_iteration_counter(self):
        return (self.value/self.iteration_counter_max)
    
    def update_iteration_counter(self):
        if self.value < self.iteration_counter_max:
            self.value += self.iteration_incrementer

    def reset_iteration_counter(self):
        self.value = 0