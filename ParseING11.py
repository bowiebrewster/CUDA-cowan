import numpy as np
import re

def parse_ing11(file_path):
    energy_levels = {}
    parameters = {}  
    interactions1 = {}
    interactions2 = {}
    

    ion_pattern = r'[A-Z][a-z]?\d*\+'
    stage = 0

    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    for line in lines[1:]:
        
        # Step 1: average energies
        # P 6  D 2  S 0  S 0  S 0  S 0  S 0  S 0  Sn12+  4p64d2      -1344349.342   0.0000
        match1 = re.match(r'(?:[A-Z]\s+\d+\s+){7}[A-Z]\s+\d+', line)
        if match1 and stage <= 1:
            stage = 1
            key = line.split()[16]+ " "+line.split()[17]
            value = line.split()[18]
            energy_levels[key] = value

        # Step 2: # To store Fk, zetai, Gk, Rk, etc.
        # Sn12+  4p64d2      7   5675090  10124861   6846241 0.00E+001 0.00E+001hr87998787
        # 0.00E+001    486792
        match2 = re.match(rf'({ion_pattern})\s+(\S+)\s+(\d+)\s+(.*)', line)
        if match2 and stage <= 2:
            stage = 2
            filtered_data = [item for item in line.split()[3:-1] if 'hr' not in item and '0.00E+' not in item and not float(item) == 0]
            comb_key= line.split()[0]+" "+line.split()[1]
            parameters[comb_key] = filtered_data


        match3 = re.match(r'\s*(\S+)\s*-\s*(\S+)\s+(.*)', line)
        if match3 and stage <= 3:
            stage = 3
            state1, state2, value = match3.groups()
            key = f"{state1} - {state2}"
            filtered_data = [item for item in line.split()[4:-1] if 'hr' not in item and '0.00E+' not in item and not float(item) == 0]
            interactions1[key] = filtered_data

        # step 4: interactions 2
        # Sn12+  4p64d2       Sn12+  4p54d3          1.17716( 4P//R1// 4D)-0.999hr -97 -98
        pattern = r'(Sn\d+\+\s+\S+)\s+(Sn\d+\+\s+\S+)\s+([-\d.]+\(\s*[^)]+\)-?\d*\.?\d*\w*\s+-?\d+\s+-?\d+)'
        match4 = re.match(pattern, line)
        if match4 and stage <= 4:
            stage = 4
            key = line.split()[0]+" "+line.split()[1]+" "+line.split()[2]+" "+line.split()[3]
            value = line.split()[4:-1]
            interactions2[key] = value
        
        # extra F,G,K's after checking if not stage 3
        if not match2 and stage == 2:
            filtered_data = [item for item in line.split() if 'hr' not in item and '0.00E+' not in item]
            parameters[comb_key] += filtered_data

    return energy_levels, parameters, interactions1, interactions2


def main(file_path):
    return parse_ing11(file_path)

# for implementing ING11_8
# this line also rolls over
#  p34f    - pdf2    7 100.23445 124.27465  79.74315  96.22265  66.41725hr85998585
#  95.33205  64.24935
# stages revert sometimes for some reason 