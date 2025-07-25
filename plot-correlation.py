import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

serial_num   = '20USBHX2002884' # used for naming

# --- Load Data --- #
hbi_3pg_away             = np.load('hbi_3pg_away.npy')
hbi_10pg_away            = np.load('hbi_10pg_away.npy')
hbi_3pg_under            = np.load('hbi_3pg_under.npy')
hbi_10pg_under           = np.load('hbi_10pg_under.npy')
hbi_3pg_innse_away       = np.load('hbi_3pg_innse_away.npy')
hbi_10pg_innse_away      = np.load('hbi_10pg_innse_away.npy')
hbi_3pg_innse_under      = np.load('hbi_3pg_innse_under.npy')
hbi_10pg_innse_under     = np.load('hbi_10pg_innse_under.npy')

tc_warm_3pg_away         = np.load('tc_warm_3pg_away.npy')
tc_warm_10pg_away        = np.load('tc_warm_10pg_away.npy')
tc_warm_3pg_under        = np.load('tc_warm_3pg_under.npy')
tc_warm_10pg_under       = np.load('tc_warm_10pg_under.npy')
tc_warm_3pg_innse_away   = np.load('tc_warm_3pg_innse_away.npy')
tc_warm_10pg_innse_away  = np.load('tc_warm_10pg_innse_away.npy')
tc_warm_3pg_innse_under  = np.load('tc_warm_3pg_innse_under.npy')
tc_warm_10pg_innse_under = np.load('tc_warm_10pg_innse_under.npy')

tc_cold_3pg_away         = np.load('tc_cold_3pg_away.npy')
tc_cold_10pg_away        = np.load('tc_cold_10pg_away.npy')
tc_cold_3pg_under        = np.load('tc_cold_3pg_under.npy')
tc_cold_10pg_under       = np.load('tc_cold_10pg_under.npy')
tc_cold_3pg_innse_away   = np.load('tc_cold_3pg_innse_away.npy')
tc_cold_10pg_innse_away  = np.load('tc_cold_10pg_innse_away.npy')
tc_cold_3pg_innse_under  = np.load('tc_cold_3pg_innse_under.npy')
tc_cold_10pg_innse_under = np.load('tc_cold_10pg_innse_under.npy')

def plot_measurement(x_data, y_data, measurement_name, stream, x_ID, y_ID):
    channel_labels = np.repeat(np.arange(10), 128)
    cmap           = plt.cm.get_cmap("tab10")
    
    plt.figure(figsize=(10, 5))

    plt.scatter(x_data, y_data, c=channel_labels, cmap=cmap)
    
    cbar = plt.colorbar(scatter, ticks=range(10))
    cbar.set_label('ABC')
    cbar.set_ticklabels([f'ABC {i}' for i in range(10)])
    
    plt.title(f"{serial_num} {measurement_name}, {stream} stream, {x_ID} vs {y_ID}")
    plt.xlabel(f"{x_ID} {measurement_name}")
    plt.ylabel(f"{y_ID} {measurement_name}")
    plt.grid()

    plt.savefig(f"{serial_num}-{measurement_name}-{stream}-{x_ID}-vs-{y_ID}.pdf")

plot_measurement(hbi_3pg_away, tc_warm_3pg_away, '3PG', 'away', 'HBI', 'Warm_TC')
plot_measurement(hbi_3pg_under, tc_warm_3pg_under, '3PG', 'under', 'HBI', 'Warm_TC')
plot_measurement(hbi_3pg_innse_away, tc_warm_3pg_innse_away, 'noise', 'away', 'HBI', 'Warm_TC')
plot_measurement(hbi_3pg_innse_under, tc_warm_3pg_innse_under, 'noise', 'under', 'HBI', 'Warm_TC')
