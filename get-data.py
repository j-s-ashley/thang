import json
import numpy as np
from pathlib import Path

# --- Serial Numbers, Locations, and File Name Patterns --- #
test_suffix  = '_RESPONSE_CURVE_PPA'

hybrid_sn    = '20USBHX2002884'
hbi_dir      = Path('/opt/local/strips/ITk/hbi-tc-analysis/thang/inputs/LS153/hbi/unmerged/rc/')
hbi_sfx      = test_suffix + '.json'
hbi_name     = 'SN' + hybrid_sn + '*' + hbi_sfx

module_sn    = '20USBML1236274'
tc_dir       = Path('/opt/local/strips/ITk/hbi-tc-analysis/thang/inputs/LS153/tc/unmerged/rc/')
tc_sfx       = test_suffix + '.json'
tc_name      = 'SN' + hybrid_sn + '*' + tc_sfx
tc_merge     = '/opt/local/strips/ITk/data/20250711_LBNL_LS153_LS154_LS155_LS156/merged_results/SN20USBML1236274_20250711_3_MODULE_TC.json'

# --- Get Cold/Warm TC Results File Names --- #
def get_warm_cold_tc_runs(merge_file):
    with open(merge_file, 'r') as mf:
        merge_data = json.load(mf)
        stages = merge_data["properties"]["ColdJig_History"]

        warm_tc = []
        cold_tc = []

        for stage_name, stage_info in stages.items():
            tests = stage_info.get("itsdaq_test_info", {}).get("all_tests", [])
            if "_TC_WARM_TEST_" in stage_name:
                warm_tc.append(tests)
            elif "_TC_COLD_TEST_" in stage_name:
                cold_tc.append(tests)

        warm_tc_rc = [test for sublist in warm_tc for test in sublist if test_suffix in test]
        cold_tc_rc = [test for sublist in cold_tc for test in sublist if test_suffix in test]

        return warm_tc_rc, cold_tc_rc

tc_warm_file_names, tc_cold_file_names = get_warm_cold_tc_runs(tc_merge)

# --- Get and Order Files by Run Number --- #
def run_num_sort_key(num): # treat run numbers like floats
    primary, secondary = num.split('-') # split run number primary and secondary
    return float(f"{primary}.{secondary.zfill(3)}") # ensure 5_1 is sorted as 5.001

def get_sorted_files(directory, name_pattern, file_suffix):
    run_numbers = []
    for file in directory.glob(name_pattern):
        with open(file, 'r') as f:
            data = json.load(f)
        
            run_number = data["runNumber"]
            run_numbers.append(run_number)

    sorted_run_numbers = [n.replace('-','_') for n in sorted(run_numbers, key=run_num_sort_key)]
 
    matched_files = []
    for num in sorted_run_numbers:
        matched_files.extend(directory.glob(f"SN{hybrid_sn}*{num}{file_suffix}"))

    sorted_files = [str(directory) + '/' + f.name for f in matched_files]
        
    return sorted_files

hbi_sorted_files = get_sorted_files(hbi_dir, hbi_name, hbi_sfx)
tc_sorted_files  = get_sorted_files(tc_dir, tc_name, tc_sfx)
print(tc_sorted_files)
# --- Get Measurements in Order of Ascending Run Number --- #
def get_measurements(sorted_files):
    gain_away   = [] 
    gain_under  = []
    innse_away  = []
    innse_under = []

    for file in sorted_files:
        with open(file, 'r') as f:
            data = json.load(f)

            run_gain_away   = data["results"]["gain_away"]
            run_gain_under  = data["results"]["gain_under"]
            run_innse_away  = data["results"]["innse_away"]
            run_innse_under = data["results"]["innse_under"]
            gain_away.append(run_gain_away)
            gain_under.append(run_gain_under)
            innse_away.append(run_innse_away)
            innse_under.append(run_innse_under)

    return gain_away, gain_under, innse_away, innse_under

hbi_gain_away, hbi_gain_under, hbi_innse_away, hbi_innse_under = get_measurements(hbi_sorted_files)
tc_gain_away, tc_gain_under, tc_innse_away, tc_innse_under = get_measurements(tc_sorted_files)

# --- Save Data --- #
hbi_gain_a_np  = np.array(hbi_gain_away)
hbi_gain_u_np  = np.array(hbi_gain_under)
hbi_innse_a_np = np.array(hbi_innse_away)
hbi_innse_u_np = np.array(hbi_innse_under)

tc_gain_a_np  = np.array(tc_gain_away)
tc_gain_u_np  = np.array(tc_gain_under)
tc_innse_a_np = np.array(tc_innse_away)
tc_innse_u_np = np.array(tc_innse_under)

np.save('hbi_gain_away.npy', hbi_gain_a_np)
np.save('hbi_gain_under.npy', hbi_gain_u_np)
np.save('hbi_innse_away.npy', hbi_innse_a_np)
np.save('hbi_innse_under.npy', hbi_innse_u_np)

np.save('tc_gain_away.npy', tc_gain_a_np)
np.save('tc_gain_under.npy', tc_gain_u_np)
np.save('tc_innse_away.npy', tc_innse_a_np)
np.save('tc_innse_under.npy', tc_innse_u_np)
