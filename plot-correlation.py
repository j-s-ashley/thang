import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

serial_num   = '20USBHX2002884' # used for naming

hbi_gain_away   = np.load('hbi_gain_away.npy')
hbi_gain_under  = np.load('hbi_gain_under.npy')
hbi_innse_away  = np.load('hbi_innse_away.npy')
hbi_innse_under = np.load('hbi_innse_under.npy')

tc_gain_away   = np.load('tc_gain_away.npy')
tc_gain_under  = np.load('tc_gain_under.npy')
tc_innse_away  = np.load('tc_innse_away.npy')
tc_innse_under = np.load('tc_innse_under.npy')

def flatten_run(run):
    '''Flatten ABC lists into one list of all channels per run'''
    return [val for chip in run for val in chip]

def plot_measurement(hbi_data, tc_data, measurement_name, stream):
    plt.figure()
    num_runs = len(hbi_data)
    norm     = Normalize(vmin=0, vmax=num_runs - 1)
    cmap     = plt.get_cmap("Greens")
    
    plt.figure(figsize=(10, 5))

    for run_num, (hbi_run, tc_run) in enumerate(zip(hbi_data, tc_data)):
        hbi_flat = flatten_run(hbi_run)
        tc_flat  = flatten_run(tc_run)
        color    = cmap(norm(run_num))
        plt.scatter(hbi_flat, tc_flat, color=color, label=f"Run {run_num}", s=10)

    plt.title(f"{serial_num} {measurement_name}, {stream} Stream HBI vs TC Correlation")
    plt.xlabel(f"HBI {measurement_name}")
    plt.ylabel(f"TC {measurement_name}")
    plt.grid()

    plt.savefig(f"{serial_num}-{measurement_name}-{stream}-correlation.pdf")

plot_measurement(hbi_gain_away, tc_gain_away, 'gain', 'away')
plot_measurement(hbi_gain_under, tc_gain_under, 'gain', 'under')
plot_measurement(hbi_innse_away, tc_innse_away, 'noise', 'away')
plot_measurement(hbi_innse_under, tc_innse_under, 'noise', 'under')
