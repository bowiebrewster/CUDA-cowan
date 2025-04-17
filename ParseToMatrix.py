import numpy as np
import re

def parse_ing11(file_path):
    energy_levels = {}
    parameters = {}  
    interactions1 = {}
    interactions2 = []
    

    ion_pattern = r'[A-Z][a-z]?\d*\+'
    stage = 0

    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    for line in lines[1:]:
        
        # Step 1: average energies
        # P 6  D 2  S 0  S 0  S 0  S 0  S 0  S 0  Sn12+  4p64d2      -1344349.342   0.0000
        match1 = re.match(r'P\s+\d+\s+D\s+\d+.*Sn12\+\s+(\S+)\s+([-\d\.]+)', line)
        if match1 and stage <= 1:
            stage = 1
            state, energy = match1.groups()
            energy_levels[state] = float(energy)

        # Step 2: # To store Fk, zetai, Gk, Rk, etc.
        # Sn12+  4p64d2      7   5675090  10124861   6846241 0.00E+001 0.00E+001hr87998787
        # 0.00E+001    486792
        match2 = re.match(rf'({ion_pattern})\s+(\S+)\s+(\d+)\s+(.*)', line)
        if match2 and stage <= 2:
            stage = 2
            filtered_data = [item for item in line.split()[3:-1] if 'hr' not in item and '0.00E+' not in item]
            comb_key= line.split()[0]+" "+line.split()[1]
            parameters[comb_key] = filtered_data

        pattern = r'\s*(\S+)\s*-\s*(\S+)\s+(.*)'

        match3 = re.match(pattern, line)
        if match3 and stage <= 3:
            stage = 3
            print("hmmmm",line)
            state1, state2, value = match3.groups()
            key = f"{state1} - {state2}"
            value = value.split()
            interactions1[key] = value

        # extra F,G,K's after checking if not stage 3
        if not match2 and stage == 2:
            filtered_data = [item for item in line.split() if 'hr' not in item and '0.00E+' not in item]
            parameters[comb_key] += filtered_data

        # step 4: interactions 2
        # Sn12+  4p64d2       Sn12+  4p54d3          1.17716( 4P//R1// 4D)-0.999hr -97 -98
        pattern = r'(Sn\d+\+\s+\S+)\s+(Sn\d+\+\s+\S+)\s+([-\d.]+\(\s*[^)]+\)-?\d*\.?\d*\w*\s+-?\d+\s+-?\d+)'
        match4 = re.match(pattern, line)
        if match4 and stage <= 4:
            stage = 4
            interactions2.append(line)

    return energy_levels, parameters, interactions1, interactions2

# Example usage:
file_path = "ING11.txt"  # Replace with actual path
energy_levels, parameters, interactions1, interactions2 = parse_ing11(file_path)

print("energy_levels:", energy_levels)
print("parameters:", parameters)
print("interactions1:",interactions1)
print("interactions2:",interactions2)

