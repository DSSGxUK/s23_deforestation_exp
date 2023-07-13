#!/bin/bash

for year in {2021..2022}; do
    for input_file in y_$year/*.tif; do
        output_dir="output_fc_$year"
        output_file="$output_dir/$(basename "$input_file" .tif)_downsampled.tif"

        if [ ! -d "$output_dir" ]; then
            mkdir "$output_dir"
        fi

        python3 downsample_forest_cover.py "$input_file" "$output_file" &
    done
done

# Wait for all background jobs to finish
wait
