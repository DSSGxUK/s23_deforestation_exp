#!/bin/bash

# Check if the correct arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 start_year end_year"
    exit 1
fi

start_year=$1
end_year=$2

# Load necessary modules
module load GCCcore/11.3.0
module load Python/3.10.4
module load GCC/11.3.0 OpenMPI/4.1.4
module load GDAL/3.5.0
module load parallel/20220722

# Function to handle processing
do_work() {
    year="$1"
    input_file="$2"
    output_dir="output_$year"
    output_file="$output_dir/$(basename "$input_file" .tif)_downsampled.tif"

    if [ ! -d "$output_dir" ]; then
        mkdir "$output_dir"
    fi

    python3 downsample.py "$input_file" "$output_file" --grid_size 200 --pixel-class deforestation
}

export -f do_work

# Parallel execution
for year in $(seq $start_year $end_year); do
    find y_$year -name '*.tif' | parallel -j8 do_work "$year" {}
done
