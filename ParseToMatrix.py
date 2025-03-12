import numpy as np
import re

def parse_ing11(file_path):
    energy_levels = {}
    interactions = []
    parameters = {}  # To store Fk, zetai, Gk, Rk, etc.

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Step 1: Extract energy levels
    for line in lines:
        match = re.match(r'P\s+\d+\s+D\s+\d+.*Sn12\+\s+(\S+)\s+([-\d\.]+)', line)
        if match:
            state, energy = match.groups()
            energy_levels[state] = float(energy)

    # Step 2: Extract Fk, zetai, Gk, Rk, etc.
    for line in lines:
        # Check if the line starts with a configuration (e.g., Sn12+ 4p64d2)
        state_match = re.match(r'(Sn12\+)\s+(\S+)\s+(\d+)\s+(.*)', line)
        if state_match:
            ion, config, num_params, rest = state_match.groups()
            key = f"{ion} {config}"  # Combine ion and config as the key
            # Extract all numerical values from the rest of the line
            values = re.findall(r'([-\d\.]+)', rest)
            # Convert values to floats
            values = [float(val) for val in values]
            # Store in the parameters dictionary
            parameters[key] = values

    # step 3 interactions
    for line in lines:
        match = re.match(r'(Sn12\+\s+\S+)\s+(Sn12\+\s+\S+)\s+([-\d\.]+)', line)
        if match:
            state1, state2, value = match.groups()
            interactions.append((state1.strip(), state2.strip(), float(value)))
    

    return energy_levels, interactions, parameters

# Example usage:
file_path = "ING11.txt"  # Replace with actual path
energy_levels, interactions, parameters = parse_ing11(file_path)

print("energy_levels:", energy_levels)
print("parameters:", parameters)


