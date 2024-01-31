import datetime
import os
import matplotlib.pyplot as plt
from IPython import display
from statistics import mean

class Plotting:
    def __init__(self):
        self.laps_history = []
        self.speed_history = []
        self.lap_speed_history = []
        self.mean_lap_speed_history = []
        self.plt = None
    
    def add_to_laps_history(self, round_result):
        self.laps_history.append(round_result)

    def add_to_speed_history(self, round_result):
        self.speed_history.append(round_result)
    
    def add_to_lap_speed_history(self):
        self.lap_speed_history.append(mean(self.speed_history))
        self.mean_lap_speed_history.append(mean(self.lap_speed_history))
        self.speed_history.clear()

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
        plt.plot(self.lap_speed_history)
        plt.plot(self.mean_lap_speed_history)
        
        plt.show(block=False)
        plt.pause(.1)

        self.plt = plt.gcf()

    def save_graph(self):
        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"Result graph {current_datetime}.png"
        filepath = os.path.join(os.getcwd(), "Results", "Graphs", name)
        self.plt.savefig(filepath)
