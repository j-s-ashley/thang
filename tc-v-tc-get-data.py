import json
import numpy as np
from pathlib import Path

# --- Serial Numbers, Locations, and File Name Patterns --- #
test_suffix  = '_RESPONSE_CURVE_PPA'

hybrid_sn    = '20USBHX2002884'
module_sn    = '20USBML1236274'
tc1_dir      = Path('/opt/local/strips/ITk/data/20250711_LBNL_LS153_LS154_LS155_LS156/results/')
tc2_dir      = Path('/opt/local/strips/ITk/data/20250718_LBNL_PS_LS153_LS160_LS161_LS162/results/')
tc_sfx       = test_suffix + '.json'
tc_name      = 'SN' + hybrid_sn + '*' + tc_sfx
tc1_merge     = '/opt/local/strips/ITk/data/20250711_LBNL_LS153_LS154_LS155_LS156/merged_results/SN20USBML1236274_20250711_3_MODULE_TC.json'
tc2_merge     = '/opt/local/strips/ITk/data/20250718_LBNL_PS_LS153_LS160_LS161_LS162/merged_results/SN20USBML1236274_20250718_5_MODULE_TC.json'

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

tc1_warm_file_names, tc1_cold_file_names = get_warm_cold_tc_runs(tc1_merge)
tc2_warm_file_names, tc2_cold_file_names = get_warm_cold_tc_runs(tc2_merge)

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

tc1_sorted_files  = get_sorted_files(tc1_dir, tc_name, tc_sfx)
tc2_sorted_files  = get_sorted_files(tc2_dir, tc_name, tc_sfx)

# --- Sort TC Files into Types --- #
# Filter into warm and cold based on file name
warm_tc1_files    = [file for file in tc1_sorted_files if any(warm in file for warm in tc1_warm_file_names)]
cold_tc1_files    = [file for file in tc1_sorted_files if any(cold in file for cold in tc1_cold_file_names)]
warm_tc2_files    = [file for file in tc2_sorted_files if any(warm in file for warm in tc2_warm_file_names)]
cold_tc2_files    = [file for file in tc2_sorted_files if any(cold in file for cold in tc2_cold_file_names)]

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

tc1_warm_3pg, tc1_warm_10pg = filter_by_point_gain(warm_tc1_files)
tc1_cold_3pg, tc1_cold_10pg = filter_by_point_gain(cold_tc1_files)
tc2_warm_3pg, tc2_warm_10pg = filter_by_point_gain(warm_tc2_files)
tc2_cold_3pg, tc2_cold_10pg = filter_by_point_gain(cold_tc2_files)

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

tc1_warm_3pg_away, tc1_warm_3pg_under, tc1_warm_3pg_innse_away, tc1_warm_3pg_innse_under = get_measurements(tc1_warm_3pg)
tc1_warm_10pg_away, tc1_warm_10pg_under, tc1_warm_10pg_innse_away, tc1_warm_10pg_innse_under = get_measurements(tc1_warm_10pg)
tc1_cold_3pg_away, tc1_cold_3pg_under, tc1_cold_3pg_innse_away, tc1_cold_3pg_innse_under = get_measurements(tc1_cold_3pg)
tc1_cold_10pg_away, tc1_cold_10pg_under, tc1_cold_10pg_innse_away, tc1_cold_10pg_innse_under = get_measurements(tc1_cold_10pg)

tc2_warm_3pg_away, tc2_warm_3pg_under, tc2_warm_3pg_innse_away, tc2_warm_3pg_innse_under = get_measurements(tc2_warm_3pg)
tc2_warm_10pg_away, tc2_warm_10pg_under, tc2_warm_10pg_innse_away, tc2_warm_10pg_innse_under = get_measurements(tc2_warm_10pg)
tc2_cold_3pg_away, tc2_cold_3pg_under, tc2_cold_3pg_innse_away, tc2_cold_3pg_innse_under = get_measurements(tc2_cold_3pg)
tc2_cold_10pg_away, tc2_cold_10pg_under, tc2_cold_10pg_innse_away, tc2_cold_10pg_innse_under = get_measurements(tc2_cold_10pg)

# --- Get Mean and Save Data --- #
def save_mean_numpy(data, name):
    numpy_object = np.array(data)
    mean_data    = numpy_object.mean(axis=0)
    np.save(name, mean_data)

# TC (warm)
save_mean_numpy(tc1_warm_3pg_away, 'tc1_warm_3pg_away.npy')
save_mean_numpy(tc1_warm_3pg_under, 'tc1_warm_3pg_under.npy')
save_mean_numpy(tc1_warm_3pg_innse_away, 'tc1_warm_3pg_innse_away.npy')
save_mean_numpy(tc1_warm_3pg_innse_under, 'tc1_warm_3pg_innse_under.npy')

save_mean_numpy(tc1_warm_10pg_away, 'tc1_warm_10pg_away.npy')
save_mean_numpy(tc1_warm_10pg_under, 'tc1_warm_10pg_under.npy')
save_mean_numpy(tc1_warm_10pg_innse_away, 'tc1_warm_10pg_innse_away.npy')
save_mean_numpy(tc1_warm_10pg_innse_under, 'tc1_warm_10pg_innse_under.npy')

# TC (cold)
save_mean_numpy(tc1_cold_3pg_away, 'tc1_cold_3pg_away.npy')
save_mean_numpy(tc1_cold_3pg_under, 'tc1_cold_3pg_under.npy')
save_mean_numpy(tc1_cold_3pg_innse_away, 'tc1_cold_3pg_innse_away.npy')
save_mean_numpy(tc1_cold_3pg_innse_under, 'tc1_cold_3pg_innse_under.npy')

save_mean_numpy(tc1_cold_10pg_away, 'tc1_cold_10pg_away.npy')
save_mean_numpy(tc1_cold_10pg_under, 'tc1_cold_10pg_under.npy')
save_mean_numpy(tc1_cold_10pg_innse_away, 'tc1_cold_10pg_innse_away.npy')
save_mean_numpy(tc1_cold_10pg_innse_under, 'tc1_cold_10pg_innse_under.npy')

# TC2 (warm)
save_mean_numpy(tc2_warm_3pg_away, 'tc2_warm_3pg_away.npy')
save_mean_numpy(tc2_warm_3pg_under, 'tc2_warm_3pg_under.npy')
save_mean_numpy(tc2_warm_3pg_innse_away, 'tc2_warm_3pg_innse_away.npy')
save_mean_numpy(tc2_warm_3pg_innse_under, 'tc2_warm_3pg_innse_under.npy')

save_mean_numpy(tc2_warm_10pg_away, 'tc2_warm_10pg_away.npy')
save_mean_numpy(tc2_warm_10pg_under, 'tc2_warm_10pg_under.npy')
save_mean_numpy(tc2_warm_10pg_innse_away, 'tc2_warm_10pg_innse_away.npy')
save_mean_numpy(tc2_warm_10pg_innse_under, 'tc2_warm_10pg_innse_under.npy')

# TC2 (cold)
save_mean_numpy(tc2_cold_3pg_away, 'tc2_cold_3pg_away.npy')
save_mean_numpy(tc2_cold_3pg_under, 'tc2_cold_3pg_under.npy')
save_mean_numpy(tc2_cold_3pg_innse_away, 'tc2_cold_3pg_innse_away.npy')
save_mean_numpy(tc2_cold_3pg_innse_under, 'tc2_cold_3pg_innse_under.npy')

save_mean_numpy(tc2_cold_10pg_away, 'tc2_cold_10pg_away.npy')
save_mean_numpy(tc2_cold_10pg_under, 'tc2_cold_10pg_under.npy')
save_mean_numpy(tc2_cold_10pg_innse_away, 'tc2_cold_10pg_innse_away.npy')
save_mean_numpy(tc2_cold_10pg_innse_under, 'tc2_cold_10pg_innse_under.npy')
