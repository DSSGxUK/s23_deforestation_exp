#!/bin/bash
module load GCCcore/11.3.0
module load Python/3.10.4
module load GCC/11.3.0 OpenMPI/4.1.4
module load GDAL/3.5.0

# Year range, time window, and input directory basename as arguments
start_year=$1
end_year=$2
time_window=$3
input_dir_basename=$4

if ! [[ $start_year =~ ^[0-9]+$ ]] || ! [[ $end_year =~ ^[0-9]+$ ]] || ! [[ $time_window =~ ^[0-9]+$ ]]; then
echo "Please provide numeric start year, end year, and time window arguments."
exit 1
fi

# loop through the years
for ((year=start_year; year<=end_year; year++)); do
    # calculate the end year based on the time window
    end_window=$((year + time_window - 1))

    # directory to hold final output files
    output_dir="output_${year}-${end_window}"

    if [ ! -d "$output_dir" ]; then
        mkdir "$output_dir"
    fi

    # loop through unique basenames and calculate average for each
    for base_name in $(ls "${input_dir_basename}_${year}"/*.tif | xargs -n 1 basename | cut -d'_' -f1 | uniq); do
        # create a string to hold the arguments for gdal_calc.py
        args="-A "
        calc=""
        
        # loop through the years in the current window
        for ((current_year=year; current_year<=end_window; current_year++)); do
            # collect file paths for this basename in this year
            for file in "${input_dir_basename}_${current_year}/${base_name}_*.tif"; do
                # add file path as an argument for gdal_calc.py
                args+="$file "
            done
        done
        
        calc="numpy.average(A,axis=0)*0.09" # take average, *0.09 to convert from pixels to hectares
        args+="--outfile=\"$output_dir/${base_name}_average.tif\" --calc=\"$calc\" --NoDataValue=0 --type=Float32 --overwrite" 
        # run GDAL calculation
        eval "gdal_calc.py $args"
    done
done
