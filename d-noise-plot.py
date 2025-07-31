import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

# --- Plot Stuff --- #
def plot_measurement(all_data, stream, y_ID):
    plt.figure(figsize=(10, 5))
    
    x_data = np.arange(len(next(iter(all_data.values()))))
    x_ID   = 'ASIC'
    measurement_name = 'TC_HBI_difference'
    
    colors = plt.cm.get_cmap("tab10", len(all_data))
    for idx, (serial_num, y_data) in enumerate(all_data.items()):
        plt.plot(x_data, y_data, label=serial_num, color=colors(idx), marker='o')
    
    plt.title(f"{measurement_name} {y_ID}, {stream} stream")
    plt.xlabel(f"{x_ID}")
    plt.ylabel(f"{y_ID} {measurement_name}")
    plt.grid()
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    plt.savefig(f"all-{measurement_name}-{stream}-{y_ID}.pdf")
    plt.close()

# --- Plot for Each Serial Number --- #
data_groups = {
    ('away', '3pg_warm'): {},
    ('away', '10pg_warm'): {},
    ('under', '3pg_warm'): {},
    ('under', '10pg_warm'): {},
    ('away', '3pg_cold'): {},
    ('away', '10pg_cold'): {},
    ('under', '3pg_cold'): {},
    ('under', '10pg_cold'): {},
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
        data_groups[('away', '3pg_warm')][module_sn] = tc_warm_3pg_innse_away - hbi_3pg_innse_away
        data_groups[('away', '10pg_warm')][module_sn] = tc_warm_10pg_innse_away - hbi_10pg_innse_away
        data_groups[('under', '3pg_warm')][module_sn] = tc_warm_3pg_innse_under - hbi_3pg_innse_under
        data_groups[('under', '10pg_warm')][module_sn] = tc_warm_10pg_innse_under - hbi_10pg_innse_under
        data_groups[('away', '3pg_cold')][module_sn] = tc_cold_3pg_innse_away - hbi_3pg_innse_away
        data_groups[('away', '10pg_cold')][module_sn] = tc_cold_10pg_innse_away - hbi_10pg_innse_away
        data_groups[('under', '3pg_cold')][module_sn] = tc_cold_3pg_innse_under - hbi_3pg_innse_under
        data_groups[('under', '10pg_cold')][module_sn] = tc_cold_10pg_innse_under - hbi_10pg_innse_under

# Now plot each
for (stream, y_ID), data_dict in data_groups.items():
    plot_measurement(data_dict, stream, y_ID)
