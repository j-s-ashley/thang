import json
import numpy as np
from pathlib import Path

# --- Serial Number, Locations, and File Name Patterns --- #
serial_num   = '20USBHX2002884'
hbi_dir      = Path('/opt/local/strips/ITk/hbi-tc-analysis/thang/inputs/LS153/hbi/unmerged/rc/')
hbi_file_sfx = '_RESPONSE_CURVE_PPA.json'
hbi_name     = 'SN' + serial_num + '*' + hbi_file_sfx
tc_dir       = Path('/opt/local/strips/ITk/hbi-tc-analysis/thang/inputs/LS153/tc/unmerged/rc/')
tc_file_sfx  = '_RESPONSE_CURVE_TC.json'
tc_name      = 'SN' + serial_num + '*' + tc_file_sfx

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
        matched_files.extend(directory.glob(f"SN{serial_num}*{num}{file_suffix}"))

    sorted_files = [str(directory) + '/' + f.name for f in matched_files]
        
    return sorted_files

hbi_sorted_files = get_sorted_files(hbi_dir, hbi_name, hbi_file_sfx)
tc_sorted_files  = get_sorted_files(tc_dir, tc_name, tc_file_sfx)

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
