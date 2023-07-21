#!/bin/bash

# Arguments
start_year=$1               # Inclusive
end_year=$2                 # Inclusive
defor_dir=$3                # Directory containing deforestation masks
output_dir=$4               # Directory to save output

# Create output dir if it doesn't exist
mkdir -p $output_dir

# Variables for creating arguments to gdal_calc.py
args_in=""
args_calc=""
id=65                        # ASCII for 'A'

# Create args for gdal_calc
for ((year=$start_year; year<=$end_year; year++)); do

    # Input file name
    file="${defor_dir}/merged_map_defor-mask_${year}.tif"

    # Convert id to alphabet
    letter=$(printf "\x$(printf %x $id)")
    args_in="${args_in} -${letter} ${file}"

    # Increment id
    id=$((id+1))

    # Add to calc
    args_calc="${args_calc} (${letter} == 1)*1 + "

done

# Add 0 to calc for completeness
args_calc="${args_calc} 0"

echo "Creating mask of deforestation from ${start_year} to ${end_year}..."
# Run calc to create mask of deforestation
gdal_calc.py ${args_in} --outfile=${output_dir}/tmp_map_defor-mask_$((start_year-2000))-$((end_year-2000)).tif --calc="${args_calc}" --NoDataValue=0 --overwrite --quiet --hideNoData
gdal_calc.py -A ${output_dir}/tmp_map_defor-mask_$((start_year-2000))-$((end_year-2000)).tif --calc="1*(A>0)" --outfile=${output_dir}/binary_defor-mask_$((start_year-2000))-$((end_year-2000)).tif --NoDataValue=0 --overwrite --quiet --hideNoData

# Remove tmp file
rm ${output_dir}/tmp_map_defor-mask_$((start_year-2000))-$((end_year-2000)).tif

# Variables
tmp_file=${output_dir}/tmp_map_defor-mask_$((start_year-2000))-$((end_year-2000)).tif
out_file=${output_dir}/tmp2_map_defor-mask_$((start_year-2000))-$((end_year-2000)).tif

cp ${output_dir}/binary_defor-mask_$((start_year-2000))-$((end_year-2000)).tif $tmp_file

# Convert mask to year of deforestation
for ((year=$start_year; year<=$end_year; year++)); do

    echo "Processing year ${year}..."
    echo "Input: $tmp_file"
    echo "Output: $out_file"

    cur_year=$((year-2000))

    # Add current year to the mask
    gdal_calc.py -A $tmp_file -B "${defor_dir}/merged_map_defor-mask_${year}.tif" --outfile=$out_file --calc="(A==1)*(B==1)*${cur_year} + (A==1)*(B!=1)*1 + (A>1)*A" --NoDataValue=0 --overwrite --quiet --hideNoData

    # Switch tmp and out files
    tmp=$tmp_file
    tmp_file=$out_file
    out_file=$tmp

done

echo "Done processing years. Creating final file and removing temporary files..."

# Rename final file
mv $tmp_file "${output_dir}/forest-loss-year_map_$((start_year-2000))-$((end_year-2000)).tif"

# Remove tmp file
rm $tmp_file $out_file
