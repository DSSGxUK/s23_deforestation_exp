#!/bin/bash
module load GCC/10.3.0  OpenMPI/4.1.1
module load GDAL/3.3.0

# Time window as an argument
time_window=$1

if ! [[ $time_window =~ ^[0-9]+$ ]]
then
    echo "Please provide a numeric time window argument."
    exit 1
fi

# loop through the years
for ((start_year=2012; start_year<=2016; start_year++)); do
    # set end year to be the time window ahead
    end_year=$((start_year + time_window - 1))

    # directory to hold final output files
    output_dir="output_$start_year-$end_year"
    
    if [ ! -d "$output_dir" ]; then
        mkdir "$output_dir"
    fi

    # loop through unique basenames and calculate average for each
    for base_name in $(ls output_${start_year}/*.tif | xargs -n 1 basename | cut -d'_' -f1 | uniq); do
        # create a string to hold the arguments for gdal_calc.py
        args="-A "
        calc=""
        
        # loop through the years in the current window
        for ((year=start_year; year<=end_year; year++)); do
            # collect file paths for this basename in this year
            for file in output_${year}/${base_name}_*.tif; do
                # add file path as argument for gdal_calc.py
                args+="$file "
            done
        done
        
        calc="numpy.average(A,axis=0)*0.09" # take average, *0.09 to convert in hectares
        args+="--outfile=\"$output_dir/${base_name}_average.tif\" --calc=\"$calc\" --NoDataValue=0 --type=Float32" 
        # run GDAL calculation
        eval "gdal_calc.py $args"
    done
done
