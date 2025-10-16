#!/bin/bash

# Hardcoded paths
CASE_DIR="/home/thk/openfoam_opencfs_coupling/openFoam"
XML_FILE="/home/thk/openfoam_opencfs_coupling/openCFS/propagation.xml"

# Start icoFoam in the case folder in the background
cd "$CASE_DIR"
icoFoam &

# Open XML file in existing VSCode window
code --reuse-window "$XML_FILE"
