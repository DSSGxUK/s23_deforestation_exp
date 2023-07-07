#!/bin/bash

for year in {2012..2021}; do
    for input_file in y_$year/*.tif; do
        output_dir="output_ed_$year"
        output_file="$output_dir/$(basename "$input_file" .tif)_ed.tif"

        if [ ! -d "$output_dir" ]; then
            mkdir "$output_dir"
        fi

        python3 edge_density.py "$input_file" "$output_file" &
    done
done

# Wait for all background jobs to finish
wait
