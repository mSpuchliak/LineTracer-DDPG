import datetime
import os
import matplotlib.pyplot as plt
from IPython import display

class Plotting:
    def __init__(self):
        self.plt = None

    def plot_laps(self, laps_history):
        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.clf()
        plt.ion()
        plt.xlabel('Number of starts')
        plt.ylabel('Has finished the round')
        plt.plot(laps_history)
        plt.show(block=False)
        plt.pause(.1)
    
    def plot_laps_and_speed(self, laps_history, lap_speed_history, mean_lap_speed_history):
        display.clear_output(wait=True)
        plt.clf()
        plt.ion()

        # Create subplot 1
        plt.subplot(2, 1, 1)
        plt.xlabel('Number of starts')
        plt.ylabel('Has finished the round')
        plt.plot(laps_history)

        # Create subplot 2
        plt.subplot(2, 1, 2)
        plt.xlabel('Number of starts')
        plt.ylabel('Average speed both wheels')
        plt.plot(lap_speed_history)
        plt.plot(mean_lap_speed_history)
        
        plt.show(block=False)
        plt.pause(.1)

        self.plt = plt.gcf()

    def save_graph(self):
        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"Result graph {current_datetime}.png"
        filepath = os.path.join(os.getcwd(), "Results", "Graphs", name)
        self.plt.savefig(filepath)
