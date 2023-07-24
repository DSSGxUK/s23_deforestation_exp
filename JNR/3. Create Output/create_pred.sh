#!/bin/bash

# Arguments
csv_file=$1                  # Deforestation rate per category (defrate_per_cat_wsXX_XX.csv) obtained from the JNR algorithm
raster_file=$2               # Risk map raster file (riskmap_wsXX_XX.tif) obtained from the JNR algorithm
out_dir=$3                   # Output directory
num_years=$4                 # Number of years to predict
downsample_size=$5           # Downsampled pixel size (in meters)

# Create variables
riskmap=$raster_file
column_number=4
factor=$(($downsample_size/30))            # Calculate factor of downsampled pixel size
column_values=()                           # Create empty array to store column values

# Create output directory if it does not exist
mkdir -p $output_dir

echo "Processing $csv_file..."
# Ignore the first line (header) and read the rest of the lines
while IFS=',' read -r -a row; do
    # Skip the header row
    if $is_header; then
        is_header=false
        continue
    fi
    # if the value is "" then column value should get 0
    if [[ ${row[$((column_number-1))]} == "" ]]; then
        column_values+=("0")
    else
        column_values+=("${row[$((column_number-1))]}")
    fi
done < "$csv_file"

# Set the GDAL calculation expression
expression="900 * ("

echo "Generating deforestation prediction maps..."
# Repeat expression for each year
for ((j=1; j<=$num_years; j++)); do

    echo "Processing year $j..."

    for ((i=1; i<=${#column_values[@]}; i++)); do
        expression+=" ( B==$((i)) ) * ${column_values[((i-1))]} + "
    done
    expression+="0 )"

    echo "Expression: $expression"
    echo "Performing raster calculation..."

    # Perform the raster calculation using gdal_calc.py
    gdal_calc.py -A $raster_file -B $riskmap --outfile=${out_dir}/tmp1.tif --calc="$expression" --type=Float32 --overwrite --NoDataValue=-1

    # Set negative values to 0 (sanity check)
    gdal_calc.py -A ${out_dir}/tmp1.tif --outfile=${out_dir}/pred_defor_year-${j}.tif --calc="A * (A>=0)" --type=Float32 --overwrite --NoDataValue=-1
    
    # Calculate forest cover map
    if [ $j -eq 1 ]; then
        gdal_calc.py -A ${out_dir}/pred_defor_year-${j}.tif --outfile=${out_dir}/pred_forest_cover_year-${j}.tif --calc="900 - A" --type=Float32 --overwrite --NoDataValue=-1
    else
        gdal_calc.py -A ${out_dir}/pred_defor_year-${j}.tif -B ${out_dir}/pred_forest_cover_year-$((j-1)).tif --outfile=${out_dir}/pred_forest_cover_year-${j}.tif --calc="B-A" --type=Float32 --overwrite --NoDataValue=-1 --co="COMPRESS=LZW"
    fi

    # Remove the temporary files
    rm -rf ${out_dir}/tmp1.tif

    # Update the expression for the next year
    raster_file="${out_dir}/pred_forest_cover_year-${j}.tif"
    expression=" A * ("

done

echo "Maps has been generated, now downsampling..."

# Downsample for each year
for ((j=1; j<=$num_years; j++)); do

    echo "Downsampling year $j..."

    # Using gdalwarp, downsample from 30m to given resolution and convert to deforestation prediction maps
    gdalwarp -r sum -tr $downsample_size $downsample_size -ot Float32 -dstnodata -1 ${out_dir}/pred_defor_year-${j}.tif ${out_dir}/pred_defor_year-${j}_downsampled-${downsample_size}.tif 

done