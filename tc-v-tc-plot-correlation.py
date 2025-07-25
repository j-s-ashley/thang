import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

serial_num   = '20USBHX2002884' # used for naming

# --- Load Data --- #
tc1_warm_3pg_away         = np.load('tc1_warm_3pg_away.npy')
tc1_warm_10pg_away        = np.load('tc1_warm_10pg_away.npy')
tc1_warm_3pg_under        = np.load('tc1_warm_3pg_under.npy')
tc1_warm_10pg_under       = np.load('tc1_warm_10pg_under.npy')
tc1_warm_3pg_innse_away   = np.load('tc1_warm_3pg_innse_away.npy')
tc1_warm_10pg_innse_away  = np.load('tc1_warm_10pg_innse_away.npy')
tc1_warm_3pg_innse_under  = np.load('tc1_warm_3pg_innse_under.npy')
tc1_warm_10pg_innse_under = np.load('tc1_warm_10pg_innse_under.npy')

tc1_cold_3pg_away         = np.load('tc1_cold_3pg_away.npy')
tc1_cold_10pg_away        = np.load('tc1_cold_10pg_away.npy')
tc1_cold_3pg_under        = np.load('tc1_cold_3pg_under.npy')
tc1_cold_10pg_under       = np.load('tc1_cold_10pg_under.npy')
tc1_cold_3pg_innse_away   = np.load('tc1_cold_3pg_innse_away.npy')
tc1_cold_10pg_innse_away  = np.load('tc1_cold_10pg_innse_away.npy')
tc1_cold_3pg_innse_under  = np.load('tc1_cold_3pg_innse_under.npy')
tc1_cold_10pg_innse_under = np.load('tc1_cold_10pg_innse_under.npy')

tc2_warm_3pg_away         = np.load('tc2_warm_3pg_away.npy')
tc2_warm_10pg_away        = np.load('tc2_warm_10pg_away.npy')
tc2_warm_3pg_under        = np.load('tc2_warm_3pg_under.npy')
tc2_warm_10pg_under       = np.load('tc2_warm_10pg_under.npy')
tc2_warm_3pg_innse_away   = np.load('tc2_warm_3pg_innse_away.npy')
tc2_warm_10pg_innse_away  = np.load('tc2_warm_10pg_innse_away.npy')
tc2_warm_3pg_innse_under  = np.load('tc2_warm_3pg_innse_under.npy')
tc2_warm_10pg_innse_under = np.load('tc2_warm_10pg_innse_under.npy')

tc2_cold_3pg_away         = np.load('tc2_cold_3pg_away.npy')
tc2_cold_10pg_away        = np.load('tc2_cold_10pg_away.npy')
tc2_cold_3pg_under        = np.load('tc2_cold_3pg_under.npy')
tc2_cold_10pg_under       = np.load('tc2_cold_10pg_under.npy')
tc2_cold_3pg_innse_away   = np.load('tc2_cold_3pg_innse_away.npy')
tc2_cold_10pg_innse_away  = np.load('tc2_cold_10pg_innse_away.npy')
tc2_cold_3pg_innse_under  = np.load('tc2_cold_3pg_innse_under.npy')
tc2_cold_10pg_innse_under = np.load('tc2_cold_10pg_innse_under.npy')

def plot_measurement(x_data, y_data, measurement_name, stream, x_ID, y_ID):
    channel_labels = np.repeat(np.arange(10), 128)
    cmap           = plt.cm.get_cmap("tab10")
    
    plt.figure(figsize=(10, 5))

    scatter = plt.scatter(x_data, y_data, c=channel_labels, cmap=cmap)
    
    cbar = plt.colorbar(scatter, ticks=range(10))
    cbar.set_label('ABC')
    cbar.set_ticklabels([f'ABC {i}' for i in range(10)])
    
    plt.title(f"{serial_num} {measurement_name}, {stream} stream, {x_ID} vs {y_ID}")
    plt.xlabel(f"{x_ID} {measurement_name}")
    plt.ylabel(f"{y_ID} {measurement_name}")
    plt.grid()

    plt.savefig(f"{serial_num}-{measurement_name}-{stream}-{x_ID}-vs-{y_ID}.pdf")

plot_measurement(tc1_warm_3pg_away, tc2_warm_3pg_away, 'warm_TC_3PG', 'away', 'pre-deionizing', 'post-deionizing')
plot_measurement(tc1_warm_3pg_under, tc2_warm_3pg_under, 'warm_TC_3PG', 'under', 'pre-deionizing', 'post-deionizing')
plot_measurement(tc1_cold_3pg_away, tc2_cold_3pg_away, 'cold_TC_3PG', 'away', 'pre-deionizing', 'post-deionizing')
plot_measurement(tc1_cold_3pg_under, tc2_cold_3pg_under, 'cold_TC_3PG', 'under', 'pre-deionizing', 'post-deionizing')

plot_measurement(tc1_warm_10pg_away, tc2_warm_10pg_away, 'warm_TC_10PG', 'away', 'pre-deionizing', 'post-deionizing')
plot_measurement(tc1_warm_10pg_under, tc2_warm_10pg_under, 'warm_TC_10PG', 'under', 'pre-deionizing', 'post-deionizing')
plot_measurement(tc1_cold_10pg_away, tc2_cold_10pg_away, 'cold_TC_10PG', 'away', 'pre-deionizing', 'post-deionizing')
plot_measurement(tc1_cold_10pg_under, tc2_cold_10pg_under, 'cold_TC_10PG', 'under', 'pre-deionizing', 'post-deionizing')

plot_measurement(tc1_warm_3pg_innse_away, tc2_warm_3pg_innse_away, 'warm_TC_noise', 'away', 'pre-deionizing', 'post-deionizing')
plot_measurement(tc1_warm_3pg_innse_under, tc2_warm_3pg_innse_under, 'warm_TC_noise', 'under', 'pre-deionizing', 'post-deionizing')
plot_measurement(tc1_cold_3pg_innse_away, tc2_cold_3pg_innse_away, 'cold_TC_noise', 'away', 'pre-deionizing', 'post-deionizing')
plot_measurement(tc1_cold_3pg_innse_under, tc2_cold_3pg_innse_under, 'cold_TC_noise', 'under', 'pre-deionizing', 'post-deionizing')
