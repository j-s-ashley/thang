import json
import numpy as np
from pathlib import Path

serial_num   = '20USBHX2002885'
directory    = Path('/opt/local/strips/ITk/hbi-tc-analysis/tc-summary-plotting/inputs/LS154/hbi/unmerged/')
file_suffix  = '_RESPONSE_CURVE_PPA.json'
name_pattern = 'SN' + serial_num + '*' + file_suffix

# --- Get and Order Files by Run Number --- #
run_numbers = []

for file in directory.glob(name_pattern):
    with open(file, 'r') as f:
        data = json.load(f)
        
        run_number = data["runNumber"]
        run_numbers.append(run_number)

def run_num_sort_key(num): # treat run numbers like floats
    primary, secondary = num.split('-') # split run number primary and secondary
    return float(f"{primary}.{secondary.zfill(3)}") # ensure 5_1 is sorted as 5.001

sorted_run_numbers = [n.replace('-','_') for n in sorted(run_numbers, key=run_num_sort_key)]

matched_files = []
for num in sorted_run_numbers:
    matched_files.extend(directory.glob(f"SN{serial_num}*{num}{file_suffix}"))

sorted_files = [str(directory) + '/' + f.name for f in matched_files]

# --- Get Measurements in Order of Ascending Run Number --- #
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

# --- Save Data --- #
gain_a_np  = np.array(gain_away)
gain_u_np  = np.array(gain_under)
innse_a_np = np.array(innse_away)
innse_u_np = np.array(innse_under)

np.save('gain_away.npy', gain_a_np)
np.save('gain_under.npy', gain_u_np)
np.save('innse_away.npy', innse_a_np)
np.save('innse_under.npy', innse_u_np)
