#!/bin/bash

# This line ensures the script exits if an error occurs
set -e

# Check if an architecture argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <arch>"
    exit 1
fi

# The architecture argument
ARCH=$1

# Specify the path to your Python script
PYTHON_SCRIPT="figure_draw.py"

# Conditionally execute commands based on the architecture argument
if [ "$ARCH" == "Sycamore" ]; then
    echo "Running script for Sycamore architecture..."
    /opt/anaconda3/bin/python figure_draw.py Sycamore ../csv_data/our_sycamore_leq100.csv ../csv_data/sabre_sycamore_leq100.csv depth
    /opt/anaconda3/bin/python figure_draw.py Sycamore ../csv_data/our_sycamore_leq100.csv ../csv_data/sabre_sycamore_leq100.csv swap
elif [ "$ARCH" == "Heavy-hex" ]; then
    echo "Running script for Heavy-hex architecture..."
    /opt/anaconda3/bin/python figure_draw.py Heavy-hex ../csv_data/our_heavy-hex.csv ../csv_data/sabre45_heavy-hex_100.csv depth
    /opt/anaconda3/bin/python figure_draw.py Heavy-hex ../csv_data/our_heavy-hex.csv ../csv_data/sabre45_heavy-hex_100.csv swap
elif [ "$ARCH" == "Lattice_Surgery" ]; then
    /opt/anaconda3/bin/python figure_draw.py Lattice_Surgery ../csv_data/our_lattice_surgery_geq100.csv ../csv_data/sabre_lattice_surgery_geq100.csv depth
    /opt/anaconda3/bin/python figure_draw.py Lattice_Surgery ../csv_data/our_lattice_surgery_geq100.csv ../csv_data/sabre_lattice_surgery_geq100.csv swap
else
    echo "Running script for a different architecture: $ARCH..."
fi


