import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

# --- Plot Stuff --- #
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

# --- Plot for Each Serial Number --- #
data_groups = {
    ('away', 'hbi'): {},
    ('under', 'hbi'): {},
    ('away', 'tc_warm'): {},
    ('under', 'tc_warm'): {},
    ('away', 'tc_cold'): {},
    ('under', 'tc_cold'): {},
}

with open("input-config.json") as i_c:
    input_config = json.load(i_c)
    for module in input_config:
        module_sn = module["module_sn"]

        # --- Load Data and Get ASIC Mean Values --- #
        hbi_3pg_innse_away       = np.load(f"{module_sn}_hbi_3pg_innse_away.npy").mean(axis=1)
        hbi_10pg_innse_away      = np.load(f"{module_sn}_hbi_10pg_innse_away.npy").mean(axis=1)
        hbi_3pg_innse_under      = np.load(f"{module_sn}_hbi_3pg_innse_under.npy").mean(axis=1)
        hbi_10pg_innse_under     = np.load(f"{module_sn}_hbi_10pg_innse_under.npy").mean(axis=1)

        tc_warm_3pg_innse_away   = np.load(f"{module_sn}_tc_warm_3pg_innse_away.npy").mean(axis=1)
        tc_warm_10pg_innse_away  = np.load(f"{module_sn}_tc_warm_10pg_innse_away.npy").mean(axis=1)
        tc_warm_3pg_innse_under  = np.load(f"{module_sn}_tc_warm_3pg_innse_under.npy").mean(axis=1)
        tc_warm_10pg_innse_under = np.load(f"{module_sn}_tc_warm_10pg_innse_under.npy").mean(axis=1)

        tc_cold_3pg_innse_away   = np.load(f"{module_sn}_tc_cold_3pg_innse_away.npy").mean(axis=1)
        tc_cold_10pg_innse_away  = np.load(f"{module_sn}_tc_cold_10pg_innse_away.npy").mean(axis=1)
        tc_cold_3pg_innse_under  = np.load(f"{module_sn}_tc_cold_3pg_innse_under.npy").mean(axis=1)
        tc_cold_10pg_innse_under = np.load(f"{module_sn}_tc_cold_10pg_innse_under.npy").mean(axis=1)

        # --- Get Differences --- #
        # Since data is passed as NumPy objects, operations can be done directly
        data_groups[('away', 'hbi')][module_sn] = hbi_10pg_innse_away - hbi_3pg_innse_away
        data_groups[('under', 'hbi')][module_sn] = hbi_10pg_innse_under - hbi_3pg_innse_under
        data_groups[('away', 'tc_warm')][module_sn] = tc_warm_10pg_innse_away - tc_warm_3pg_innse_away
        data_groups[('under', 'tc_warm')][module_sn] = tc_warm_10pg_innse_under - tc_warm_3pg_innse_under
        data_groups[('away', 'tc_cold')][module_sn] = tc_cold_10pg_innse_away - tc_cold_3pg_innse_away
        data_groups[('under', 'tc_cold')][module_sn] = tc_cold_10pg_innse_under - tc_cold_3pg_innse_under

# Now plot each
for (stream, y_ID), data_dict in data_groups.items():
    plot_measurement(data_dict, stream, y_ID)
