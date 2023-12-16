import matplotlib.pyplot as plt
from IPython import display
from statistics import mean

class Plotting:
    def __init__(self):
        self.laps_history = []
        self.lap_speed_history = []
        self.avg_lap_speed_history = []
    
    def add_to_laps_history(self, round_result):
        self.laps_history.append(round_result)

    def add_to_lap_speed_history(self, round_result):
        self.lap_speed_history.append(round_result)
    
    def add_to_avg_lap_speed_history(self):
        self.avg_lap_speed_history.append(mean(self.lap_speed_history))
        self.lap_speed_history.clear()

    def plot_laps(self):
        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.clf()
        plt.ion()
        plt.xlabel('Number of starts')
        plt.ylabel('Has finished the round')
        plt.plot(self.laps_history)
        plt.show(block=False)
        plt.pause(.1)
    
    def plot_laps_and_speed(self):
        display.clear_output(wait=True)
        plt.clf()
        plt.ion()

        # Create subplot 1
        plt.subplot(2, 1, 1)
        plt.xlabel('Number of starts')
        plt.ylabel('Has finished the round')
        plt.plot(self.laps_history)

        # Create subplot 2
        plt.subplot(2, 1, 2)
        plt.xlabel('Number of starts')
        plt.ylabel('Average speed both wheels')
        plt.plot(self.avg_lap_speed_history)

        plt.show(block=False)
        plt.pause(.1)