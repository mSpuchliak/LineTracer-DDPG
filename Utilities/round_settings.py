from statistics import mean
from Utilities.plotting import Plotting

class RoundSettings:
    def __init__(self, scene_name, alg_name):
        self.scene_name = scene_name
        self.alg_name = alg_name
        
        self.max_rounds = 400
        self.done = False
        self.round_done = False
        self.finished_rounds_count = 0 

        self.plot = Plotting()
        self.laps_history = []
        self.speed_history = []
        self.lap_speed_history = []
        self.mean_lap_speed_history = []
        self.reward_history = []
        self.mean_reward_history = []
        self.iteration_counter_history = []

        self.iteration_counter = 0
        self.iteration_incrementer = 0.05
        self.iteration_counter_max = 100

    def get_norm_iteration_counter(self):
        return (self.iteration_counter/self.iteration_counter_max)
    
    def update_iteration_counter(self):
        if self.iteration_counter < self.iteration_counter_max:
            self.iteration_counter += self.iteration_incrementer

    def reset_iteration_counter(self):
        self.iteration_counter_history.append(self.iteration_counter)
        self.iteration_counter = 0

    def add_to_laps_history(self, round_result):
        self.laps_history.append(round_result)

    def add_to_speed_history(self, round_result):
        self.speed_history.append(round_result)
    
    def add_to_lap_speed_history(self):
        self.lap_speed_history.append(mean(self.speed_history))
        self.mean_lap_speed_history.append(mean(self.lap_speed_history))
        self.speed_history.clear()
    
    def add_to_reward_history(self, reward):
        self.reward_history.append(reward)

    def add_to_mean_reward_history(self):
        self.mean_reward_history.append(mean(self.reward_history))
        self.reward_history.clear()

    def check_finished_rounds_count(self):
        self.finished_rounds_count += 1    

        if (self.finished_rounds_count == self.max_rounds):
            self.done = True
            self.save_graph()
    
    def check_round_done(self):
        if(self.round_done):
            self.round_done = False
            self.add_to_lap_speed_history()
            self.add_to_mean_reward_history()
            self.reset_iteration_counter()
            
            if(self.finished_rounds_count == 100 or
               self.finished_rounds_count == 200 or
               self.finished_rounds_count == 300 or
               self.finished_rounds_count == 398 or
               self.finished_rounds_count == 399 or
               self.finished_rounds_count == 500):

                self.plot.plot_laps_and_speed(self.laps_history, self.lap_speed_history, self.mean_lap_speed_history, self.mean_reward_history, self.iteration_counter_history )
            self.check_finished_rounds_count()
            return True
        
        return False

    def check_round_done_dql(self):
        if(self.round_done):
            self.plot.plot_laps(self.laps_history)
            self.round_done = False
            return True
        
        return False
    
    def save_graph(self):
        self.plot.save_graph(self.scene_name, self.alg_name)