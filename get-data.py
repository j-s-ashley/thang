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

        w_tc_rc_formatted = [name.replace('-','_') for name in warm_tc_rc]
        c_tc_rc_formatted = [name.replace('-','_') for name in cold_tc_rc]

        return w_tc_rc_formatted, c_tc_rc_formatted

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

# --- Sort TC Files into Types --- #
# Filter into warm and cold based on file name
warm_tc_files    = [file for file in tc_sorted_files if any(warm in file for warm in tc_warm_file_names)]
cold_tc_files    = [file for file in tc_sorted_files if any(cold in file for cold in tc_cold_file_names)]

# Filter into 3-point and 10-point gain
def get_test_type(rc_file):
    '''
    Adapted from Madison Levagood's beautiful work
    https://github.com/mlevagood/tc-summary-plotting/blob/master/common_functions.py#L274
    '''
    with open(rc_file, 'r') as rcf:
        rc_data = json.load(rcf)        
        ft_code = rc_data["properties"]["fit_type_code"]
        if ft_code == 4:
            test_type = "3PG"
        elif ft_code == 3:
            test_type = "10PG"
        return test_type

def filter_by_point_gain(test_list):
    threepg = []
    tenpg   = []
    for test in test_list:
        if get_test_type(test) == "3PG":
            threepg.append(test)
        else:
            tenpg.append(test)
    return threepg, tenpg

hbi_3pg, hbi_10pg         = filter_by_point_gain(hbi_sorted_files)
tc_warm_3pg, tc_warm_10pg = filter_by_point_gain(warm_tc_files)
tc_cold_3pg, tc_cold_10pg = filter_by_point_gain(cold_tc_files)

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

hbi_3pg_away, hbi_3pg_under, hbi_3pg_innse_away, hbi_3pg_innse_under = get_measurements(hbi_3pg)
hbi_10pg_away, hbi_10pg_under, hbi_10pg_innse_away, hbi_10pg_innse_under = get_measurements(hbi_10pg)
tc_warm_3pg_away, tc_warm_3pg_under, tc_warm_3pg_innse_away, tc_warm_3pg_innse_under = get_measurements(tc_warm_3pg)
tc_warm_10pg_away, tc_warm_10pg_under, tc_warm_10pg_innse_away, tc_warm_10pg_innse_under = get_measurements(tc_warm_10pg)
tc_cold_3pg_away, tc_cold_3pg_under, tc_cold_3pg_innse_away, tc_cold_3pg_innse_under = get_measurements(tc_cold_3pg)
tc_cold_10pg_away, tc_cold_10pg_under, tc_cold_10pg_innse_away, tc_cold_10pg_innse_under = get_measurements(tc_cold_10pg)

# --- Save Data --- #
def save_with_numpy(data, name):
    numpy_object = np.array(data)
    np.save(name, numpy_object)

# HBI
save_with_numpy(hbi_3pg_away)
save_with_numpy(hbi_3pg_under)
save_with_numpy(hbi_3pg_innse_away)
save_with_numpy(hbi_3pg_innse_under)

save_with_numpy(hbi_10pg_away)
save_with_numpy(hbi_10pg_under)
save_with_numpy(hbi_10pg_innse_away)
save_with_numpy(hbi_10pg_innse_under)

# TC (warm)
save_with_numpy(tc_warm_3pg_away)
save_with_numpy(tc_warm_3pg_under)
save_with_numpy(tc_warm_3pg_innse_away)
save_with_numpy(tc_warm_3pg_innse_under)

save_with_numpy(tc_warm_10pg_away)
save_with_numpy(tc_warm_10pg_under)
save_with_numpy(tc_warm_10pg_innse_away)
save_with_numpy(tc_warm_10pg_innse_under)

# TC (cold)
save_with_numpy(tc_cold_3pg_away)
save_with_numpy(tc_cold_3pg_under)
save_with_numpy(tc_cold_3pg_innse_away)
save_with_numpy(tc_cold_3pg_innse_under)

save_with_numpy(tc_cold_10pg_away)
save_with_numpy(tc_cold_10pg_under)
save_with_numpy(tc_cold_10pg_innse_away)
save_with_numpy(tc_cold_10pg_innse_under)
