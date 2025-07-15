#!/bin/bash

# Go to the directory with the input files
cd "/c/Users/brewster/Desktop/CowanFrontend/InputOutputCowan" || { echo "cd failed"; exit 1; }

# Run RCN.BAT using its absolute path
echo "Running RCN.BAT..."
"/c/Users/brewster/Desktop/Cowan/CODE/RCN.BAT" < "./IN36" > "./OUT36"

if [ $? -eq 0 ]; then
    echo "RCN.BAT completed successfully."
else
    echo "RCN.BAT failed. Exiting..."
    exit 1
fi

# Run RCN2.BAT using its absolute path
echo "Running RCN2.BAT..."
"/c/Users/brewster/Desktop/Cowan/CODE/RCN2.BAT" < "./IN2" > "./OUT2"

if [ $? -eq 0 ]; then
    echo "RCN2.BAT completed successfully."
else
    echo "RCN2.BAT failed. Exiting..."
    exit 1
fi
