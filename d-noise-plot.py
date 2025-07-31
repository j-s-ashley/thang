import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

# --- Plot Stuff --- #
def plot_measurement(serial_num, y_data, stream, y_ID):
    plt.figure(figsize=(10, 5))
    
    x_data  = np.arange(len(y_data)) # Should come out to 10
    x_ID    = 'ASIC'
    measurement_name = 'TC_HBI_difference'
    scatter = plt.scatter(x_data, y_data)
    
    plt.title(f"{serial_num} {measurement_name} {y_ID}, {stream} stream")
    plt.xlabel(f"{x_ID}")
    plt.ylabel(f"{y_ID} {measurement_name}")
    plt.grid()

    plt.savefig(f"{serial_num}-{measurement_name}-{stream}-{y_ID}.pdf")

# --- Plot for Each Serial Number --- #
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
    # --- Since data is passed as NumPy objects, operations can be done directly
    diff_warm_3pg_away  = tc_warm_3pg_innse_away - hbi_3pg_innse_away
    diff_warm_10pg_away = tc_warm_10pg_innse_away - hbi_10pg_innse_away
    diff_warm_3pg_under  = tc_warm_3pg_innse_under - hbi_3pg_innse_under
    diff_warm_10pg_under = tc_warm_10pg_innse_under - hbi_10pg_innse_under

    diff_cold_3pg_away  = tc_cold_3pg_innse_away - hbi_3pg_innse_away
    diff_cold_10pg_away = tc_cold_10pg_innse_away - hbi_10pg_innse_away
    diff_cold_3pg_under  = tc_cold_3pg_innse_under - hbi_3pg_innse_under
    diff_cold_10pg_under = tc_cold_10pg_innse_under - hbi_10pg_innse_under

    plot_measurement(module_sn, diff_warm_3pg_away, 'away', '3pg_warm')
    plot_measurement(module_sn, diff_warm_10pg_away, 'away', '10pg_warm')
    plot_measurement(module_sn, diff_warm_3pg_under, 'under', '3pg_warm')
    plot_measurement(module_sn, diff_warm_10pg_under, 'under', '10pg_warm')

    plot_measurement(module_sn, diff_cold_3pg_away, 'away', '3pg_cold')
    plot_measurement(module_sn, diff_cold_10pg_away, 'away', '10pg_cold')
    plot_measurement(module_sn, diff_cold_3pg_under, 'under', '3pg_cold')
    plot_measurement(module_sn, diff_cold_10pg_under, 'under', '10pg_cold')
