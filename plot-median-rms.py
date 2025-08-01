import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

# --- Get RMS --- #
def get_rms_from_median(data):
    median = np.median(data, axis=1, keepdims=True)
    rms = np.sqrt(np.mean(np.square(data - median), axis=1))
    return rms

# --- Plot Stuff --- #
def plot_measurement(all_data, stream, y_ID):
    plt.figure(figsize=(10, 5))
    
    x_data = np.arange(len(next(iter(all_data.values()))[0]))  # x for each ASIC
    x_ID   = 'ASIC'
    measurement_name = 'median-3pg-noise-per-ASIC'
    
    cmap = plt.cm.get_cmap("tab10", len(all_data))
    for idx, (serial_num, (y_median, y_rms)) in enumerate(all_data.items()):
        plt.errorbar(
            x_data, y_median, yerr=y_rms, fmt='o', label=serial_num,
            color=cmap(idx), capsize=3
        )

    plt.title(f"{measurement_name} {y_ID}, {stream} stream")
    plt.xlabel(f"{x_ID}")
    plt.ylabel(f"{y_ID} {measurement_name}")
    plt.grid()
    plt.xticks(x_data)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    plt.savefig(f"all-{measurement_name}-{stream}-{y_ID}.pdf")
    plt.close()

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

        # --- Load Data --- #
        hbi_3pg_innse_away       = np.load(f"{module_sn}_hbi_3pg_innse_away.npy")
        hbi_3pg_innse_under      = np.load(f"{module_sn}_hbi_3pg_innse_under.npy")
        tc_warm_3pg_innse_away   = np.load(f"{module_sn}_tc_warm_3pg_innse_away.npy")
        tc_warm_3pg_innse_under  = np.load(f"{module_sn}_tc_warm_3pg_innse_under.npy")
        tc_cold_3pg_innse_away   = np.load(f"{module_sn}_tc_cold_3pg_innse_away.npy")
        tc_cold_3pg_innse_under  = np.load(f"{module_sn}_tc_cold_3pg_innse_under.npy")

        # --- Store Median and RMS of Data --- #
        # Since data is passed as NumPy objects, operations can be done directly
        data_groups[('away', 'hbi')][module_sn] = (
            np.median(hbi_3pg_innse_away, axis=1),
            get_rms_from_median(hbi_3pg_innse_away)
        )
        data_groups[('under', 'hbi')][module_sn] = (
            np.median(hbi_3pg_innse_under, axis=1),
            get_rms_from_median(hbi_3pg_innse_under)
        )
        data_groups[('away', 'tc_warm')][module_sn] = (
            np.median(tc_warm_3pg_innse_away, axis=1),
            get_rms_from_median(tc_warm_3pg_innse_away)
        )
        data_groups[('under', 'tc_warm')][module_sn] = (
            np.median(tc_warm_3pg_innse_under, axis=1),
            get_rms_from_median(tc_warm_3pg_innse_under)
        )
        data_groups[('away', 'tc_cold')][module_sn] = (
            np.median(tc_cold_3pg_innse_away, axis=1),
            get_rms_from_median(tc_cold_3pg_innse_away)
        )
        data_groups[('under', 'tc_cold')][module_sn] = (
            np.median(tc_cold_3pg_innse_under, axis=1),
            get_rms_from_median(tc_cold_3pg_innse_under)
        )

# Now plot each
for (stream, y_ID), data_dict in data_groups.items():
    plot_measurement(data_dict, stream, y_ID)
