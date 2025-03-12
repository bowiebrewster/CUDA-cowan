#!/bin/bash

# Navigate to the directory where the input files are located
cd /c/Users/brewster/Desktop/CUDA\ Cowan

# Run RCN.BAT with input file IN36
echo "Running RCN.BAT..."
./Cowan/CODE/RCN.BAT < ./IN36 > ./OUT36

# Check if RCN.BAT ran successfully
if [ $? -eq 0 ]; then
    echo "RCN.BAT completed successfully."
else
    echo "RCN.BAT failed. Exiting..."
    exit 1
fi

# Run RCN2.BAT with input file IN2
echo "Running RCN2.BAT..."
./Cowan/CODE/RCN2.BAT < ./IN2 > ./OUT2

# Check if RCN2.BAT ran successfully
if [ $? -eq 0 ]; then
    echo "RCN2.BAT completed successfully."
else
    echo "RCN2.BAT failed. Exiting..."
    exit 1
fi




