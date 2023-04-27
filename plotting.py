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