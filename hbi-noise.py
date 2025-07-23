import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

innse_away  = np.load('innse_away.npy')
innse_under = np.load('innse_under.npy')

def flatten_run(run):
    '''Flatten ABC lists into one list of all channels per run'''
    return [val for chip in run for val in chip]

def plot_measurement(measurement_data, measurement_name, stream, y_axis):
    plt.figure()
    num_runs = len(measurement_data)
    norm     = Normalize(vmin=0, vmax=num_runs - 1)
    cmap     = plt.get_cmap("Greens")
    
    plt.figure(figsize=(10, 5))

    for run_num, run in enumerate(measurement_data):
        flattened = flatten_run(run)
        x_vals    = np.arange(len(flattened))
        color     = cmap(norm(run_num))
        plt.scatter(x_vals, flattened, color=color, label=f"Run {run_num}", s=10)

    plt.title(f"{serial_num} {measurement_name}, {stream} Stream")
    plt.xlabel("Channel")
    plt.ylabel(f"{y_axis}")
    plt.grid(True, axis='x', which='major', linestyle='--', alpha=0.5)

    max_x = max(len(flatten_run(run)) for run in measurement_data)
    plt.xticks(np.arange(0, max_x, 128))

    plt.savefig(f"{serial_num}-{y_axis}{stream}.pdf")

plot_measurement(innse_away, 'Noise', 'Away', 'Noise')
plot_measurement(innse_under, 'Noise', 'Under', 'Noise')
