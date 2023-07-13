#!/bin/bash

for year in {2021..2021}; do
    for input_file in y_$year/*.tif; do
        output_dir="output_$year"
        output_file="$output_dir/$(basename "$input_file" .tif)_downsampled.tif"

        if [ ! -d "$output_dir" ]; then
            mkdir "$output_dir"
        fi

        python3 downsample.py "$input_file" "$output_file" --grid_size 200 --pixel-class deforestation &
    done
done

# Wait for all background jobs to finish
wait
