import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

serial_num   = '20USBHX2002884' # used for naming

# --- Load Data --- #
hbi_3pg_innse_away       = np.load('hbi_3pg_innse_away.npy')
hbi_10pg_innse_away      = np.load('hbi_10pg_innse_away.npy')
hbi_3pg_innse_under      = np.load('hbi_3pg_innse_under.npy')
hbi_10pg_innse_under     = np.load('hbi_10pg_innse_under.npy')

tc_warm_3pg_innse_away   = np.load('tc_warm_3pg_innse_away.npy')
tc_warm_10pg_innse_away  = np.load('tc_warm_10pg_innse_away.npy')
tc_warm_3pg_innse_under  = np.load('tc_warm_3pg_innse_under.npy')
tc_warm_10pg_innse_under = np.load('tc_warm_10pg_innse_under.npy')

tc_cold_3pg_innse_away   = np.load('tc_cold_3pg_innse_away.npy')
tc_cold_10pg_innse_away  = np.load('tc_cold_10pg_innse_away.npy')
tc_cold_3pg_innse_under  = np.load('tc_cold_3pg_innse_under.npy')
tc_cold_10pg_innse_under = np.load('tc_cold_10pg_innse_under.npy')

# --- Get Differences --- #
# --- Since data is passed as NumPy objects, operations can be done directly
diff_warm_3pg_away  = tc_warm_3pg_innse_away - hbi_3pg_innse_away
diff_warm_10pg_away = tc_warm_10pg_innse_away - hbi_10pg_innse_away
diff_warm_3pg_under  = tc_warm_3pg_innse_under - hbi_3pg_innse_under
diff_warm_10pg_under = tc_warm_10pg_innse_under - hbi_10pg_innse_under

diff_cold_3pg_away  = tc_cold_3pg_innse_away - hbi_3pg_innse_away
diff_cold_10pg_away = tc_cold_10pg_innse_away - hbi_10pg_innse_away
diff_cold_3pg_under  = tc_cold_3pg_innse_under - hbi_3pg_innse_under
diff_cold_10pg_under = tc_cold_10pg_innse_under - hbi_10pg_innse_under

# --- Plot Stuff --- #
def plot_measurement(y_data, stream, y_ID):
    channel_labels = np.repeat(np.arange(10), 128)
    cmap           = plt.cm.get_cmap("tab10")
    
    plt.figure(figsize=(10, 5))
    
    x_data  = np.arrange(len(diff_data)) # Should come out to 1280
    x_ID    = 'channel'
    measurement_name = 'TC_HBI_difference'
    scatter = plt.scatter(x_data, y_data, c=channel_labels, cmap=cmap)
    
    cbar = plt.colorbar(scatter, ticks=range(10))
    cbar.set_label('ABC')
    cbar.set_ticklabels([f'ABC {i}' for i in range(10)])
    
    plt.title(f"{serial_num} {measurement_name} {y_ID}, {stream} stream")
    plt.xlabel(f"{x_ID}")
    plt.ylabel(f"{y_ID} {measurement_name}")
    plt.grid()

    plt.savefig(f"{serial_num}-{measurement_name}-{stream}-{y_ID}.pdf")

plot_measurement(diff_warm_3pg_away, 'away', '3pg_warm')
plot_measurement(diff_warm_10pg_away, 'away', '10pg_warm')
plot_measurement(diff_warm_3pg_under, 'under', '3pg_warm')
plot_measurement(diff_warm_10pg_under, 'under', '10pg_warm')

plot_measurement(diff_cold_3pg_away, 'away', '3pg_cold')
plot_measurement(diff_cold_10pg_away, 'away', '10pg_cold')
plot_measurement(diff_cold_3pg_under, 'under', '3pg_cold')
plot_measurement(diff_cold_10pg_under, 'under', '10pg_cold')
