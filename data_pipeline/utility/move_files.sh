#!/bin/bash

# Define source and destination directories
src_dir=Data/Dynamic
dst_dir=Test_Data/Dynamic

mkdir -p "$dst_dir"

# Get all unique features
features=$(find "$src_dir" -mindepth 1 -maxdepth 1 -type d -exec basename {} \;)

# For each feature, get all unique years, and copy the cut.tif file
for feature in $features
do
    years=$(find "$src_dir/$feature" -mindepth 1 -maxdepth 1 -type d -exec basename {} \;)
    for year in $years
    do
        # Check if file exists
        if [ -f "$src_dir/$feature/$year/cut.tif" ]
        then
            # Make sure the destination directory exists
            mkdir -p "$dst_dir/$feature/$year"
            cp "$src_dir/$feature/$year/cut.tif" "$dst_dir/$feature/$year"
        fi
    done
done
