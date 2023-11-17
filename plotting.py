import matplotlib.pyplot as plt
from IPython import display

class Plotting:
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
    
    def plot_laps_and_speed(self, laps_history1, speed_history):
        display.clear_output(wait=True)
        plt.clf()
        plt.ion()

        # Create subplot 1
        plt.subplot(2, 1, 1)
        plt.xlabel('Number of starts')
        plt.ylabel('Has finished the round')
        plt.plot(laps_history1)

        # Create subplot 2
        plt.subplot(2, 1, 2)
        plt.xlabel('Number of starts')
        plt.ylabel('Has finished the round')
        plt.plot(speed_history)

        plt.show(block=False)
        plt.pause(.1)